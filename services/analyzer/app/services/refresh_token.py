import hashlib
import secrets


def create_refresh_token() -> tuple[str, str]:
    """Create a refresh token."""

    token = secrets.token_urlsafe(64)

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    return token, token_hash


def hash_refresh_token(token: str) -> str:
    """Hash a refresh token."""

    return hashlib.sha256(token.encode()).hexdigest()
