import json
import requests

## GET /containers/<id>/logs
## Dump specific container logs
response = requests.get("http://35.205.226.244:5000/containers/45f9fa3af89a/logs", json={}).json()
print(json.dumps(response, indent=4))