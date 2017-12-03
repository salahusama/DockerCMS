import json
import requests

## POST /images
## Create a new image
response = requests.post("http://35.205.226.244:5000/images", files={'file': open('Dockerfile','rb')}).json()
print(response)