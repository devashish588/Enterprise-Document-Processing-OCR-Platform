from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.schemas.document import DocumentOut, SearchResult
from app.services.search import SearchEngine

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
def search(
    q: str = Query(min_length=1),
    document_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(current_user),
):
    docs = DocumentRepository(db).search(q, limit=limit * 4)
    if document_type:
        docs = [d for d in docs if d.document_type == document_type]
    if status:
        docs = [d for d in docs if d.status == status]
    ranked = SearchEngine().rank(q, docs)
    return [
        SearchResult(document=DocumentOut.model_validate(doc), score=score, snippet=snippet)
        for doc, score, snippet in ranked[:limit]
    ]
