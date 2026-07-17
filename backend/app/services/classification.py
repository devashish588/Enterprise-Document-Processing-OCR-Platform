from dataclasses import dataclass
from pathlib import Path


@dataclass
class Classification:
    label: str
    confidence: float


_KEYWORD_MAP: dict[str, tuple[str, ...]] = {
    "invoice": ("invoice", "gst", "subtotal", "tax", "amount due", "bill to", "vendor"),
    "receipt": ("receipt", "cash", "change", "paid", "cashier"),
    "contract": ("agreement", "party", "terms", "signature", "whereas", "hereinafter"),
    "bank_statement": ("statement", "account", "balance", "transaction", "debit", "credit"),
    "id_card": ("passport", "license", "identity", "date of birth", "nationality"),
    "medical_report": ("patient", "diagnosis", "doctor", "clinical", "prescription"),
    "purchase_order": ("purchase order", "po number", "ship to", "order date"),
    "tax_document": ("tax return", "pan", "assessment year", "income tax"),
}


class DocumentClassifier:
    def classify(self, text: str) -> Classification:
        model_path = Path(__file__).with_name("classifier.pkl")
        if model_path.exists():
            try:
                import pickle

                with model_path.open("rb") as fh:
                    model = pickle.load(fh)
                label = str(model.predict([text])[0])
                confidence = float(max(model.predict_proba([text])[0])) if hasattr(model, "predict_proba") else 0.7
                return Classification(label, confidence)
            except Exception:
                pass
        haystack = text.lower()
        scores = {label: sum(1 for kw in keywords if kw in haystack) for label, keywords in _KEYWORD_MAP.items()}
        label, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            return Classification("general", 0.35)
        return Classification(label, min(0.95, 0.45 + score * 0.12))
