"""
Extracts plain text from uploaded knowledge base files. Each format gets
its own small function; extract_text() dispatches by file extension so
the rest of the app (knowledge_base_service) only ever deals with plain
strings, never format-specific parsing libraries.
"""
import io

import docx
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {"pdf", "docx", "txt"}


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_docx_text(content: bytes) -> str:
    document = docx.Document(io.BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def _extract_txt_text(content: bytes) -> str:
    return content.decode("utf-8", errors="replace")


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def extract_text(filename: str, content: bytes) -> str:
    extension = get_extension(filename)

    if extension == "pdf":
        text = _extract_pdf_text(content)
    elif extension == "docx":
        text = _extract_docx_text(content)
    elif extension == "txt":
        text = _extract_txt_text(content)
    else:
        raise ValueError(f"Unsupported file type: .{extension}. Supported: PDF, DOCX, TXT.")

    text = text.strip()
    if not text:
        raise ValueError("No extractable text was found in this file.")
    return text
