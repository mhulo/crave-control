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


  def GetData(self, keys):
    data = {}
    for key in keys:
      data[key] = self.Get(key)
    return data


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


  def JGetData(self, keys):
    data = {}
    for key in keys:
      data[key] = self.JGet(key)
    return data





