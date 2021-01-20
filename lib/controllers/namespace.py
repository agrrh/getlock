import logging

from flask_restful import Resource, request

from lib.objects.namespace import Namespace


class NamespaceController(Resource):
    def __init__(self, storage):
        self.storage = storage

    # TODO Validate ID here and for other methods
    # TODO Check access as separate method or decorator
    #   https://flask-restful.readthedocs.io/en/latest/extending.html#resource-method-decorators

    def put(self, namespace_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        logging.info("Checking if namespace exists")

        if not namespace.read():
            logging.warning(f"Namespace {namespace_id} not exists, creating")
            namespace.create()

        else:
            logging.warning(f"Namespace {namespace_id} exists, reading")
            namespace._load_self()

            logging.info("Checking auth")
            token = request.headers.get("X-Getlock-Auth")

            if token != namespace.token:
                logging.warning("Provided wrong auth token")
                return {"message": "Provided wrong auth token"}, 403

            logging.info("Provided correct auth token")

            # TODO Update namespace with data sent (JSON?)

            namespace.update()

        return {"namespace": namespace._dump()}, 201

    def get(self, namespace_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found"}, 404

        namespace._load_self()
        namespace._locks_refresh()

        return {"namespace": namespace._dump()}, 200

    def delete(self, namespace_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found"}, 404

        else:
            namespace._load_self()

            logging.info("Checking auth")
            token = request.headers.get("X-Getlock-Auth")

            if token != namespace.token:
                return {"message": "Provided wrong auth token"}, 403

            logging.warning(f"Removing namespace {namespace_id}")

            namespace.delete()

        return {"message": "Namespace removed"}, 200
