import json
import requests

## GET /images
## List all images
response = requests.get("http://35.205.226.244:5000/images", json={}).json()
print(json.dumps(response, indent=4))