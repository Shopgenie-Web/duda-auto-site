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
    return pathlib.Path(os.getenv("GMAIL_TOKEN_PATH", "gmail_token.json"))

def _get_creds():
    token_file = _token_path()
    if token_file.exists():
        return Credentials.from_authorized_user_file(token_file, SCOPES)

def gmail_service():
    creds = _get_creds()
    if not creds or not creds.valid:
        raise RuntimeError("No valid Gmail token—run /authorize once")
    return build("gmail", "v1", credentials=creds)

def send_email(to_addr, subject, html_body):
    message = MIMEText(html_body, "html")
    message["to"] = to_addr
    message["from"] = os.environ["SENDER_EMAIL"]
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    gmail_service().users().messages().send(userId="me", body={"raw": raw}).execute()

def flow_for_oauth():
    return Flow.from_client_secrets_file(
        _client_secret_path(),
        scopes=SCOPES,
        redirect_uri=os.environ.get("OAUTH_REDIRECT_URI"),
    )

def save_token(creds):
    _token_path().write_text(creds.to_json())
