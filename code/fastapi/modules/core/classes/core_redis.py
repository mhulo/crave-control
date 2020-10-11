import json
import redis
from time import time

class CoreRedis:

  # will only connect if not already connected
  def Conn(self):
  	return redis.Redis(host='redis', port=6379, db=0)


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





