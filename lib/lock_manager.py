from flask_restful import Resource, reqparse

from lib.lock import Lock

# TODO Some persistent storage
#   https://github.com/hashicorp/nomad-guides/blob/master/application-deployment/redis/redis.nomad
locks = {}


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
