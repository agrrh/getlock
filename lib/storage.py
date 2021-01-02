import redis
import json


class RedisStorage(object):
    def __init__(self, **kwargs):
        self.conn = redis.Redis(**kwargs)

    def create(self, key: str, data):
        data = json.dumps(data)
        self.conn.set(key, data)
        return True

    def read(self, key: str):
        data = self.conn.get(key)
        return json.loads(data) if data else None

    def update(self, key: str, data):
        data = json.dumps(data)
        self.conn.set(key, data)
        return True

    def delete(self, key: str):
        self.conn.delete(key)
        return True

    def list(self):
        return self.conn.keys()

    def ttl(self, key, time: int):
        self.conn.expire(key, time)  # FIXME Not a valid way to get listing
        return True
