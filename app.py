import os
from dotenv import load_dotenv; load_dotenv()

from flask import Flask, redirect, request, url_for
from email_helper import flow_for_oauth, save_token, send_email

app = Flask(__name__)

# set redirect URI dynamically for local vs Heroku
if "HEROKU_APP_NAME" in os.environ:
    os.environ["OAUTH_REDIRECT_URI"] = f"https://{os.environ['HEROKU_APP_NAME']}.herokuapp.com/oauth2callback"
else:
    os.environ["OAUTH_REDIRECT_URI"] = "http://127.0.0.1:5000/oauth2callback"

@app.route("/authorize")
def authorize():
    flow = flow_for_oauth()
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow = flow_for_oauth()
    flow.fetch_token(authorization_response=request.url)
    save_token(flow.credentials)
    return "✅ Gmail authorization complete. You can close this tab."
