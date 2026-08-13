from flask_mail import Message
from flask import current_app
from extensions import mail


def send_reset_email(recipient_email, reset_link):
    subject = "Password Reset Request"

    body = f"""
Hello,

A password reset was requested for your account.

Click the link below to reset your password:

{reset_link}

This link will expire in 30 minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
IT Support
"""

    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        body=body
    )

    mail.send(msg)