import json
import requests

## PATCH /images/
## Change a specific image's attributes
response = requests.patch("http://35.205.226.244:5000/images/34f3e9233ef9", json={"tag": "new-tag"}).json()
print(json.dumps(response, indent=4))