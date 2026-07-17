from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import AuditLog, Document, ExtractedField, OCRResult, User, ValidationIssue
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).one_or_none()


class DocumentRepository(Repository[Document]):
    def __init__(self, db: Session):
        super().__init__(db, Document)

    def search(self, query: str, limit: int = 25) -> list[Document]:
        term = f"%{query}%"
        return (
            self.db.query(Document)
            .outerjoin(OCRResult)
            .filter(or_(Document.filename.ilike(term), OCRResult.text.ilike(term)))
            .limit(limit)
            .all()
        )


class OCRRepository(Repository[OCRResult]):
    def __init__(self, db: Session):
        super().__init__(db, OCRResult)


class FieldRepository(Repository[ExtractedField]):
    def __init__(self, db: Session):
        super().__init__(db, ExtractedField)


class ValidationRepository(Repository[ValidationIssue]):
    def __init__(self, db: Session):
        super().__init__(db, ValidationIssue)


class AuditRepository(Repository[AuditLog]):
    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

