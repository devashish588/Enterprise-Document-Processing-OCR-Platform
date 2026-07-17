from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.services.reporting import ReportingService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/documents.csv")
def export_csv(db: Session = Depends(get_db), _=Depends(current_user)):
    data = ReportingService().to_csv(DocumentRepository(db).list(limit=10_000))
    return Response(data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=documents.csv"})


@router.get("/documents.xlsx")
def export_excel(db: Session = Depends(get_db), _=Depends(current_user)):
    data = ReportingService().to_excel(DocumentRepository(db).list(limit=10_000))
    return Response(
        data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=documents.xlsx"},
    )
