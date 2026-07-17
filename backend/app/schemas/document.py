from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "analyst"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
    created_at: datetime


class FieldOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: str
    confidence: float


class ValidationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    field_name: str
    severity: str
    message: str


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    document_type: str
    status: str
    confidence: float
    created_at: datetime


class DocumentDetail(DocumentOut):
    ocr_text: str | None = None
    fields: list[FieldOut] = []
    validations: list[ValidationOut] = []


class SearchResult(BaseModel):
    document: DocumentOut
    score: float
    snippet: str
