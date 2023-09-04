import redis

# 创建 Redis 连接
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# 存储数据
redis_client.set('name', 'Alice')

# 获取数据
retrieved_name = redis_client.get('name')
if retrieved_name:
    print("Retrieved name:", retrieved_name.decode('utf-8'))  # 转换为字符串
