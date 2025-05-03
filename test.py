import requests
from urllib.parse import quote

url = "https://opendata.myswitzerland.io/v1/destinations"
headers = {
    "x-api-key": "jp8qBDqD7HaPZz1XsSmD7W03Zm1RoWj9I9Js5Nai"
}
params = {
    "lang": "en",
    "limit": 5,
    "query": quote("Zermatt")  # Example destination
}

response = requests.get(url, headers=headers, params=params)

print("Status Code:", response.status_code)
print("\nResponse:")
print(response.json())
