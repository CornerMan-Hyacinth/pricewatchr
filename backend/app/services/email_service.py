from fastapi import BackgroundTasks

async def send_verification_email(to: str, code: str, background_tasks: BackgroundTasks):
    # Use Resend on prod
    print(f"[EMAIL] To: {to} | Verification code: {code}")
    
async def send_password_reset_email(to: str, reset_link: str, user_name: str, background_tasks: BackgroundTasks):
    print(f"[EMAIL] To: {to} | Verification reset link: {reset_link}")