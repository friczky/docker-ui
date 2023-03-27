import docker
from flask import Flask, url_for, render_template, jsonify
import jinja2.exceptions

app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/containers')
def containers():
    containers = client.containers.list()
    return render_template('containers.html', containers=containers)
    # return jsonify([c.name for c in containers])


@app.route('/containers/all')
def containers_all():
    containers = client.containers.list(all=True)
    return jsonify([c.name for c in containers])


@app.route('/containers/<container_id>')
def container(container_id):
    container = client.containers.get(container_id)
    return render_template('containers_details.html', container=container)


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


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
