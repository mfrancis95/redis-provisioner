from docker import APIClient
from os import environ
from docker.errors import APIError

_docker = APIClient(environ.get('DOCKER_SOCKET', 'unix://var/run/docker.sock'), 'auto')

def _container_map(container):
    return {
        'id': container['Id'], 'name': container['Names'][0][1:],
        'port': container['Ports'][0]['PublicPort'],
        'status': container['Status'],
        'username': container['Labels']['username']
    }

def create(username, name, port, password):
    try:
        container = _docker.create_container(
            'redis:alpine', command = f'redis-server --requirepass {password}',
            detach = True,
            host_config = _docker.create_host_config(port_bindings = {
                6379: port
            }),
            labels = {'username': username}, name = name
        )
        _docker.start(container['Id'])
        return True
    except APIError as error:
        if error.status_code == 500:
            _docker.remove_container(container['Id'])
    return False

def delete(id):
    try:
        _docker.remove_container(id, force = True)
    except:
        return False
    return True

def get_instances():
    return map(_container_map, _docker.containers())