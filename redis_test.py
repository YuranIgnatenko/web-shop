import redis

bd = redis.Redis("127.0.0.1", 6379, 0)

print(bd.get('test_1'))