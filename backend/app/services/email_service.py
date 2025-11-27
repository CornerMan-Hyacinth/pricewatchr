from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.utils.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASS,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

async def send_verification_email(to: str, code: str, background_tasks: BackgroundTasks):
    
    print(f"[EMAIL] To: {to} | Verification code: {code}")
    
async def send_password_reset_email(to: str, reset_link: str, user_name: str, background_tasks: BackgroundTasks):
    print(f"[EMAIL] To: {to} | Verification reset link: {reset_link}")