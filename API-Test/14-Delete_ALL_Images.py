import json
import requests

## DELETE /images
## Delete all images
response = requests.delete("http://35.205.226.244:5000/images", json={}).json()
print(json.dumps(response, indent=4))