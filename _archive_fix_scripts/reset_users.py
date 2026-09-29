import requests

PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"
base_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# 1. Haquuf: Duraan jiran fudhachuu
print("⏳ Daataa users duraan jiru fudhachaa...")
get_url = f"{base_url}/users?key={API_KEY}"
res = requests.get(get_url)

if res.status_code == 200 and "documents" in res.json():
    docs = res.json()["documents"]
    print(f"🗑️ Daataa {len(docs)} haquu jalqabame...")
    for doc in docs:
        doc_id = doc['name'].split('/')[-1]
        del_url = f"{base_url}/users/{doc_id}?key={API_KEY}"
        del_res = requests.delete(del_url)
        if del_res.status_code == 200:
            print(f"   ✅ {doc_id} haqameera.")
        else:
            print(f"   ❌ {doc_id} hin haqamne.")
else:
    print("ℹ️ Daataan duraan jiru hin argamne (duwwaa dha).")

# 2. Haaraa galchuu
users_data = [
    {"id": "user_01", "name": "Admin User", "email": "admin@datapulse.com", "role": "admin", "status": "active"},
    {"id": "user_02", "name": "John Doe", "email": "john@example.com", "role": "user", "status": "active"},
    {"id": "user_03", "name": "Jane Smith", "email": "jane@example.com", "role": "user", "status": "pending"}
]

def convert_to_firestore_value(value):
    if isinstance(value, str): return {"stringValue": value}
    elif isinstance(value, bool): return {"booleanValue": value}
    elif isinstance(value, int): return {"integerValue": value}
    elif isinstance(value, float): return {"doubleValue": value}
    elif isinstance(value, list): return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict): return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

print("\n⏳ Daataa users haaraa galchuu jalqabame...")
for user in users_data:
    doc_id = user.pop("id")
    url = f"{base_url}/users/{doc_id}?key={API_KEY}"
    fields = {k: convert_to_firestore_value(v) for k, v in user.items()}
    payload = {"fields": fields}
    
    response = requests.patch(url, json=payload)
    if response.status_code == 200:
        print(f"✅ users keessatti {doc_id} galameera.")
    else:
        print(f"❌ users keessatti {doc_id} hin galamne. Dogoggora: {response.status_code}")

print("🎉 Daataa users haaraa milkaa'inaan galameera!")
