import time
import uuid
import re

from lib.objects.generic import GenericObject


class Lock(GenericObject):
    STORAGE_PREFIX = "lock"

    PROPERTIES_IGNORE_DUMP = ("namespace",)

    # Some random UUID to make lock UUIDs persistent
    ROOT_UUID = uuid.UUID("0bbbf540-1e6d-47f9-ab52-0d3d6c814018")

    def __init__(self, storage, namespace, id, **kwargs):
        self.id = id
        self.uuid = str(
            uuid.uuid5(
                self.ROOT_UUID,
                "-".join((namespace.id, id))
            )
        )

        self.namespace = namespace

        super(Lock, self).__init__(storage=storage, id=self.uuid)

        self.ttl = kwargs.get("ttl", 60)
        self.timestamp = kwargs.get("timestamp", int(time.time()))

    def _write(self):
        self.namespace._load_self()

        # Replace old occurency with new one
        if self.id in [lock.get("id") for lock in self.namespace.locks]:
            self.namespace.locks = list(filter(lambda i: i.get("id") != self.id, self.namespace.locks))
        self.namespace.locks.append(self._dump())

        self.namespace.update()

        self._storage.create(self._storage_id, self._dump())
        self._storage.ttl(self._storage_id, self.ttl)

    # FIXME Rework this dirty hack
    #   We need always dump current Lock age, not from DB, but current one
    def read(self):
        data = self._storage.read(self._storage_id)

        if data:
            data.update({"age": int(time.time()) - data.get("timestamp")})

        return data

    def validate_id(self):
        return bool(re.match(r'^[a-z0-9][0-9a-z-]{2,46}[0-9a-z]$', self.id))
