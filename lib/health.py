from flask_restful import Resource


# TODO Add some logic behind it
class Health(Resource):
    def get(self):
        return {
            "message": "okay"
        }, 200
