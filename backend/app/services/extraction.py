import re


class FieldExtractor:
    patterns = {
        "invoice_number": r"(?:invoice\s*(?:no|number|#)\s*[:\-]?\s*)([A-Z0-9\-\/]+)",
        "date": r"\b(\d{2}[\/\-]\d{2}[\/\-]\d{4}|\d{4}[\/\-]\d{2}[\/\-]\d{2})\b",
        "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "phone": r"\b(?:\+?\d[\d\s\-]{7,}\d)\b",
        "gst": r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b",
        "pan": r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "total_amount": r"(?:total|amount due|grand total)\s*[:\-]?\s*(?:INR|Rs\.?|\$)?\s*([0-9,]+(?:\.\d{2})?)",
    }

    def extract(self, document_type: str, text: str) -> dict[str, tuple[str, float]]:
        flags = re.IGNORECASE
        fields: dict[str, tuple[str, float]] = {}
        for name, pattern in self.patterns.items():
            match = re.search(pattern, text, flags)
            if match:
                fields[name] = (match.group(1) if match.groups() else match.group(0), 0.82)
        if document_type == "contract" and "signature" in text.lower():
            fields["signature_detected"] = ("true", 0.7)
        return fields

