import json
import requests

## POST /containers
## Create a new container
response = requests.post("http://35.205.226.244:5000/containers", json={"image": "34f3e9233ef9"}).json()
print(json.dumps(response, indent=4))