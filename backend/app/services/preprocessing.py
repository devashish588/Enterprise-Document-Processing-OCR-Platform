import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_PDF_SUFFIXES = {".pdf"}
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}


class ImagePreprocessor:
    def preprocess(self, path: Path) -> Path:
        suffix = path.suffix.lower()
        if suffix in _PDF_SUFFIXES:
            return self._extract_pdf_text(path)
        if suffix in _IMAGE_SUFFIXES:
            return self._enhance_image(path)
        return path

    def _extract_pdf_text(self, path: Path) -> Path:
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(str(path))
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            if text.strip():
                out = path.with_suffix(".txt")
                out.write_text(text, encoding="utf-8")
                return out
        except Exception as exc:
            logger.warning("PDF text extraction failed for %s: %s", path.name, exc)
        return path

    def _enhance_image(self, path: Path) -> Path:
        try:
            import cv2

            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                return path
            image = cv2.fastNlMeansDenoising(image, h=10)
            image = cv2.equalizeHist(image)
            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            output = path.with_name(f"{path.stem}.preprocessed{path.suffix}")
            cv2.imwrite(str(output), image)
            return output
        except Exception as exc:
            logger.warning("Image preprocessing failed for %s: %s", path.name, exc)
            return path
