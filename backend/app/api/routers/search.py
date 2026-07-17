from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.schemas.document import DocumentOut, SearchResult
from app.services.search import SearchEngine

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
def search(q: str = Query(min_length=1), db: Session = Depends(get_db), _=Depends(current_user)):
    docs = DocumentRepository(db).search(q, limit=100)
    return [SearchResult(document=DocumentOut.model_validate(doc), score=score, snippet=snippet) for doc, score, snippet in SearchEngine().rank(q, docs)]

