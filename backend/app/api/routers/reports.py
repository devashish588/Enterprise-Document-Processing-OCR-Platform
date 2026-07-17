from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.services.reporting import ReportingService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/documents.csv")
def export_documents(db: Session = Depends(get_db), _=Depends(current_user)):
    csv_data = ReportingService().to_csv(DocumentRepository(db).list(limit=10_000))
    return Response(csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=documents.csv"})

