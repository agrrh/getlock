from lib.objects.generic import GenericObject
from lib.objects.lock import Lock


class Namespace(GenericObject):
    STORAGE_PREFIX = "namespace"
    PROPERTIES_IGNORE_DUMP = ("token",)

    def __init__(self, storage, id):
        super(Namespace, self).__init__(storage=storage, id=id)

        self.id = id
        self.token = id  # FIXME For now it's just namespace name. Later we should use some hash or JWT?
        self.locks = []

    def _locks_refresh(self):
        self.locks = [
            lock_id
            for lock_id
            in self.locks
            if Lock(storage=self._storage, namespace=self, id=lock_id).read()
        ]
        self.locks = list(set(self.locks))
