from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.documents import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)
        self.settings = get_settings()

    def register(self, email: str, password: str, role: str = "analyst") -> User:
        existing = self.users.by_email(email)
        if existing:
            return existing
        return self.users.add(User(email=email.lower(), password_hash=hash_password(password), role=role))

    def login(self, email: str, password: str) -> str | None:
        user = self.users.by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return create_access_token(str(user.id), self.settings.secret_key, self.settings.access_token_minutes, {"role": user.role, "email": user.email})

