"""Authentication backend."""

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.config.settings import (
    settings,
)

bearer_transport = BearerTransport(tokenUrl='auth/login')


def get_jwt_strategy() -> JWTStrategy:
    """Return JWT strategy."""
    return JWTStrategy(
        secret=settings.verification_token_secret,
        lifetime_seconds=3600,
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
