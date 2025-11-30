from jinja2 import Environment, FileSystemLoader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.utils.config.find_dir import find_dir
from app.utils.config.settings import settings

TEMPLATES_DIR = find_dir(dir_name="templates")

# Jinja setup
env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True
)

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

async def send_email(subject: str, email_to: str, html: str, text: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html,
        subtype="html",
        text=text
    )
    await fm.send_message(message)