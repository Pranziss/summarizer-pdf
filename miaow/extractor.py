import fitz  # PyMuPDF

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".txt") or file_path.endswith(".md"):
        return extract_txt_md(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def extract_txt_md(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()