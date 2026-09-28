import time
import redis

r = redis.Redis(host='redis', port=6379, decode_responses=True)

while True:
    r.incr("contador")
    print("Incrementando contador...")
    time.sleep(1)