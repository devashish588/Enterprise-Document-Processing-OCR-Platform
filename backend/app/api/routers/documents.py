from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import current_user, require_role
from app.db.session import get_db
from app.models import Document, User
from app.repositories.documents import DocumentRepository
from app.schemas.document import DocumentDetail, DocumentOut
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])

_MAX_FILE_BYTES = 50 * 1024 * 1024  # 50 MB


def _to_detail(doc: Document) -> DocumentDetail:
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
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(data) > _MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 50 MB limit")
    return DocumentService(db).ingest_bytes(
        file.filename or "document.bin",
        file.content_type or "application/octet-stream",
        data,
        user.email,
    )


@router.get("", response_model=list[DocumentOut])
def list_documents(
    document_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(current_user),
):
    return DocumentRepository(db).list_filtered(document_type=document_type, status=status, limit=limit, offset=offset)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    doc = DocumentRepository(db).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return _to_detail(doc)


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin", "manager")),
):
    repo = DocumentRepository(db)
    doc = repo.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    repo.delete(doc)
