import csv
from io import StringIO

from app.models import Document


class ReportingService:
    def to_csv(self, documents: list[Document]) -> str:
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(["id", "filename", "document_type", "status", "confidence", "created_at"])
        for doc in documents:
            writer.writerow([doc.id, doc.filename, doc.document_type, doc.status, doc.confidence, doc.created_at.isoformat()])
        return out.getvalue()

