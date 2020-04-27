import asyncio
import sys
import datetime
import redis
from boto3.session import Session

p = sys.argv
if len(p) < 3:
    print("Usage: python %s <host> <port>" % (p[0]))
    sys.exit(0)

redis = redis.Redis(host=p[1], port=int(p[2]), db=0)

async def increment(thread_name, key, n, wait):
    for i in range(100):
        res = redis.incr(key, n)
    await asyncio.sleep(wait)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    redis.set("allowed", 0)
    t0 = datetime.datetime.now()
    result = loop.run_until_complete(asyncio.gather(
        increment("th1", "allowed", 1, 0.002),
        increment("th2", "allowed", 1, 0.002),
        increment("th3", "allowed", 1, 0.002),
        increment("th4", "allowed", 1, 0.002),
    ))
    t1 = datetime.datetime.now()
    print("Value: %s" % redis.get("allowed"))
    print(t1-t0)
