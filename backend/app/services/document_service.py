from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import AuditLog, Document, ExtractedField, OCRResult, ValidationIssue
from app.repositories.documents import AuditRepository, DocumentRepository, FieldRepository, OCRRepository, ValidationRepository
from app.services.classification import DocumentClassifier
from app.services.extraction import FieldExtractor
from app.services.ocr import OCREngine
from app.services.preprocessing import ImagePreprocessor
from app.services.validation import ValidationEngine


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.documents = DocumentRepository(db)
        self.ocr_results = OCRRepository(db)
        self.fields = FieldRepository(db)
        self.validations = ValidationRepository(db)
        self.audit = AuditRepository(db)
        self.settings = get_settings()

    def ingest_bytes(self, filename: str, content_type: str, data: bytes, actor: str = "system") -> Document:
        safe_name = Path(filename).name
        path = self.settings.upload_dir / f"{uuid4().hex}_{safe_name}"
        path.write_bytes(data)

        doc = self.documents.add(Document(filename=safe_name, content_type=content_type, storage_path=str(path)))
        processed = ImagePreprocessor().preprocess(path)
        ocr = OCREngine().extract(processed)
        classification = DocumentClassifier().classify(ocr.text)
        extracted = FieldExtractor().extract(classification.label, ocr.text)
        issues = ValidationEngine().validate(classification.label, extracted)

        doc.document_type = classification.label
        doc.status = "needs_review" if issues else "processed"
        doc.confidence = min(ocr.confidence, classification.confidence)
        self.ocr_results.add(OCRResult(document_id=doc.id, engine=ocr.engine, text=ocr.text, confidence=ocr.confidence))
        for name, (value, confidence) in extracted.items():
            self.fields.add(ExtractedField(document_id=doc.id, name=name, value=value, confidence=confidence))
        for issue in issues:
            self.validations.add(ValidationIssue(document_id=doc.id, field_name=issue.field_name, severity=issue.severity, message=issue.message))
        self.audit.add(AuditLog(actor=actor, action="document.ingested", entity_type="document", entity_id=str(doc.id)))
        self.db.commit()
        self.db.refresh(doc)
        return doc

