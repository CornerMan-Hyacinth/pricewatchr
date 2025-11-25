from fastapi import BackgroundTasks

async def send_verification_email(to: str, code: str, background_tasks: BackgroundTasks):
    # Use Resend on prod
    print(f"[EMAIL] To: {to} | Verification code: {code}")