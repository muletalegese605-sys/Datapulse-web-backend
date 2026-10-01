from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Yeroo hojii yaaluuf CORS hundaaf hayyami
CORS(app, resources={r"/*": {"origins": "*"}})

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
