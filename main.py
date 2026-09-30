from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["https://datapulseapp-20237.web.app", "https://datapulse-web-backend-2.onrender.com"])
