import json

def load_email_credentials(path="email_credentials.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data["EMAIL_SENDER"], data["EMAIL_PASSWORD"]
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load email credentials: {e}")

def load_email_receivers(path="email_receivers.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data.get("receivers", [])
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load email receivers: {e}")
