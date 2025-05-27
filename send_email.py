import os
import json
import smtplib
import html
from email.message import EmailMessage
from docx import Document
from datetime import datetime, timezone, timedelta

# --- CONFIG ---
INIT_PATH = "__init__.py"
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
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"❌ Failed to read DOCX: {e}")
        return "(Could not read release note.)"

def get_current_ist_time():
    IST = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")


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
    raise ValueError("❌ Missing email environment configuration!")

recipients = [email.strip() for email in EMAIL_RECEIVERS.split(",")]
docx_content = read_docx(DOCX_PATH)
escaped_content = html.escape(docx_content).replace("\n", "<br>")
release_date = get_current_ist_time()

# Compose HTML email
html_intro = f"""
<b>🚀 New Website Release Deployed!</b><br><br>
<b>🆕 Version:</b> {new_version}<br>
<b>🔄 Update Type:</b> {update_type}<br>
<b>🗓️ Release Date:</b> {release_date}<br><br>
<b>📄 Release Notes:</b><br>
"""
email_body = html_intro + escaped_content

# Compose EmailMessage
msg = EmailMessage()
msg['Subject'] = f'🚀 Website Release Note - Version {new_version}'
msg['From'] = EMAIL_SENDER
msg['To'] = ", ".join(recipients)

# Add plain text fallback + HTML version
msg.set_content("This email contains release notes. Please use an HTML-capable email client.")
msg.add_alternative(email_body, subtype='html')

# Attach the docx
try:
    with open(DOCX_PATH, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=os.path.basename(DOCX_PATH)
        )
    print("📎 Attached DOCX release note.")
except Exception as e:
    print(f"❌ Failed to attach DOCX: {e}")

# Send email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"✅ Email sent to: {', '.join(recipients)}")
except smtplib.SMTPAuthenticationError as e:
    print("❌ Authentication Error:", e)
except Exception as e:
    print("❌ Sending Error:", e)
