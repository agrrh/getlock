import time


# IDEA Think of some human-friendly format, like docker names-generator
#   https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
# IDEA Is it possible to use some inline docs + mkdocs?
class Lock(object):
    # TODO Consider adding time left property
    # TODO Use integers for timings since we're not operationg fractions smaller than a second
    def __init__(self, id: str, ttl: float = 60.0):
        self.id = id
        self.timestamp = time.time()
        self.ttl = ttl
        self.expires = self.timestamp + self.ttl
        # REVIEW Why actually?
        self.refreshed = []

    # FIXME Should be a roperty
    def is_active(self):
        return self.expires > time.time()

    def refresh(self):
        self.refreshed.append(time.time())

        if len(self.refreshed) > 10:
            self.refreshed = self.refreshed[:10]

        self.expires = time.time() + self.ttl
