from docker import APIClient
from os import environ

_docker = APIClient(environ['DOCKER_SOCKET'], 'auto')

def _container_map(container):
    return {
        'id': container['Id'],
        'name': container['Names'][0][1:],
        'port': container['Ports'][0]['PublicPort'],
        'status': container['Status'],
        'username': container['Labels']['username']
    }

def get_instances():
    return (_container_map(container) for container in _docker.containers())