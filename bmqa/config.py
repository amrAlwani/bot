import fnmatch
import os
import redis


class DummyRedis:
    def __init__(self):
        self.store = {}
        self.hashes = {}
        self.sets = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, ex=None):
        self.store[key] = str(value)
        return True

    def delete(self, *keys):
        removed = 0
        for key in keys:
            if key in self.store:
                del self.store[key]
                removed += 1
            if key in self.hashes:
                del self.hashes[key]
                removed += 1
            if key in self.sets:
                del self.sets[key]
                removed += 1
        return removed

    def hgetall(self, name):
        return dict(self.hashes.get(name, {}))

    def hget(self, name, key):
        return self.hashes.get(name, {}).get(key)

    def hset(self, name, key, value):
        self.hashes.setdefault(name, {})[key] = str(value)
        return 1

    def hdel(self, name, *keys):
        removed = 0
        if name in self.hashes:
            for key in keys:
                if key in self.hashes[name]:
                    del self.hashes[name][key]
                    removed += 1
        return removed

    def smembers(self, name):
        return set(self.sets.get(name, set()))

    def sadd(self, name, *values):
        self.sets.setdefault(name, set()).update(str(v) for v in values)
        return len(values)

    def sismember(self, name, value):
        return str(value) in self.sets.get(name, set())

    def srem(self, name, *values):
        removed = 0
        if name in self.sets:
            for v in values:
                sv = str(v)
                if sv in self.sets[name]:
                    self.sets[name].discard(sv)
                    removed += 1
        return removed

    def exists(self, key):
        return key in self.store or key in self.hashes or key in self.sets

    def keys(self, pattern="*"):
        return [key for key in self.store if fnmatch.fnmatch(key, pattern)]

    def incr(self, key, amount=1):
        value = int(self.store.get(key, 0)) + amount
        self.store[key] = str(value)
        return value

    def setex(self, key, ex, value):
        return self.set(key, value, ex=ex)

    def ttl(self, key):
        return -1

    def expire(self, key, seconds):
        return True

    def lrange(self, name, start, end):
        return []

    def lpush(self, name, *values):
        return len(values)

    def type(self, key):
        if key in self.store:
            return b"string"
        if key in self.hashes:
            return b"hash"
        if key in self.sets:
            return b"set"
        return b"none"


try:
    r = redis.Redis("localhost", decode_responses=True)
    r.ping()
except Exception as e:
    print(f"Redis not available: {e}")
    r = DummyRedis()

TOKEN = os.environ.get("BOT_TOKEN", "5892582536:AAGnc7hxSfEque9vSKK5BueykFDYFhFnoaY")
if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not set. "
        "Please add your Telegram bot token as a secret named BOT_TOKEN."
    )

Dev_Zaid = TOKEN.split(":")[0]
OWNER_ID = int(os.environ.get("OWNER_ID", "7264011066"))
BOT_NAME = os.environ.get("BOT_NAME", "")
botUsername = BOT_NAME
NAME = os.environ.get("NAME", "غدغد")

from kvsqlite.sync import Client as DB

ytdb = DB("ytdb.sqlite")
sounddb = DB("sounddb.sqlite")
wsdb = DB("wsdb.sqlite")
