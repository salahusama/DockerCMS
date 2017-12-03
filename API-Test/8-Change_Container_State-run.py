import json
import requests

## PATCH /containers/
## Change a container's state
response = requests.patch("http://35.205.226.244:5000/containers/127201ecd52f", json={"state": "stopped"}).json()
print(json.dumps(response, indent=4))