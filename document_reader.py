# NOTE: Reuse candidate lifted from the team's prior project
# (eerele-art/MoveFlow-Learning-Walk). It already extracts text from PDF/DOCX/TXT
# uploads and matches our stack (pypdf, python-docx). Kept here so Ugo's
# knowledge-base-prep slice is self-contained and testable before the shared repo
# exists. Application ownership sits with Maria (app development) once merged.

from pathlib import Path

from docx import Document
from pypdf import PdfReader


def read_uploaded_file(file_path):
    """
    Extract text from a PDF, DOCX, or TXT file.

    Gradio gives us the temporary filepath of the uploaded document.
    """

    if not file_path:
        return ""

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(str(path))

        pages_text = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)

        return "\n\n".join(pages_text)

    if extension == ".docx":
        document = Document(str(path))

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n\n".join(paragraphs)

    if extension == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")

    raise ValueError(
        "Unsupported file type. Please upload a PDF, DOCX, or TXT file."
    )
