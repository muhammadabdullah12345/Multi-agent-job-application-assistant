import pdfplumber

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text from an uploaded PDF file (Streamlit UploadedFile object).
    Falls back to pymupdf if pdfplumber fails.
    """
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
        else:
            raise ValueError("pdfplumber returned empty text")
    except Exception:
        # Fallback to pymupdf
        import fitz
        uploaded_file.seek(0)
        raw_bytes = uploaded_file.read()
        doc = fitz.open(stream=raw_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text.strip()