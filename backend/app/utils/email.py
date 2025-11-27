from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.utils.config.settings import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASS,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

fm = FastMail(mail_config)

async def send_email(subject: str, email_to: str, body: str, text: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
        text=text
    )
    await fm.send_message(message)