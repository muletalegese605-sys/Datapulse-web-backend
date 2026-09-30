import requests

PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"
base_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# 1. Adminoota shan gahee hojii adda addaa qaban
admins_data = [
    {
        "id": "admin_uid_03", 
        "name": "Super Admin", 
        "email": "superadmin@datapulse.com", 
        "role": "super_admin", 
        "permissions": ["all_access", "manage_users", "manage_admins", "view_reports"],
        "status": "active"
    },
    {
        "id": "admin_uid_04", 
        "name": "Content Manager", 
        "email": "content@datapulse.com", 
        "role": "content_manager", 
        "permissions": ["manage_features", "manage_categories", "manage_settings"],
        "status": "active"
    },
    {
        "id": "admin_uid_05", 
        "name": "Data Analyst", 
        "email": "analyst@datapulse.com", 
        "role": "data_analyst", 
        "permissions": ["view_records", "view_datasets", "export_data"],
        "status": "active"
    },
    {
        "id": "admin_uid_06", 
        "name": "User Manager", 
        "email": "usermanager@datapulse.com", 
        "role": "user_manager", 
        "permissions": ["manage_users", "manage_subscriptions", "view_user_data"],
        "status": "active"
    },
    {
        "id": "admin_uid_07", 
        "name": "Support Agent", 
        "email": "support@datapulse.com", 
        "role": "support_agent", 
        "permissions": ["view_audits", "resolve_queries", "view_user_data"],
        "status": "active"
    }
]

def convert_to_firestore_value(value):
    if isinstance(value, str): return {"stringValue": value}
    elif isinstance(value, bool): return {"booleanValue": value}
    elif isinstance(value, int): return {"integerValue": value}
    elif isinstance(value, float): return {"doubleValue": value}
    elif isinstance(value, list): return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict): return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

print("⏳ Adminoota shan galchuu jalqabame...")
for admin in admins_data:
    doc_id = admin.pop("id")
    url = f"{base_url}/admins/{doc_id}?key={API_KEY}"
    
    fields = {k: convert_to_firestore_value(v) for k, v in admin.items()}
    payload = {"fields": fields}
    
    response = requests.patch(url, json=payload)
    
    if response.status_code == 200:
        print(f"✅ admins keessatti {doc_id} galameera (Gahee: {admin.get('role')}).")
    else:
        print(f"❌ admins keessatti {doc_id} hin galamne. Dogoggora: {response.status_code}")
        print(f"   Ibsa: {response.text}")

print("🎉 Adminootni shan milkaa'inaan galameera!")
