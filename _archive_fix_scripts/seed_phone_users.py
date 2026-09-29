import requests

PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"
base_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# Fayyadamtoota haaraa (Phone fi Email qaban)
phone_users = [
    {"id": "user_09", "name": "Kebede Tesfaye", "email": "kebede@example.com", "phone": "+251911223344", "role": "user", "status": "active"},
    {"id": "user_10", "name": "Amina Yusuf", "email": "amina@example.com", "phone": "+251922334455", "role": "user", "status": "active"},
    {"id": "user_11", "name": "John Smith", "email": "john.smith@global.com", "phone": "+14155552671", "role": "user", "status": "active"},
    {"id": "user_12", "name": "Fatima Al-Sayed", "email": "fatima@global.com", "phone": "+971501234567", "role": "user", "status": "active"}
]

def convert_to_firestore_value(value):
    if isinstance(value, str): return {"stringValue": value}
    elif isinstance(value, bool): return {"booleanValue": value}
    elif isinstance(value, int): return {"integerValue": value}
    elif isinstance(value, float): return {"doubleValue": value}
    elif isinstance(value, list): return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict): return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

print("⏳ Fayyadamtoota Phone qaban galchuu jalqabame...")
for user in phone_users:
    doc_id = user.pop("id")
    url = f"{base_url}/users/{doc_id}?key={API_KEY}"
    
    fields = {k: convert_to_firestore_value(v) for k, v in user.items()}
    payload = {"fields": fields}
    
    response = requests.patch(url, json=payload)
    if response.status_code == 200:
        print(f"✅ users keessatti {doc_id} galameera ({user.get('phone')}).")
    else:
        print(f"❌ users keessatti {doc_id} hin galamne. Dogoggora: {response.status_code}")

print("🎉 Fayyadamtoonni Phone qaban milkaa'inaan galameera!")
