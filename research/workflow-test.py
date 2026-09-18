import os
import ollama
from pypdf import PdfReader
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. READ PDF & CONVERT TO TEXT
def extract_text_from_pdf(pdf_path):
    print(f"Reading {pdf_path}...")
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text.strip()

# 2. MULTI-MODAL VISION FUNCTION (Optional Helper)
# Use this if you want Gemma to analyze a real image file on your Mac
def analyze_image_with_gemma(image_path, prompt):
    print(f"Analyzing image: {image_path}...")
    response = ollama.chat(
        model='gemma4:e4b',
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [image_path]
        }]
    )
    return response['message']['content']

# 3. TOOL USE & GENERATING AN ILLUSTRATION
def generate_illustration_code(story_text):
    print("Asking Gemma 4 to write illustration code...")
    prompt = f"Based on this text, write a Python snippet using PIL (Pillow) to draw a simple conceptual visual block/diagram or pattern illustration. Output ONLY valid, executable python code inside markdown blocks. Text: {story_text}"
    
    response = ollama.chat(
        model='gemma4:e4b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    raw_content = response['message']['content']
    
    # Tool-use imitation: Extract code from Markdown blocks
    if "```python" in raw_content:
        code = raw_content.split("```python")[1].split("```")[0].strip()
    elif "```" in raw_content:
        code = raw_content.split("```")[1].split("```")[0].strip()
    else:
        code = raw_content.strip()
    return code

# 4. COMPILING TEXT AND GENERATIVE PICTURES INTO A NEW PDF
def create_illustrated_pdf(output_path, original_text, image_path):
    print(f"Compiling final PDF to {output_path}...")
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Insert Extracted Text
    text_object = c.beginText(50, height - 50)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(14)
    
    # Soft wrap original text lines
    lines = original_text.split('\n')
    for line in lines[:20]:  # Limit lines for example page boundary safety
        if len(line) > 80:
            text_object.textLine(line[:80])
            text_object.textLine(line[80:160])
        else:
            text_object.textLine(line)
            
    c.drawText(text_object)
    
    # Insert the generated picture/illustration back into the PDF
    if os.path.exists(image_path):
        c.drawImage(image_path, 50, 100, width=400, height=250)
    
    c.showPage()
    c.save()
    print("PDF Creation Complete!")

# --- EXECUTION PIPELINE ---
if __name__ == "__main__":
    # Create a dummy input PDF to test if one doesn't exist
    test_pdf = "sample.pdf"
    if not os.path.exists(test_pdf):
        c = canvas.Canvas(test_pdf, pagesize=letter)
        c.drawString(100, 750, "The quick brown fox jumps over the lazy dog.")
        c.drawString(100, 730, "This is a local automation pipeline powered by Gemma 4.")
        c.save()
        
    # Execution steps
    extracted_text = extract_text_from_pdf(test_pdf)
    print(f"\n[Extracted Text]:\n{extracted_text}\n")
    
    # Get Python code dynamically constructed by Gemma
    drawing_code = generate_illustration_code(extracted_text)
    
    # Fallback default code if Gemma's output generation slips up due to 4B constraints
    illustration_file = "illustration.png"
    default_code = f"""
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 500), color='#f0f0f0')
d = ImageDraw.Draw(img)
d.rectangle([(100, 100), (700, 400)], fill='#4A90E2', outline='#1034A6', width=5)
img.save('{illustration_file}')
"""
    
    # Safely evaluate or fall back
    try:
        print("Executing generated drawing code...")
        # Ensure the filename target matches what we expect
        if "img.save" not in drawing_code:
            drawing_code += f"\nimg.save('{illustration_file}')"
        exec(drawing_code, globals())
    except Exception as e:
        print(f"Dynamic code failed ({e}). Running template illustration.")
        exec(default_code, globals())

    # Build final combined output
    create_illustrated_pdf("final_output.pdf", extracted_text, illustration_file)

