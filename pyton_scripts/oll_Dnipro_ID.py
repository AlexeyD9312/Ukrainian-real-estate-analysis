import requests
import json
import time

API_KEY = "tBpXw0JFJHFL5gbyB0h1WP6ax6ZpmtnjhsQrVXgf"
URL = "https://developers.ria.com/dom/search"

params = {
    "api_key": API_KEY,
    "category":1,
    "operation":1,
    "state_id":11,
    "city_id":11,
    "page":0
}
response = requests.get(URL,params=params)

if response.status_code == 200:
    data = response.json()
    total_count = data["count"]
    total_pages = (total_count//100) + (1 if total_count % 100 !=0 else 0)
    all_ID = data["items"]
    print(f"I see count : {total_count},download {total_pages} pages ")
else:
    print(f'Error {response.status_code}:{response.text}')
    exit()

for page in range(1,total_pages):
    API_KEY = "tBpXw0JFJHFL5gbyB0h1WP6ax6ZpmtnjhsQrVXgf"
    URL = "https://developers.ria.com/dom/search"

    params = {
        "api_key": API_KEY,
        "category": 1,
        "operation": 1,
        "state_id": 11,
        "city_id": 11,
        "page": page
    }
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        all_ID.extend(data["items"])
        print(f"Page {page} download, ID: {len(data['items'])}")
    else:
        print(f'Error in {page} page , {response.status_code} ')
    time.sleep(1)

with open("All_ID_Dnipro","w") as f:
    json.dump(all_ID,f)
print(f"Download {len(all_ID)} ID in Json")

