from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import json
import os
from typing import Any


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or _b64(os.urandom(16))
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"pbkdf2_sha256${salt}${_b64(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    parts = password_hash.split("$", 2)
    if len(parts) != 3 or parts[0] != "pbkdf2_sha256":
        return False
    _, salt, digest = parts
    candidate = hash_password(password, salt).split("$", 2)[2]
    return hmac.compare_digest(candidate, digest)


def _sign(secret: str, signing_input: str) -> str:
    mac = hmac.HMAC(secret.encode(), signing_input.encode(), hashlib.sha256)
    return _b64(mac.digest())


def create_access_token(subject: str, secret: str, minutes: int, claims: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    payload.update(claims or {})
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = (
        f"{_b64(json.dumps(header, separators=(',', ':')).encode())}"
        f".{_b64(json.dumps(payload, separators=(',', ':')).encode())}"
    )
    return f"{signing_input}.{_sign(secret, signing_input)}"


def decode_access_token(token: str, secret: str) -> dict[str, Any]:
    parts = token.split(".", 2)
    if len(parts) != 3:
        raise ValueError("malformed token")
    header_b64, payload_b64, signature_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}"
    if not hmac.compare_digest(_sign(secret, signing_input), signature_b64):
        raise ValueError("invalid token signature")
    payload = json.loads(_unb64(payload_b64))
    if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("token expired")
    return payload
