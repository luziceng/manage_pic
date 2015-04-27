__author__ = 'cheng'
import redis

RedisClient = redis.StrictRedis(host="127.0.0.1", port=16379, db=0)


#RedisClient.rpush("user_under_check",1)
#RedisClient.rpush("user_under_check",3)
#RedisClient.rpush("user_under_check",5)


#while RedisClient.llen("user_under_check") >0:
#    t=RedisClient.blpop("user_under_check")
#    print t[1]

print RedisClient.llen("user_under_check")