from dataclasses import dataclass
from pathlib import Path
import pickle


@dataclass
class Classification:
    label: str
    confidence: float


class DocumentClassifier:
    labels = {
        "invoice": ("invoice", "gst", "subtotal", "tax", "amount due"),
        "receipt": ("receipt", "cash", "change", "paid"),
        "contract": ("agreement", "party", "terms", "signature"),
        "bank_statement": ("statement", "account", "balance", "transaction"),
        "id_card": ("passport", "license", "identity", "date of birth"),
        "medical_report": ("patient", "diagnosis", "doctor", "clinical"),
    }

    def classify(self, text: str) -> Classification:
        model_path = Path(__file__).with_name("classifier.pkl")
        if model_path.exists():
            try:
                model = pickle.loads(model_path.read_bytes())
                label = str(model.predict([text])[0])
                confidence = max(model.predict_proba([text])[0]) if hasattr(model, "predict_proba") else 0.7
                return Classification(label, float(confidence))
            except Exception:
                pass
        haystack = text.lower()
        scores = {label: sum(1 for word in words if word in haystack) for label, words in self.labels.items()}
        label, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            return Classification("general", 0.35)
        return Classification(label, min(0.95, 0.45 + score * 0.15))
