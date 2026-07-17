from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models import Document, User
from app.repositories.documents import DocumentRepository
from app.schemas.document import DocumentDetail, DocumentOut
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


def to_detail(doc: Document) -> DocumentDetail:
    return DocumentDetail(
        id=doc.id,
        filename=doc.filename,
        document_type=doc.document_type,
        status=doc.status,
        confidence=doc.confidence,
        created_at=doc.created_at,
        ocr_text=doc.ocr_result.text if doc.ocr_result else None,
        fields=doc.fields,
        validations=doc.validations,
    )


@router.post("", response_model=DocumentOut, status_code=201)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")
    return DocumentService(db).ingest_bytes(file.filename or "document.bin", file.content_type or "application/octet-stream", data, user.email)


@router.get("", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return DocumentRepository(db).list(limit=100)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    doc = DocumentRepository(db).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return to_detail(doc)

