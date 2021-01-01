from flask_restful import Resource

from .getlock import locks


class LockCatalog(Resource):
    def get(self):
        return {
            "message": "okay",
            "locks": {lock.id: lock.__dict__ for lock_id, lock in locks.items()},
            "locks_count": len(locks),
        }, 200
