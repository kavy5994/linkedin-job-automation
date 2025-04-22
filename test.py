import requests

# Airtable credentials
AIRTABLE_API_KEY = "patTL096O7kNGtYdN.7c7b2a8fa60ebb9e569e881bd6642311f2f0481ba9efb6151f02b45ea1405098"
AIRTABLE_BASE_ID = "appLIhUJQf5qhcsmD"
AIRTABLE_TABLE_NAME = "job_application"

# Airtable API URL
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch records from Airtable
def fetch_records():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None

# Example usage
data = fetch_records()
if data:
    print(data)
