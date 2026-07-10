from pathlib import Path
from PyPDF2 import PdfReader
import markdown

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        html = markdown.markdown(md_content)
        return html

def load_document(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    elif ext in [".md", ".markdown"]:
        return load_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
