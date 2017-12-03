import json
import requests

## GET /containers
## List all containers
response = requests.get("http://35.205.226.244:5000/containers", json={}).json()
print(json.dumps(response, indent=4))