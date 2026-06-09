import hashlib
import hmac

from fastapi import Header, HTTPException

from app.config import settings

_TOKEN_SALT = "eva-2-admin"


def issue_token() -> str:
    """Derive a stateless bearer token from the admin password.

    Stateless (survives restarts, no storage) and changes if the password
    changes. Sufficient for the basic single-admin panel.
    """
    digest = hashlib.sha256(f"{_TOKEN_SALT}:{settings.admin_password}".encode()).hexdigest()

    return digest


def verify_password(password: str) -> bool:
    return hmac.compare_digest(password, settings.admin_password)


async def require_admin(authorization: str | None = Header(default=None)) -> None:
    expected = issue_token()
    token = ""

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    if not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")
