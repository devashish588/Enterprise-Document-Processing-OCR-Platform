from typing import Generic, TypeVar
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class Repository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]):
        self.db = db
        self.model = model

    def get(self, entity_id: int) -> ModelT | None:
        return self.db.get(self.model, entity_id)

    def list(self, limit: int = 50, offset: int = 0) -> list[ModelT]:
        return list(self.db.query(self.model).offset(offset).limit(limit))

    def add(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

