from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models import User
from app.schemas.document import TokenRequest, TokenResponse, UserCreate, UserOut
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = AuthService(db).register(payload.email, payload.password, payload.role)
    token = AuthService(db).login(payload.email, payload.password)
    return TokenResponse(access_token=token or "")


@router.post("/login", response_model=TokenResponse)
def login(payload: TokenRequest, db: Session = Depends(get_db)):
    token = AuthService(db).login(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
