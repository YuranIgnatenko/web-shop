import redis

bd = redis.Redis("127.0.0.1", 6379, 0)

def create_user_admin():
    pass

print(bd.get('test_1'))