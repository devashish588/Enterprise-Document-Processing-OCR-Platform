import csv
from io import BytesIO, StringIO

from app.models import Document


class ReportingService:
    _COLUMNS = ["id", "filename", "document_type", "status", "confidence", "created_at"]

    def _rows(self, documents: list[Document]) -> list[list]:
        return [[doc.id, doc.filename, doc.document_type, doc.status, doc.confidence, doc.created_at.isoformat()] for doc in documents]

    def to_csv(self, documents: list[Document]) -> str:
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(self._COLUMNS)
        writer.writerows(self._rows(documents))
        return out.getvalue()

    def to_excel(self, documents: list[Document]) -> bytes:
        import pandas as pd

        df = pd.DataFrame(self._rows(documents), columns=self._COLUMNS)
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Documents")
        return buf.getvalue()
