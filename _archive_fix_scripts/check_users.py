import requests
import json

PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"

# URL'a users collection
url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users?key={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if "documents" in data:
        print(f"✅ Daataan users keessa jiru: {len(data['documents'])}")
        for doc in data['documents']:
            doc_id = doc['name'].split('/')[-1]
            fields = doc.get('fields', {})
            # Maqaa fi email agarsiisuuf
            name = fields.get('name', {}).get('stringValue', 'N/A')
            email = fields.get('email', {}).get('stringValue', 'N/A')
            print(f"   - ID: {doc_id} | Name: {name} | Email: {email}")
    else:
        print("❌ Daataan users keessa hin jiru (duwwaa dha).")
else:
    print(f"❌ Dogoggora: {response.status_code} - {response.text}")
