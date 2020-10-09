import json
import redis
from time import time

class RedisCache:

  def Conn(self):

  	return redis.Redis(host='redis', port=6379, db=0)


  # dump a dict value to json and set
  def JSet(self, key, val):

    r = self.Conn()
    r.set(key, json.dumps(val))


  # get a value and load json to dict
  def JGet(self, key):

    r = self.Conn()
    return json.loads(r.get(key))


  def Set(self, key, val):

    r = self.Conn()
    r.set(key, val)
    r.set('last_updated', str(time()))


  # get a value and decode from bytes to str
  def Get(self, key):

    r = self.Conn()
    return r.get(key).decode("utf-8")



