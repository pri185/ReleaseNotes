import os
import json
import smtplib
from email.message import EmailMessage
from docx import Document

# --- CONFIG ---
INIT_PATH = "your_package/__init__.py"  # Update path as needed
PREV_VERSION_JSON = "prev_version.json"
DOCX_PATH = "Release_Notes/Website_Release_Note.docx"

# --- UTIL FUNCTIONS ---

def read_version_from_init(path):
    with open(path, "r") as f:
        for line in f:
            if "__version__" in line:
                return line.split("=")[1].strip().strip('"\'')
    return None

def read_previous_version(path):
    if not os.path.exists(path):
        return "0.0.0"
    with open(path, "r") as f:
        return json.load(f).get("version", "0.0.0")

def write_current_version(path, version):
    with open(path, "w") as f:
        json.dump({"version": version}, f)

def determine_update_type(prev, current):
    prev_parts = list(map(int, prev.split(".")))
    curr_parts = list(map(int, current.split(".")))

    if curr_parts[0] > prev_parts[0]:
        return "Major"
    elif curr_parts[1] > prev_parts[1]:
        return "Minor"
    elif curr_parts[2] > prev_parts[2]:
        return "Bug Fix / Patch"
    else:
        return "Unknown"

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# --- VERSION LOGIC ---
new_version = read_version_from_init(INIT_PATH)
prev_version = read_previous_version(PREV_VERSION_JSON)

if new_version == prev_version:
    print(f"⚠️ No version change detected (still {new_version}). Skipping email.")
    exit(0)

update_type = determine_update_type(prev_version, new_version)
write_current_version(PREV_VERSION_JSON, new_version)

# --- EMAIL SETUP ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS")

if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS]):
    raise ValueError("Missing email environment configuration!")

recipients = [email.strip() for email in EMAIL_RECEIVERS.split(",")]
docx_content = read_docx(DOCX_PATH)

# Compose email
email_body = f"""🚀 A new release has been deployed!

🆕 Version: {new_version}
🔄 Update Type: {update_type}

📄 Release Notes:
{docx_content}

We'd love your feedback or thoughts!
"""

msg = EmailMessage()
msg['Subject'] = f'🚀 Website Release Note - Version {new_version}'
msg['From'] = EMAIL_SENDER
msg['To'] = ", ".join(recipients)
msg.set_content(email_body)

# Attach the docx
with open(DOCX_PATH, 'rb') as f:
    msg.add_attachment(
        f.read(),
        maintype='application',
        subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
        filename=os.path.basename(DOCX_PATH)
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
