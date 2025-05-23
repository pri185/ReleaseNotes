import os
import smtplib
from email.message import EmailMessage
from docx import Document

# Read .docx content
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Config from GitHub Actions Secrets (set as environment vars)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS")  # comma-separated

if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECEIVERS):
    raise ValueError("Missing email config from environment variables!")

recipients = [email.strip() for email in EMAIL_RECEIVERS.split(",")]

# Prepare content
docx_path = "Release_Notes/Website_Release_Note.docx"
content = read_docx(docx_path)

# Email setup
msg = EmailMessage()
msg['Subject'] = '🚀 Website Release Note - Version 1.2.0'
msg['From'] = EMAIL_SENDER
msg['To'] = ", ".join(recipients)
msg.set_content(content)

# Attach the docx
with open(docx_path, 'rb') as f:
    msg.add_attachment(
        f.read(),
        maintype='application',
        subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
        filename=os.path.basename(docx_path)
    )

# Send email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"✅ Email sent to: {', '.join(recipients)}")
except smtplib.SMTPAuthenticationError as e:
    print("❌ Auth Error:", e)
except Exception as e:
    print("❌ Sending Error:", e)
