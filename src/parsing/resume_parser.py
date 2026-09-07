import os
import sys
from pathlib import Path
import pdfplumber
from docx import Document
import pytesseract
from pdf2image import convert_from_path

# Tesseract executable (Windows fallback)
windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if sys.platform.startswith("win") and os.path.exists(windows_tesseract):
    pytesseract.pytesseract.tesseract_cmd = windows_tesseract

# Poppler bin folder (Windows fallback)
windows_poppler = r"C:\poppler\poppler-26.02.0\Library\bin"
POPPLER_PATH = windows_poppler if (sys.platform.startswith("win") and os.path.exists(windows_poppler)) else None


def extract_text(file_path):
    file_path = Path(file_path)

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf(file_path)

    elif suffix == ".docx":
        return extract_docx(file_path)

    elif suffix == ".txt":
        return file_path.read_text(encoding="utf-8")

    else:
        raise ValueError("Unsupported file type.")


def extract_pdf(file_path):
    """
    Try pdfplumber first.
    If no text found, use OCR.
    """

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # If text exists, return it
    if text.strip():
        print("✅ Text PDF Detected")
        return text

    # Otherwise OCR
    print("🖼 Scanned PDF Detected")
    return extract_pdf_ocr(file_path)


def extract_pdf_ocr(file_path):

    text = ""

    try:
        kwargs = {}
        if POPPLER_PATH and os.path.exists(POPPLER_PATH):
            kwargs["poppler_path"] = POPPLER_PATH

        images = convert_from_path(
            file_path,
            **kwargs
        )

        for image in images:
            text += pytesseract.image_to_string(image)

    except Exception as e:
        print(f"OCR warning: {e}")

    return text


def extract_docx(file_path):

    document = Document(file_path)

    return "\n".join(
        para.text for para in document.paragraphs
    )