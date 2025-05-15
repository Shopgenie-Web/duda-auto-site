import os, json, base64, pathlib, tempfile
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def _client_secret_path():
    if os.getenv("GMAIL_CLIENT_SECRET_JSON"):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp.write(os.environ["GMAIL_CLIENT_SECRET_JSON"].encode())
        tmp.close()
        return tmp.name
    return os.getenv("GMAIL_CLIENT_SECRET")

def _token_path():
    # use tmp on Heroku, file on local dev
    return pathlib.Path(os.getenv("GMAIL_TOKEN_PATH", "/tmp/gmail_token.json"))

def _ensure_token_file():
    token_file = _token_path()
    if token_file.exists():
        return token_file
    # If token missing but JSON is in env, write it
    if os.getenv("GMAIL_TOKEN_JSON"):
        token_file.write_text(os.environ["GMAIL_TOKEN_JSON"])
        return token_file
    return None

def gmail_service():
    token_file = _ensure_token_file()
    if not token_file:
        raise RuntimeError("No Gmail token—run /authorize once")
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    return build("gmail", "v1", credentials=creds)

def send_email(to_addr, subject, html_body):
    message = MIMEText(html_body, "html")
    message["to"] = to_addr
    message["from"] = os.environ["SENDER_EMAIL"]
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    gmail_service().users().messages().send(userId="me", body={"raw": raw}).execute()
