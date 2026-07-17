from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models import Document

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), _=Depends(current_user)):
    by_type = db.query(Document.document_type, func.count(Document.id)).group_by(Document.document_type).all()
    by_status = db.query(Document.status, func.count(Document.id)).group_by(Document.status).all()
    return {"by_type": dict(by_type), "by_status": dict(by_status), "total": db.query(Document).count()}

