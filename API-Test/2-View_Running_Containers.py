import json
import requests

## GET /containers?state=running
## List running containers (only)
response = requests.get("http://35.205.226.244:5000/containers?state=running", json={}).json()
print(json.dumps(response, indent=4))