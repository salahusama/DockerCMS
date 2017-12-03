












## POST /containers
## Create a new container
response = requests.post("http://35.205.226.244:5000/containers", json={"image": "34f3e9233ef9"}).json()
print(json.dumps(response, indent=4))

## PATCH /containers/
## Change a container's state
response = requests.patch("http://35.205.226.244:5000/containers/127201ecd52f", json={"state": "stopped"}).json()
print(json.dumps(response, indent=4))

## PATCH /images/
## Change a specific image's attributes
response = requests.patch("http://35.205.226.244:5000/images/34f3e9233ef9", json={"tag": "new-tag"}).json()
print(json.dumps(response, indent=4))

## DELETE /containers/
## Delete a specific container
response = requests.delete("http://35.205.226.244:5000/containers/45f9fa3af89a", json={}).json()
print(json.dumps(response, indent=4))

## DELETE /containers
## Delete all containers (including running)
response = requests.delete("http://35.205.226.244:5000/containers", json={}).json()
print(json.dumps(response, indent=4))

## DELETE /images/
## Delete a specific image
response = requests.delete("http://35.205.226.244:5000/images/new-tag", json={}).json()
print(json.dumps(response, indent=4))

## DELETE /images
## Delete all images
response = requests.delete("http://35.205.226.244:5000/images", json={}).json()
print(json.dumps(response, indent=4))