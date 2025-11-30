from app.celery_worker import celery_app
from  app.utils.email import send_email, env
from celery.canvas import Signature
from datetime import datetime
import asyncio

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email_task(to: str, code: str, user_name: str):
    subject = "Your verification code"
    name_part = user_name.split()[0] if user_name else "there"
    
    html = env.get_template("verify_email.html").render(
        name=name_part,
        verification_code=" ".join(code[i:i+3] for i in range(0, len(code), 3)),  # 123 456
        expires_in_minutes=10,
        year=datetime.now().year,
    )
    text = env.get_template("verify_email.txt").render(
        name=name_part,
        verification_code=code.replace(" ", ""),
        expires_in_minutes=10,
    )
    
    # run the async send_email inside the worker's event loop
    asyncio.get_event_loop().run_until_complete(
        send_email(subject=subject, email_to=to, html=html, text=text)
    )
    
send_verification_email_task: Signature = send_verification_email_task

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(to: str, reset_link: str, user_name: str):
    subject = "Reset your password"
    name_part = user_name.split()[0] if user_name else "there"
    
    html = env.get_template("password_reset.html").render(
        name=name_part,
        reset_link=reset_link,
        expires_in_minutes=30,
        year=datetime.now().year,
    )
    text = env.get_template("password_reset.txt").render(
        name=name_part,
        reset_link=reset_link,
        expires_in_minutes=30,
    )
    
    asyncio.get_event_loop().run_until_complete(
        send_email(subject=subject, email_to=to, html=html, text=text)
    )
    
send_password_reset_email_task: Signature = send_password_reset_email_task