import yaml
import os

from box import Box

from flask import Flask
from flask_restful import Api

import redis

from lib.health import Health
from lib.lock_manager import LockManager
from lib.lock_catalog import LockCatalog

config = Box.from_yaml(
    filename=os.environ.get("CONFIG_PATH", "./config.example.yml"),
    Loader=yaml.FullLoader,
)

app = Flask(__name__)
api = Api(app)

conn = redis.Redis(**config.redis.host)

# TODO Some persistent storage
#   https://github.com/hashicorp/nomad-guides/blob/master/application-deployment/redis/redis.nomad
locks = {}

# FIXME Rename file to not import from main


# TODO Consider separate create/refresh paths
api.add_resource(Health, "/health")
api.add_resource(LockManager, "/<uuid:lock_id>")
api.add_resource(LockCatalog, "/locks")

# TODO Add metrics

if __name__ == "__main__":
    app.run(**config.flask)
