from dataclasses import dataclass
from pathlib import Path


@dataclass
class OCRPayload:
    text: str
    confidence: float
    engine: str


class OCRStrategy:
    name = "base"

    def extract(self, path: Path) -> OCRPayload:
        raise NotImplementedError


class TesseractOCRStrategy(OCRStrategy):
    name = "tesseract"

    def extract(self, path: Path) -> OCRPayload:
        try:
            from PIL import Image
            import pytesseract

            text = pytesseract.image_to_string(Image.open(path)).strip()
            return OCRPayload(text=text, confidence=0.85 if text else 0.0, engine=self.name)
        except Exception:
            text = path.read_text(encoding="utf-8", errors="ignore") if path.suffix.lower() in {".txt", ".md"} else ""
            return OCRPayload(text=text.strip(), confidence=0.5 if text else 0.0, engine=f"{self.name}-fallback")


class EasyOCRStrategy(OCRStrategy):
    name = "easyocr"

    def extract(self, path: Path) -> OCRPayload:
        try:
            import easyocr

            reader = easyocr.Reader(["en"], gpu=False)
            results = reader.readtext(str(path))
            text = "\n".join(item[1] for item in results)
            confidence = sum(float(item[2]) for item in results) / len(results) if results else 0.0
            return OCRPayload(text=text, confidence=confidence, engine=self.name)
        except Exception:
            return TesseractOCRStrategy().extract(path)


class OCREngine:
    def __init__(self, strategy: OCRStrategy | None = None):
        self.strategy = strategy or TesseractOCRStrategy()

    def extract(self, path: Path) -> OCRPayload:
        return self.strategy.extract(path)

