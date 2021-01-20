class StorageObject(object):
    STORAGE_PREFIX = "object"

    PROPERTIES_IGNORE_DUMP = ()
    PROPERTIES_IGNORE_LOAD = ()

    def __init__(self, storage, *args, **kwargs):
        self._storage = storage
        self._storage_id = ":".join((
            self.STORAGE_PREFIX,
            kwargs.get("id", "changeme")
        ))

    def _dump(self):
        return {
            k: v
            for k, v
            in self.__dict__.items()
            if k not in self.PROPERTIES_IGNORE_DUMP and k not in ("_storage", "_storage_id",)
        }

    def _load(self, **kwargs):
        [
            setattr(self, k, v)
            for k, v
            in kwargs.items()
            if k not in self.PROPERTIES_IGNORE_LOAD and k not in ("_storage", "_storage_id",)
        ]

    def _load_self(self):
        self._load(**self.read())

    def _write(self):
        return self._storage.create(self._storage_id, self._dump())

    def create(self):
        return self._write()

    def read(self):
        return self._storage.read(self._storage_id)

    def update(self):
        return self._write()

    def delete(self):
        return self._storage.delete(self._storage_id)

    def ttl(self, key, time: int):
        return self.storage.ttl(key, time)
