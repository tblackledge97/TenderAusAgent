# Creates and sends a email
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# email configuation
SENDER_EMAIL = "t.blackledge97@gmail.com"
APP_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "465"

if not APP_PASSWORD:
    raise ValueError("APP_PASSWORD enviroment variable is not set.")


def build_email_body(opportunities):
    """Builds formatted text for email body."""
    email_body = ""
    for opp in opportunities:
        email_body += f"Title: {opp['title']}\n"
        email_body += f"Link: {opp['link']}\n"
        email_body += f"Description: {opp['description']}\n"
        email_body += f"Keywords: {opp['matched_keywords']}\n"
        email_body += f"score: {opp['total_score']}\n"
        email_body += "=" * 20 + "\n"
    return email_body


def send_email(subject, body, to_email):
    """Sends an email via the SMTP server."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        print("Email sent")
    except Exception as e:
        print(f"Failed to send email: {e}")
