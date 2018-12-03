from flask import Flask, jsonify
from redis_provisioner.redis import get_instances

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(list(get_instances()))
