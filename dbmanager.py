# _*_ coding: utf-8 _*_
__author__ = 'cheng'

import  redis
#import redisClient
from srvframe.database import Connection
from srvframe.database import Connection
from config.const import db_server,db_database,db_user,db_password

#redis db on localhost
#token_redis = redisClient.StrictRedis(host='127.0.0.1', port=6379, db=0)

manage_pic_db=Connection(host= db_server, database=db_database,user=db_user, password=db_password)

RedisClient = redis.StrictRedis(host="127.0.0.1", port=16379, db=0)
