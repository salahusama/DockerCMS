import json
import requests

## DELETE /images/
## Delete a specific image
response = requests.delete("http://35.205.226.244:5000/images/new-tag", json={}).json()
print(json.dumps(response, indent=4))