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
    avg_confidence = db.query(func.avg(Document.confidence)).scalar() or 0.0
    recent = (
        db.query(func.date(Document.created_at), func.count(Document.id))
        .group_by(func.date(Document.created_at))
        .order_by(func.date(Document.created_at))
        .limit(30)
        .all()
    )
    return {
        "total": db.query(Document).count(),
        "by_type": dict(by_type),
        "by_status": dict(by_status),
        "avg_confidence": round(float(avg_confidence), 4),
        "daily_trend": [{"date": str(date), "count": count} for date, count in recent],
    }
