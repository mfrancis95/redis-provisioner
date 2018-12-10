from docker import APIClient
from os import environ
from subprocess import call

_docker = APIClient(environ['DOCKER_SOCKET'], 'auto')

def _container_map(container):
    return {
        'id': container['Id'],
        'name': container['Names'][0][1:],
        'port': container['Ports'][0]['PublicPort'],
        'status': container['Status'],
        'username': container['Labels']['username']
    }

def create(username, name, port, password):
    return call([
        'docker', 'run', '-d', '-l' f'username={username}', '--name', name,
        '-p', f'{port}:6379', 'redis:alpine', 'redis-server', '--requirepass',
        password
    ])

def get_instances():
    return map(_container_map, _docker.containers())