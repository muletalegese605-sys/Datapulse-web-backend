from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# CORS configuration - Firebase frontend fi local testing
CORS(app, origins=[
    "https://datapulseapp-20237.web.app",
    "https://datapulseapp-20237.firebaseapp.com",
    "http://localhost:3000",
    "http://127.0.0.1:8000"
])

# ==================== API ROUTES ====================

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    # Asitti odeeffannoo database kee irraa fidi
    return jsonify({
        "status": "success",
        "data": "Hello from backend!",
        "message": "Kun odeeffannoo backend irraa dhufe"
    })

# Yoo frontend kee endpoint biraa barbaadu, asitti dabali
@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        "status": "success",
        "message": "Dashboard data",
        "data": []
    })

# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True)
