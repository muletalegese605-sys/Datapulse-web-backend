from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/*": {"origins": [
    "https://datapulseapp-20237.web.app",
    "https://datapulseapp-20237.firebaseapp.com",
    "http://localhost:3000",
    "http://127.0.0.1:8000"
]}})

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        "status": "success",
        "data": "Hello from backend!",
        "message": "Kun odeeffannoo backend irraa dhufe"
    })

if __name__ == '__main__':
    app.run(debug=True)
