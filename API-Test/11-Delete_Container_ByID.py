import json
import requests

## DELETE /containers/
## Delete a specific container
response = requests.delete("http://35.205.226.244:5000/containers/45f9fa3af89a", json={}).json()
print(json.dumps(response, indent=4))