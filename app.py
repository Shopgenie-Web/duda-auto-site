from dotenv import load_dotenv
load_dotenv()           # ← reads .env into os.environ

from flask import Flask
app = Flask(__name__)