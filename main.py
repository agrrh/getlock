import time
import yaml
import os

from box import Box

from flask import Flask
from flask_restful import Resource, Api, reqparse

config = Box.from_yaml(
    filename=os.environ.get("CONFIG_PATH", "./config.example.yml"),
    Loader=yaml.FullLoader,
)

app = Flask(__name__)
api = Api(app)

# TODO Some persistent storage
#   https://github.com/hashicorp/nomad-guides/blob/master/application-deployment/redis/redis.nomad
locks = {}


# TODO Move to separate file
# IDEA Think of some human-friendly format, like docker names-generator
#   https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
# IDEA Is it possible to use some inline docs + mkdocs?
class Lock(object):
    # TODO Consider adding time left property
    # TODO Use integers for timings since we're not operationg fractions smaller than a second
    def __init__(self, id: str, ttl=60.0):
        self.id = id
        self.timestamp = time.time()
        self.ttl = ttl
        self.expires = self.timestamp + self.ttl
        # REVIEW Why actually?
        self.refreshed = []

    # FIXME Should be a roperty
    def is_active(self):
        return self.expires > time.time()

    def refresh(self):
        self.refreshed.append(time.time())

        if len(self.refreshed) > 10:
            self.refreshed = self.refreshed[:10]

        self.expires = time.time() + self.ttl


# TODO Move to separate file
class LockManager(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "ttl", type=float, default=60.0, help="Time for lock to live without refreshes"
    )

    # FIXME Steal prevention, some kind of owner token?
    def put(self, lock_id):
        args = self.parser.parse_args(strict=True)

        lock = Lock(str(lock_id), **args)

        if lock.id not in locks:
            locks[lock.id] = lock
            return {
                "locked": True,
                "message": "lock acquired",
                "lock": lock.__dict__,
            }, 201

        lock = locks.get(lock.id)
        locks[lock.id].refresh()

        return {"locked": True, "message": "lock refreshed", "lock": lock.__dict__}, 200

    def get(self, lock_id):
        lock = locks.get(str(lock_id), None)

        if not lock:
            return {"locked": False, "message": "lock not found or expired"}, 404

        if not lock.is_active():
            del locks[lock.id]
            return {
                "locked": False,
                "message": "lock has expired",
                "lock": lock.__dict__,
            }, 404

        return {"locked": True, "message": "lock is active", "lock": lock.__dict__}, 423

    # FIXME Add some security, like check for owner token?
    def delete(self, lock_id):
        lock = locks.get(str(lock_id), None)

        if not lock:
            return {"locked": False, "message": "lock not found or expired"}, 404

        del locks[lock.id]
        return {
            "locked": False,
            "message": "lock has been removed",
            "lock": lock.__dict__,
        }, 200


class LockCatalog(Resource):
    def get(self):
        return {
            "message": "okay",
            "locks": {lock.id: lock.__dict__ for lock_id, lock in locks.items()},
            "locks_count": len(locks),
        }, 200


# TODO Add some logic behind it
# TODO Move to separate file
class Health(Resource):
    def get(self):
        return {
            "message": "okay"
        }, 200


# TODO Consider separate create/refresh paths
api.add_resource(Health, "/health")
api.add_resource(LockManager, "/<uuid:lock_id>")
api.add_resource(LockCatalog, "/locks")

# TODO Add metrics

if __name__ == "__main__":
    app.run(**config.flask)
