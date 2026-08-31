"""Email service."""

from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
)

from app.config.settings import (
    settings,
)

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.email_user,
    MAIL_PASSWORD=settings.email_password,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_host,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)

async def send_verification_email(
    email: str,
    token: str,
) -> None:
    """Send verification email."""

    verification_url = (
        f'{settings.email_verification_url}?token={token}'
    )

    message = MessageSchema(
        subject='Подтверждение учетной записи в NeuroHunter',
        recipients=[email],
        body=(
            "Здравствуйте!\n\n"
            "Для подтверждения регистрации перейдите по ссылке:\n\n"
            f"{verification_url}\n\n"
            "Ссылка действительна 24 часа."
        ),
        subtype=MessageType.plain,
    )

    fast_mail = FastMail(mail_config)

    await fast_mail.send_message(message)
