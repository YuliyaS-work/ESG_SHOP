import redis

r = redis.Redis(host='172.30.114.77', port=6379, db=0)

r.set('yuliya', 'awesome')
print(r.get('yuliya'))

try:
    r.ping()
    print("Redis доступен!")
except redis.ConnectionError:
    print("Redis не отвечает.")
