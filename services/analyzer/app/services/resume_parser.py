"""Resume text parser service."""

from io import (
    BytesIO,
)

from docx import (
    Document,
)
from fastapi import (
    UploadFile,
)
from pypdf import (
    PdfReader,
)


class ResumeTextExtractor:
    """Extract text from PDF and DOCX resume file."""

    async def extract(self, file: UploadFile) -> str:
        """Extract text from PDF or DOCX file."""

        context = await file.read()
        text = ''

        if not file.filename:
            raise ValueError('Не удалось получить имя файла')

        if file.filename.endswith('.pdf'):
            text = self._extract_from_pdf(context)
        elif file.filename.endswith('.docx'):
            text = self._extract_from_docx(context)
        else:
            raise ValueError('Неподдерживаемый формат файла')

        return text

    @staticmethod
    def _extract_from_pdf(content: bytes) -> str:
        """Extract text from PDF file."""

        reader = PdfReader(BytesIO(content))

        return '\n'.join(
            page.extract_text()
            for page in reader.pages
        ).strip()


    @staticmethod
    def _extract_from_docx(content: bytes) -> str:
        """Extract text from DOCX file."""

        document = Document(BytesIO(content))

        return '\n'.join(
            paragraph.text
            for paragraph in document.paragraphs
        ).strip()
