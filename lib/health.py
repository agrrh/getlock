import time

from flask_restful import Resource


# TODO Move storage check to storage internal method
class Health(Resource):
    def __init__(self, id='changeme', storage=None):
        self.id = id
        self.storage = storage

    def get(self):
        try:
            self.storage.update(f"health-{self.id}", time.time())
            time_write = self.storage.read(f"health-{self.id}")
            time_avg = (time.time() - time_write) / 2.0
            assert time_avg > 0
            self.storage.delete(f"health-{self.id}")
        except Exception:
            return {
                "message": "failed"
            }, 500

        return {
            "message": "okay",
            "storage_response": f"{time_avg}"
        }, 200
