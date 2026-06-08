import asyncio
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import get_settings


async def send_email(subject: str, to: str, body: str, html: Optional[str] = None) -> None:
    """Send an email using configured SMTP settings. Runs SMTP in a thread to avoid blocking."""
    settings = get_settings()

    if not settings.smtp_host or not settings.smtp_from:
        # no-op if SMTP not configured
        return

    def _send():
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.smtp_from
        msg["To"] = to
        if html:
            msg.set_content(body)
            msg.add_alternative(html, subtype="html")
        else:
            msg.set_content(body)

        host = settings.smtp_host
        port = settings.smtp_port or 587
        username = settings.smtp_username
        password = settings.smtp_password

        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            server.starttls()

        try:
            if username and password:
                server.login(username, password)
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                pass

    await asyncio.to_thread(_send)
