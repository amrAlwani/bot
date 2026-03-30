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

    def hlen(self, name):
        return len(self.hashes.get(name, {}))

    def hkeys(self, name):
        return list(self.hashes.get(name, {}).keys())

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

    def scard(self, name):
        """إرجاع عدد العناصر في المجموعة (set)"""
        return len(self.sets.get(name, set()))

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
    # استخدم wsdb (kvsqlite) كبديل دائم
    from kvsqlite.sync import Client as DB
    wsdb = DB("wsdb.sqlite")
    class WSDBRedis:
        def get(self, key):
            return wsdb.get(key)
        def set(self, key, value, ex=None):
            wsdb.set(key, value)
            return True
        def delete(self, *keys):
            for key in keys:
                wsdb.delete(key)
            return True
        def sadd(self, name, *values):
            s = set(wsdb.get(name) or [])
            for v in values:
                s.add(str(v))
            wsdb.set(name, list(s))
            return len(values)
        def smembers(self, name):
            return set(wsdb.get(name) or [])
        def sismember(self, name, value):
            return str(value) in set(wsdb.get(name) or [])
        def srem(self, name, *values):
            s = set(wsdb.get(name) or [])
            for v in values:
                s.discard(str(v))
            wsdb.set(name, list(s))
            return True
        def exists(self, key):
            return wsdb.get(key) is not None
        def keys(self, pattern="*"):
            # kvsqlite لا يدعم الأنماط، نعيد كل المفاتيح
            return wsdb.keys()

        # Hash methods
        def hgetall(self, name):
            return dict(wsdb.get(name) or {})
        def hget(self, name, key):
            d = wsdb.get(name) or {}
            return d.get(key)
        def hset(self, name, key, value):
            d = wsdb.get(name) or {}
            d[key] = str(value)
            wsdb.set(name, d)
            return 1
        def hdel(self, name, *keys):
            d = wsdb.get(name) or {}
            removed = 0
            for key in keys:
                if key in d:
                    del d[key]
                    removed += 1
            wsdb.set(name, d)
            return removed
        def hlen(self, name):
            d = wsdb.get(name) or {}
            return len(d)
        def hkeys(self, name):
            d = wsdb.get(name) or {}
            return list(d.keys())
    r = WSDBRedis()

TOKEN = os.environ.get("BOT_TOKEN", "")
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
