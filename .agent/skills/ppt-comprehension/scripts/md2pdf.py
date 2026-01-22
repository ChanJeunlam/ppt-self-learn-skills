
import sys
import markdown
import os
from weasyprint import HTML, CSS

def convert_md_to_pdf(md_file, pdf_file):
    print(f"Converting {md_file} to {pdf_file}...")
    
    # Read Markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{md_file}' not found.")
        sys.exit(1)

    # Pre-process to handle WMF images (not supported by WeasyPrint)
    # detailed strategy: find .wmf images and replace with a placeholder text
    # Ideally we would convert them, but without ImageMagick/LibWMF on the system, 
    # skipping is safer than crashing.
    import re
    
    # Pattern to find images with .wmf extension
    # ![Alt](path/to/image.wmf)
    wmf_pattern = re.compile(r'!\[(.*?)\]\((.*?\.wmf)\)', re.IGNORECASE)
    
    def wmf_replacer(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        print(f"Warning: Skipping WMF image '{img_path}' (not supported in PDF).")
        return f"> *[Image '{alt_text}' omitted: WMF format not supported in PDF generation]*"

    text = wmf_pattern.sub(wmf_replacer, text)

    # Convert Markdown to HTML
    # We use 'extra' extension for better features (tables, etc.)
    html_content = markdown.markdown(text, extensions=['extra', 'toc'])

    # Add basic CSS for styling
    # Ensure images fit within the page
    css_string = """
    body {
        font-family: sans-serif;
        line-height: 1.6;
        font-size: 11pt; /* Slightly smaller for density */
    }
    h1, h2, h3, h4 {
        color: #2c3e50;
        margin-top: 1.2em;
        margin-bottom: 0.5em;
    }
    h1 { font-size: 2em; border-bottom: 2px solid #2c3e50; padding-bottom: 0.2em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
    h3 { font-size: 1.2em; color: #34495e; }
    
    p { margin-bottom: 0.8em; text-align: justify; }
    
    /* List Handling */
    ul, ol {
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        padding-left: 1.5em;
    }
    li {
        margin-bottom: 0.3em;
    }
    
    img {
        max-width: 90%;
        height: auto;
        display: block;
        margin: 1em auto;
        border: 1px solid #eee;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    code {
        background-color: #f4f4f4;
        padding: 2px 4px;
        border-radius: 4px;
    }
    pre {
        background-color: #f4f4f4;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        white-space: pre-wrap; /* Wrap long lines in code blocks */
        word-wrap: break-word; 
    }
    blockquote {
        background-color: #f9f9f9;
        border-left: 5px solid #ccc;
        margin: 1.5em 10px;
        padding: 0.5em 10px;
    }
    /* Page breaks */
    h2 {
        page-break-before: always;
    }
    h2:first-of-type {
        page-break-before: avoid;
    }
    """

    # Resolve relative image paths
    # WeasyPrint needs a base URL to find images if they are relative
    base_url = os.path.dirname(os.path.abspath(md_file))

    # Generate PDF
    try:
        html = HTML(string=html_content, base_url=base_url)
        css = CSS(string=css_string)
        html.write_pdf(pdf_file, stylesheets=[css])
        print(f"Successfully created: {pdf_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: uv run md2pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    
    input_md = sys.argv[1]
    output_pdf = sys.argv[2]
    
    convert_md_to_pdf(input_md, output_pdf)
