import time


# IDEA Think of some human-friendly format, like docker names-generator
#   https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
# IDEA Is it possible to use some inline docs + mkdocs?
class Lock(object):
    # TODO Consider adding time left property
    # TODO Use integers for timings since we're not operationg fractions smaller than a second
    def __init__(self, id: str = None, ttl: float = 60.0, **kwargs):
        self.id = id
        self.timestamp = kwargs.get("timestamp") or time.time()
        self.ttl = ttl
        self.expires = kwargs.get("expires") or (self.timestamp + self.ttl)

    # FIXME Should be a roperty
    def is_active(self):
        return self.expires > time.time()

    def refresh(self):
        self.expires = time.time() + self.ttl
