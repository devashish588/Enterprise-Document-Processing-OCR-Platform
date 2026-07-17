from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models import Document


class SearchEngine:
    def rank(self, query: str, documents: list[Document]) -> list[tuple[Document, float, str]]:
        texts = [(doc.ocr_result.text if doc.ocr_result else doc.filename) for doc in documents]
        if not query or not texts:
            return [(doc, 0.0, "") for doc in documents]
        matrix = TfidfVectorizer(stop_words="english").fit_transform([query, *texts])
        scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
        ranked = sorted(zip(documents, scores), key=lambda item: item[1], reverse=True)
        return [(doc, float(score), (doc.ocr_result.text[:180] if doc.ocr_result else doc.filename)) for doc, score in ranked]

