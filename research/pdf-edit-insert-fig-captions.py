import os
import re
import sys
import ollama
from pypdf import PdfReader
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ==========================================
# 1. GENERATE A MULTI-PARAGRAPH SAMPLE PDF
# ==========================================
def create_sample_input_pdf(pdf_path):
    print(f"Creating sample input PDF: {pdf_path}...")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    paragraphs = [
        "Paragraph 1: The Mars Rover 'Perseverance' touched down "
        "in the Jezero Crater to search for signs of ancient "
        "microbial life. The red Martian landscape is covered "
        "in coarse rust-colored dust, wind-swept dunes, and "
        "jagged basalt volcanic rocks under a thin, pale pink sky.",

        "Paragraph 2: The rover uses a heavy robotic arm equipped "
        "with a drill to collect rock and soil samples. These "
        "core samples are sealed into airtight titanium tubes "
        "and left on the surface for a future retrieval mission "
        "to return them to Earth.",

        "Figure: A robotic rover drilling into red Martian rocks "
        "with dust storms in the background",

        "Paragraph 3: Scientists back on Earth monitor the telemetry "
        "data sent through the Deep Space Network. Every image sent "
        "back helps geologists map out the ancient lakebed that "
        "once filled the crater billions of years ago.",

        "Paragraph 4: As solar power and battery tech improve, "
        "future missions will likely feature autonomous drones "
        "capable of flying through the thin carbon dioxide "
        "atmosphere, expanding our mapping range exponentially.",
    ]

    y = height - 60
    for text in paragraphs:
        if text.startswith("Figure:"):
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y, text)
            y -= 30
        else:
            c.setFont("Helvetica", 11)
            words = text.split(" ")
            line = ""
            for word in words:
                if len(line + " " + word) < 85:
                    line += " " + word
                else:
                    c.drawString(50, y, line.strip())
                    y -= 15
                    line = word
            c.drawString(50, y, line.strip())
            y -= 25

    c.save()


# ==========================================
# 2. PARSER: PRESERVES PARAGRAPH BOUNDARIES
# ==========================================
def parse_input_pdf(pdf_path):
    print(f"Parsing {pdf_path}...")
    reader = PdfReader(pdf_path)
    lines = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            lines.extend(text.split("\n"))

    paragraphs = []
    current_p = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            continue

        if line.startswith("Figure:"):
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            figure_description = line.replace("Figure:", "").strip()
            paragraphs.append(f"IMAGE_PLACEHOLDER|{figure_description}")
        elif line.startswith("Paragraph ") and current_p:
            paragraphs.append(" ".join(current_p))
            current_p = [line]
        else:
            current_p.append(line)

    if current_p:
        paragraphs.append(" ".join(current_p))

    return paragraphs


# ==========================================
# 3. SANITIZE LLM-GENERATED PILLOW CODE
# ==========================================
def auto_correct_pillow_coordinates(code_str):
    def sort_bbox(match):
        nums = [int(n) for n in re.findall(r'\d+', match.group(0))]
        if len(nums) == 4:
            x0, y0, x1, y1 = nums
            return (f"[({min(x0, x1)}, {min(y0, y1)}), "
                    f"({max(x0, x1)}, {max(y0, y1)})]")
        return match.group(0)

    pattern = (r'\[\s*\(\s*\d+\s*,\s*\d+\s*\)\s*,\s*'
               r'\(\s*\d+\s*,\s*\d+\s*\)\s*\]')
    fixed_code = re.sub(pattern, sort_bbox, code_str)
    return fixed_code


def rewrite_circle_calls_to_ellipse(code_str):
    """Pillow's ImageDraw has no circle(); rewrite d.circle((cx, cy), r, ...)
    into the equivalent d.ellipse((cx - r, cy - r, cx + r, cy + r), ...)."""
    try:
        import ast

        if not hasattr(ast, "unparse"):
            return code_str

        tree = ast.parse(code_str)

        class CircleToEllipse(ast.NodeTransformer):
            def visit_Call(self, node):
                self.generic_visit(node)
                func = node.func
                if not isinstance(func, ast.Attribute) or func.attr != "circle":
                    return node
                if len(node.args) < 2:
                    return node
                center = node.args[0]
                if not isinstance(center, ast.Tuple) or len(center.elts) != 2:
                    return node
                radius = node.args[1]
                cx, cy = center.elts

                # Bounding box: (cx - r, cy - r, cx + r, cy + r)
                bbox = ast.Tuple(
                    elts=[
                        ast.BinOp(left=cx, op=ast.Sub(), right=radius),
                        ast.BinOp(left=cy, op=ast.Sub(), right=radius),
                        ast.BinOp(left=cx, op=ast.Add(), right=radius),
                        ast.BinOp(left=cy, op=ast.Add(), right=radius),
                    ],
                    ctx=ast.Load(),
                )

                func.attr = "ellipse"
                extra_args = node.args[2:]
                node.args = [bbox]

                # Map extra positional args onto ellipse()'s keyword params
                keyword_names = ["fill", "outline", "width"]
                for index, extra_arg in enumerate(extra_args):
                    if index < len(keyword_names):
                        node.keywords.append(
                            ast.keyword(arg=keyword_names[index], value=extra_arg)
                        )
                    else:
                        node.args.append(extra_arg)
                return node

        tree = CircleToEllipse().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except SyntaxError:
        return code_str


