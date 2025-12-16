import pdfplumber
from abc import abstractmethod, ABC

class PDFExtractor(ABC):
    @abstractmethod
    def extract_text(self) -> str:
        """Extracts text from a PDF and returns a raw string."""
        pass

class PDFPlumberExtractor(PDFExtractor):
    def __init__(self, path: str):
        self.path = path

    def extract_text(self) -> str:
        """Extract readable text from a PDF using pdfplumber."""
        text = ""
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text
