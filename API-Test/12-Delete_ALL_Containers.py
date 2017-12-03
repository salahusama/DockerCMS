import json
import requests

## DELETE /containers
## Delete all containers (including running)
response = requests.delete("http://35.205.226.244:5000/containers", json={}).json()
print(json.dumps(response, indent=4))