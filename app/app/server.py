from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
	return """
	<h2>Available API endpoints:</h2>

	<table>
		<tr><td>GET /containers</td><td>List all containers</td></tr>
		<tr><td>GET /containers?state=running</td><td>List running containers (only)</td></tr>
		<tr><td>GET /containers/<id></td><td>Inspect a specific container</td></tr>
		<tr><td>GET /containers/<id>/logs</td><td>Dump specific container logs</td></tr>
		<tr><td>GET /images</td><td>List all images</td></tr>


		<tr><td>POST /images</td><td>Create a new image</td></tr>
		<tr><td>POST /containers</td><td>Create a new container</td></tr>

		<tr><td>PATCH /containers/<id></td><td>Change a container's state</td></tr>
		<tr><td>PATCH /images/<id></td><td>Change a specific image's attributes</td></tr>

		<tr><td>DELETE /containers/<id></td><td>Delete a specific container</td></tr>
		<tr><td>DELETE /containers</td><td>Delete all containers (including running)</td></tr>
		<tr><td>DELETE /images/<id></td><td>Delete a specific image</td></tr>
		<tr><td>DELETE /images</td><td>Delete all images</td></tr>
	</table>
	"""

@app.route('/containers', methods=['GET'])
def containers_index():
	"""
	List all containers

	curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
	curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool

	"""
	if request.args.get('state') == 'running':
		output = docker('ps')
		resp = json.dumps(docker_ps_to_array(output))

	else:
		output = docker('ps', '-a')
		resp = json.dumps(docker_ps_to_array(output))

	#resp = ''
	return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['GET'])
def images_index():
	"""
	List all images

	Complete the code below generating a valid response.
	"""
	output = docker('images')
	resp = json.dumps(docker_images_to_array(output))

	return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
	"""
	Inspect specific container

	"""
	condition = 'id=' + str(id)
	output = docker('ps', '-f', condition)
	resp = json.dumps(docker_ps_to_array(output))

	return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
	"""
	Dump specific container logs

	"""
	output = docker('logs', id)
	resp = json.dumps(docker_ps_to_array(output))

	return Response(response=resp, mimetype="application/json")


@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
	"""
	Delete a specific image
	"""
	docker ('rmi', id)
	resp = '{"id": "%s"}' % id

	return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
	"""
	Delete a specific container - must be already stopped/killed

	"""
	docker ('rm', id)
	resp = '{"id": "%s"}' % id

	return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
	"""
	Force remove all containers - dangrous!
	"""

	output = docker('ps', '-a')
	containers = docker_ps_to_array(output)

	all = []
	removed = {"removed": []}

	for obj in containers:
		id = obj['id']
		docker('rm', '--force', id)
		removed["removed"].append(id)

	all.append(removed)
	resp = json.dumps(all)

	return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['DELETE'])
def images_remove_all():
	"""
	Force remove all images - dangrous!

	"""
	output = docker('images')
	images = docker_images_to_array(output)

	all = []
	removed = {"removed": []}

	for obj in images:
		id = obj['id']
		docker('rmi', id)
		removed["removed"].append(id)

	all.append(removed)
	resp = json.dumps(all)
	return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['POST'])
def containers_create():
	"""
	Create container (from existing image using id or name)

	curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "my-app"}'
	curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e"}'
	curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e","publish":"8081:22"}'

	"""
	body = request.get_json(force=True)
	image = body['image']
	args = ('run', '-d')
	id = docker(*(args + (image,)))[0:12]
	return Response(response='{"id": "%s"}' % id, mimetype="application/json")

@app.route('/images', methods=['POST'])
def images_create():
	"""
	Create image (from uploaded Dockerfile)

	curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images

	"""
	resp = json.dumps("{'complete': 'false'}")
	dockerfile = request.files['file']
	if dockerfile:
		filename = secure_filename(dockerfile.filename)
		filepath = os.path.join('./data/', filename)
		dockerfile.save(filepath)

		output = docker('build', './data/')
		# remove after build
		#os.remove(filepath)

		resp = json.dumps("{'completed': 'true'}")

	return Response(response=resp, mimetype="application/json")




@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
	"""
	Update container attributes (support: state=running|stopped)

	curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "running"}'
	curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}'

	"""
	body = request.get_json(force=True)
	try:
		state = body['state']
		if state == 'running':
			docker('restart', id)
		elif state == 'stopped':
			docker('stop', id)
	except:
		pass

	action = []
	action.append('{"id": "%s"}' % id)
	action.append('{"action": %s}' % state)

	resp = json.dumps(action)
	return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
	"""
	Update image attributes (support: name[:tag])  tag name should be lowercase only

	curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/7f2619ed1768 -d '{"tag": "test:1.0"}'

	"""
	body = request.get_json(force=True)
	try:
		tag = body['tag']
		docker('tag', id, tag)
	except:
		pass

	resp = '{"id": "%s"}' % id
	return Response(response=resp, mimetype="application/json")


def docker(*args):
	cmd = ['docker']
	for sub in args:
		cmd.append(sub)
	process = Popen(cmd, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	if stderr.startswith('Error'):
		print 'Error: {0} -> {1}'.format(' '.join(cmd), stderr)
	return stderr + stdout

# 
# Docker output parsing helpers
#

#
# Parses the output of a Docker PS command to a python List
# 
def docker_ps_to_array(output):
	all = []
	for c in [line.split() for line in output.splitlines()[1:]]:
		each = {}
		each['id'] = c[0]
		each['image'] = c[1]
		each['name'] = c[-1]
		each['ports'] = c[-2]
		all.append(each)
	return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
	logs = {}
	logs['id'] = id
	all = []
	for line in output.splitlines():
		all.append(line)
	logs['logs'] = all
	return logs

#
# Parses the output of a Docker image command to a python List
# 
def docker_images_to_array(output):
	all = []
	for c in [line.split() for line in output.splitlines()[1:]]:
		each = {}
		each['id'] = c[2]
		each['tag'] = c[1]
		each['name'] = c[0]
		all.append(each)
	return all

#
# Parses the output of a Docker build command to a python Dictionary
# (Key Value Pair object)
def docker_build_to_object(output):
	result = {}
	all = []
	for line in output.splitlines():
		all.append(line)
	result['result'] = all
	return result

if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5000, debug=True)
