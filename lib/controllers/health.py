from flask_restful import Resource


class HealthController(Resource):
    def __init__(self, id='changeme', storage=None):
        self.id = id
        self.storage = storage

    def get(self):
        try:
            time_avg = self.storage.health(key=f"health-{self.id}")
        except Exception:
            time_avg = 0
            message = "Health check failed"
            code = 500
        else:
            message = "OK"
            code = 200

        return {
            "message": message,
            "storage_response": f"{time_avg}"
        }, code