# ==========================================
# 4. SAFE MARKDOWN CODE BLOCK EXTRACTOR
# ==========================================
def extract_pure_code(markdown_content):
    if "```python" in markdown_content:
        first_split = markdown_content.split("```python")
        if len(first_split) > 1:
            second_split = first_split[1].split("```")
            return second_split[0].strip()
    elif "```" in markdown_content:
        first_split = markdown_content.split("```")
        if len(first_split) > 1:
            second_split = first_split[1].split("```")
            return second_split[0].strip()
    return markdown_content.strip()


# ==========================================
# 5. CODE GENERATION AND SANDBOX EXECUTION
# ==========================================
def generate_contextual_illustration(context_text,
                                     figure_desc,
                                     output_img_path):
    print("\n[Agent] Starting contextual illustration process...")
    prompt = f"""
You are an expert helper tool. Based on the context and target description,
write a clean Python script using PIL (Pillow) to draw an abstract diagram,
schematic, or pattern illustration that matches the layout theme.

[Background Context]:
{context_text}

[Figure Objective Target]:
{figure_desc}

Requirements:
- Setup a canvas layout using exactly: img = Image.new('RGB', (600, 350), color='#1a1a2e')
- Draw shapes (rectangles, circles, lines) using ImageDraw.Draw(img) matching the theme.
- Crucial: Bounding boxes like [(x0, y0), (x1, y1)] MUST have x1 > x0 and y1 > y0.
- Pillow's ImageDraw has NO circle() method; never call d.circle(...). To draw a
  circle centered at (cx, cy) with radius r, use d.ellipse((cx - r, cy - r, cx + r, cy + r), ...).
- Do NOT utilize external fonts or draw standard text strings inside the image.
- Output ONLY valid, executable python code inside markdown code blocks. No conversational text.
"""
    try:
        response = ollama.chat(
            model='gemma4:e4b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw_content = response['message']['content']

        # Unpack and sanitize cleanly
        code = extract_pure_code(raw_content)
        code = auto_correct_pillow_coordinates(code)
        code = rewrite_circle_calls_to_ellipse(code)

        if "img.save" not in code:
            code += f"\nimg.save('{output_img_path}')"

        print("Executing code generated by Gemma...")

        # Dynamic variable mapping proxy configuration
        class SafeSandbox(dict):
            def __getitem__(self, key):
                try:
                    return super().__getitem__(key)
                except KeyError:
                    k = key.lower()
                    if any(x in k for x in ['orange', 'rust', 'red']):
                        return '#d65a31'
                    if any(x in k for x in ['dust', 'sand', 'yellow']):
                        return '#e2b4bd'
                    if any(x in k for x in ['dark', 'basalt', 'rock']):
                        return '#393e46'
                    return '#eeeeee'

        sandbox_globals = SafeSandbox(globals())
        exec(code, sandbox_globals)

    except Exception as e:
        print(f"Parsing encountered exceptions ({e}). Running backup design canvas.")
        img = Image.new('RGB', (600, 350), color='#2d1414')
        d = ImageDraw.Draw(img)
        d.ellipse([(200, 75), (400, 275)], fill='#b85c38', outline='#e07a5f', width=4)
        d.rectangle([(50, 280), (550, 320)], fill='#5c3d3d')
        img.save(output_img_path)


# ==========================================
# 6. REBUILD STRUCTURAL PDF DOCUMENT
# ==========================================
def compile_final_pdf(output_path, content_structure, image_file):
    print(f"\nCompiling final structural PDF into: {output_path}...")
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 60

    for item in content_structure:
        if y < 150:
            c.showPage()
            y = height - 60

        if item.startswith("IMAGE_PLACEHOLDER|"):
            desc_parts = item.split("|")
            caption_text = desc_parts[1] if len(desc_parts) > 1 else "Illustration Diagram"
            y -= 15

            if os.path.exists(image_file):
                c.drawImage(image_file, 100, y - 220, width=400, height=220)
                y -= 235

            c.setFont("Helvetica-BoldOblique", 10)
            c.drawCentredString(width / 2, y, f"Figure: {caption_text}")
            y -= 35

        else:
            c.setFont("Helvetica", 11)
            words = item.split(" ")
            line = ""
            for word in words:
                if len(line + " " + word) < 80:
                    line += " " + word
                else:
                    c.drawString(60, y, line.strip())
                    y -= 16
                    line = word
            c.drawString(60, y, line.strip())
            y -= 25

    c.showPage()
    c.save()
    print("New Illustrated PDF successfully generated!")


# ==========================================
# EXECUTION ROUTINE
# ==========================================
if __name__ == "__main__":
    input_filename = "multi_para_input.pdf"
    output_filename = "final_structured_output.pdf"
    generated_img_path = "contextual_illustration.png"

    create_sample_input_pdf(input_filename)
    parsed_items = parse_input_pdf(input_filename)

    context_accumulator = ""
    figure_caption = "Abstract Martian Architecture Visual Guide"

    for item in parsed_items:
        if item.startswith("IMAGE_PLACEHOLDER|"):
            desc_parts = item.split("|")
            if len(desc_parts) > 1:
                figure_caption = desc_parts[1]
            break
        else:
            context_accumulator += item + "\n"

    generate_contextual_illustration(
        context_accumulator, figure_caption, generated_img_path
    )
    compile_final_pdf(output_filename, parsed_items, generated_img_path)
