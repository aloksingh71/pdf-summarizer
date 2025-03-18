import fitz

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF Extraction Failed: {str(e)}")