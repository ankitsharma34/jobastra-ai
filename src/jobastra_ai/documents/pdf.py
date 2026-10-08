from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader
from pypdf.errors import PyPdfError

type PDFSource = bytes | str | Path


class PDFTextExtractionError(ValueError):
    """Raised when plain text cannot be extracted from a PDF."""


def extract_text(source: PDFSource) -> str:
    """Extract plain text from PDF bytes or a filesystem path.
    This function extracts embedded PDF text only. It does not perform OCR.
    """

    pdf_source: BinaryIO | str | Path
    pdf_source = BytesIO(source) if isinstance(source, bytes) else source

    try:
        reader = PdfReader(pdf_source)
        if reader.is_encrypted:
            raise PDFTextExtractionError("Encrypted PDFs are not supported")

        page_text = [text.strip() for page in reader.pages if (text := page.extract_text())]
    except PDFTextExtractionError:
        raise
    except (OSError, PyPdfError, ValueError) as exc:
        raise PDFTextExtractionError("Unable to read the supplied PDF") from exc

    text = "\n\n".join(part for part in page_text if part).strip()
    if not text:
        raise PDFTextExtractionError(
            "The PDF contains no extractable text; scanned PDFs require OCR"
        )
    return text
