import json
import requests

## GET /containers/<id>
## Inspect a specific container
response = requests.get("http://35.205.226.244:5000/containers/43942653c8e1", json={}).json()
print(json.dumps(response, indent=4))