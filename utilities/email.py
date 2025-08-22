import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.config import EMAIL_HOST, EMAIL_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to: str, subject: str, body: str = None, otp: str = None, name: str = None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    # Format body with name if provided
    if otp:
        body = f"""
Hi {name or to.split('@')[0].title()},
Your OTP is: {otp}

This code will expire in 10 minutes. Please don’t share it.

Thanks,
Church Attendance Team
        """
    elif name:
        body = f"""
Hi {name},

{body}

Thanks,
Church Attendance Team
        """

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")
