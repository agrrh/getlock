import time
import uuid

from datetime import datetime

from lib.storage_object import StorageObject


class Lock(StorageObject):
    STORAGE_PREFIX = "lock"

    PROPERTIES_IGNORE_DUMP = ("namespace",)

    # Some random UUID to make lock UUIDs persistent
    ROOT_UUID = uuid.UUID("0bbbf540-1e6d-47f9-ab52-0d3d6c814018")

    def __init__(self, storage, id, namespace, **kwargs):
        self.id = id
        self.uuid = str(
            uuid.uuid5(
                self.ROOT_UUID,
                "-".join((namespace.id, id))
            )
        )

        super(Lock, self).__init__(storage=storage, id=self.uuid)

        self.ttl = kwargs.get("ttl", 60)
        self.timestamp = kwargs.get("timestamp", int(time.time()))

    # FIXME
    # @property
    # def expires(self):
    #     return datetime.fromtimestamp(self.timestamp + self.ttl)

    def _write(self):
        self._storage.create(self._storage_id, self._dump())
        self._storage.ttl(self._storage_id, self.ttl)
