import os
import ollama
from pypdf import PdfReader
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. GENERATE A MULTI-PARAGRAPH SAMPLE PDF WITH A PLACEHOLDER
def create_sample_input_pdf(pdf_path):
    print(f"Creating sample input PDF: {pdf_path}...")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Paragraph 1
    p1 = "Paragraph 1: The Mars Rover 'Perseverance' touched down in the Jezero Crater to search for signs of ancient microbial life. The red Martian landscape is covered in coarse rust-colored dust, wind-swept dunes, and jagged basalt volcanic rocks under a thin, pale pink sky."
    # Paragraph 2
    p2 = "Paragraph 2: The rover uses a heavy robotic arm equipped with a drill to collect rock and soil samples. These core samples are sealed into airtight titanium tubes and left on the surface for a future retrieval mission to return them to Earth."
    # Placeholder
    placeholder = "Figure: A robotic rover drilling into red Martian rocks with dust storms in the background"
    # Paragraph 3
    p3 = "Paragraph 3: Scientists back on Earth monitor the telemetry data sent through the Deep Space Network. Every image sent back helps geologists map out the ancient lakebed that once filled the crater billions of years ago."
    # Paragraph 4
    p4 = "Paragraph 4: As solar power and battery tech improve, future missions will likely feature autonomous drones capable of flying through the thin carbon dioxide atmosphere, expanding our mapping range exponentially."
    
    # Draw them to the PDF file
    y = height - 60
    paragraphs = [p1, "", p2, "", placeholder, "", p3, "", p4]
    
    for text in paragraphs:
        if text.startswith("Figure:"):
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y, text)
            y -= 20
        elif text == "":
            y -= 15
        else:
            c.setFont("Helvetica", 11)
            # Simple soft text wrapping for the input generation
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
            y -= 15
            
    c.save()

# 2. READ PDF & EXTRACT SEPARATE PARAGRAPHS / PLACEHOLDERS
def parse_input_pdf(pdf_path):
    print(f"Parsing {pdf_path}...")
    reader = PdfReader(pdf_path)
    lines = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            lines.extend(text.split("\n"))
            
    paragraphs = []
    current_p = ""
    figure_description = None
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_p:
                paragraphs.append(current_p)
                current_p = ""
            continue
            
        if line.startswith("Figure:"):
            if current_p:
                paragraphs.append(current_p)
                current_p = ""
            figure_description = line.replace("Figure:", "").strip()
            paragraphs.append(f"IMAGE_PLACEHOLDER|{figure_description}")
        else:
            current_p += " " + line
            
    if current_p:
        paragraphs.append(current_p.strip())
        
    return paragraphs

# 3. ASK GEMMA TO WRITE CODE RELATED TO THE CONTEXT
def generate_contextual_illustration(context_text, figure_desc, output_img_path):
    print("Asking Gemma 4 to generate contextual drawing code...")
    prompt = f"""
You are an expert design tool helper. Based on the following background context and the figure description, write a Python script using PIL (Pillow) to draw a simple abstract diagram, pattern, or schematic block illustration that fits the theme.

[Context]:
{context_text}

[Figure Target]:
{figure_desc}

Requirements:
- Create an image using: img = Image.new('RGB', (600, 350), color='#1a1a2e')
- Draw shapes (rectangles, circles, lines) using ImageDraw.Draw(img) that relate visually to the context (e.g., use warm rust/red/orange colors for Mars).
- Do NOT use fonts or draw text inside the image.
- Output ONLY valid, executable python code inside markdown blocks. Do not add explanations.
"""
    try:
        response = ollama.chat(
            model='gemma4:e4b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw_content = response['message']['content']
        
        # Clean up code blocks safely
        if "```python" in raw_content:
            code = raw_content.split("```python")[1].split("```")[0].strip()
        elif "```" in raw_content:
            code = raw_content.split("```")[1].split("```")[0].strip()
        else:
            code = raw_content.strip()
            
        # Append save line to ensure it outputs properly
        if "img.save" not in code:
            code += f"\nimg.save('{output_img_path}')"
            
        print("Executing code generated by Gemma...")
        exec(code, globals())
        
    except Exception as e:
        print(f"Gemma dynamic generation failed or timed out ({e}). Using a themed fallback fallback canvas.")
        # Fallback themed drawing script
        img = Image.new('RGB', (600, 350), color='#2d1414')
        d = ImageDraw.Draw(img)
        # Draw a generic rusty red circle (Mars planet) and base blocks
        d.ellipse([(200, 75), (400, 275)], fill='#b85c38', outline='#e07a5f', width=4)
        d.rectangle([(50, 280), (550, 320)], fill='#5c3d3d')
        img.save(output_img_path)

# 4. REBUILD THE PDF WITH PROPER IMAGE INSERTION AND CAPTIONS
def compile_final_pdf(output_path, content_structure, image_file):
    print(f"Compiling final structural PDF into: {output_path}...")
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 60
    
    for item in content_structure:
        # Check if page bound overflow is approaching
        if y < 120:
            c.showPage()
            y = height - 60
            
        if item.startswith("IMAGE_PLACEHOLDER|"):
            desc = item.split("|")[1]
            y -= 10
            
            # Draw the image
            if os.path.exists(image_file):
                c.drawImage(image_file, 75, y - 220, width=450, height=210)
                y -= 230
                
            # Draw bold/italic styled caption below the image frame
            c.setFont("Helvetica-BoldOblique", 10)
            c.drawCentredString(width / 2, y, f"Figure: {desc}")
            y -= 35
            
        else:
            c.setFont("Helvetica", 11)
            # Wrap lines cleanly for final rendering
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
            y -= 25 # Paragraph spacing
            
    c.showPage()
    c.save()
    print("New Illustrated PDF successfully created!")

# --- ORCHESTRATION PIPELINE ---
if __name__ == "__main__":
    input_filename = "multi_para_input.pdf"
    output_filename = "final_structured_output.pdf"
    generated_img_path = "contextual_illustration.png"
    
    # Step 1: Initialize structured multiline sample PDF
    create_sample_input_pdf(input_filename)
    
    # Step 2: Extract text components and figure specifications
    parsed_items = parse_input_pdf(input_filename)
    
    # Gather background elements (Paragraphs 1 and 2) to build visual context
    context_accumulator = ""
    figure_caption = "A beautiful thematic diagram"
    
    for item in parsed_items:
        if item.startswith("IMAGE_PLACEHOLDER|"):
            figure_caption = item.split("|")[1]
            break
        else:
            context_accumulator += item + "\n"
            
    # Step 3: Run generative layout rendering logic via Gemma 4
    generate_contextual_illustration(context_accumulator, figure_caption, generated_img_path)
    
    # Step 4: Output the fully realized multi-paragraph document
    compile_final_pdf(output_filename, parsed_items, generated_img_path)

