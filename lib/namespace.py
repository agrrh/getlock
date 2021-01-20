from lib.storage_object import StorageObject


class Namespace(StorageObject):
    STORAGE_PREFIX = "namespace"
    PROPERTIES_IGNORE_DUMP = ("token",)

    def __init__(self, storage, id):
        super(Namespace, self).__init__(storage=storage, id=id)

        self.id = id
        self.token = id  # FIXME For now it's just namespace name. Later we should use some hash or JWT?
        self.locks = []
