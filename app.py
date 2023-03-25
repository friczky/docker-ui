import docker
from flask import Flask, jsonify, render_template, url_for, redirect, request

app = Flask(__name__)
client = docker.from_env()


@app.route('/containers')
def containers():
    containers = client.containers.list()
    return jsonify([c.name for c in containers])


@app.route('/containers/create')
def create_container():
    container = client.containers.run('nginx:latest', detach=True)
    return container.id


@app.route('/containers/<container_id>/stop')
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    return 'Kontainer telah dihentikan'


@app.route('/volumes')
def volumes():
    volumes = client.volumes.list()
    return jsonify([v.name for v in volumes])


@app.route('/volumes/create')
def create_volume():
    volume = client.volumes.create()
    return volume.name


@app.route('/volumes/<volume_name>/remove')
def remove_volume(volume_name):
    volume = client.volumes.get(volume_name)
    volume.remove()
    return 'Volume telah dihapus'


if __name__ == '__main__':
    app.run()
