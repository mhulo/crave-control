import json
import redis

from time import time

class MainRedis:

  # will only connect if not already connected
  def Conn(self):
  	return redis.Redis(host='redis', port=6379, db=0)


  def Set(self, key, val):
    r = self.Conn()
    r.set(key, val)
    r.set('last_updated', str(time()))


  # get a value and decode from bytes to str
  def Get(self, key):
    r = self.Conn()
    val = r.get(key)
    if (val != None):
      val = val.decode("utf-8")
    return val


  # dump a dict value to json and set
  def JSet(self, key, val):
    r = self.Conn()
    r.set(key, json.dumps(val))
    r.set('last_updated', str(time()))


  # get a value and load json to dict
  def JGet(self, key):
    r = self.Conn()
    val = r.get(key)
    if (val != None):
      val = json.loads(val.decode("utf-8"))
    return val


  # set a dict of values to a hash
  def HSet(self, rhash, rdata):
    r = self.Conn()
    val = r.hset(rhash, mapping=rdata)
    return val


  # get a value from a hash
  def HGet(self, rhash, key):
    r = self.Conn()
    val = r.hget(rhash, key)
    if (val != None):
      val = val.decode("utf-8")
    return val


  # get all values from a hash
  def HGetAll(self, rhash):
    r = self.Conn()
    resp = r.hgetall(rhash)
    vals = {}
    for i in resp:
      if (resp[i] != None):
        vals[i.decode("utf-8")] = resp[i].decode("utf-8")
    return vals


  # delete a key from a hash
  def HDel(self, rhash, key):
    r = self.Conn()
    val = r.hdel(rhash, key)
    return val




