import json
import redis

from time import time
from datetime import datetime


class MainRedis:

  # will only connect if not already connected
  def Conn(self):
  	return redis.Redis(host='redis', port=6379, db=0)


  def Set(self, key, val):
    r = self.Conn()
    r.set(key, val)


  # get a value and decode from bytes to str
  def Get(self, key):
    r = self.Conn()
    val = r.get(key)
    if (val != None):
      val = val.decode("utf-8")
    return val


  def Del(self, key):
    r = self.Conn()
    r.delete(key)


  # dump a dict value to json and set
  def JSet(self, key, val):
    r = self.Conn()
    r.set(key, json.dumps(val))


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
    if (rhash == 'state'):
      rdata['updated_ts'] = str(time())
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


  # get state as dicts
  def GetState(self):
    r = self.Conn()
    resp = r.hgetall('state')
    vals = {}
    for i in resp:
      if (resp[i] != None):
        val = resp[i].decode("utf-8")
        if (val[0:1] == '{'):
          val = json.loads(val)
      vals[i.decode("utf-8")] = val

    return vals


  def GetStatus(self, rhash):
    status = self.HGetAll(rhash)
    data = {}
    for key in status:
      if (key[-3:] == '_ts'):
        data[key[0:-2]+'sec'] = time() - float(status[key])
        data[key] = datetime.fromtimestamp(float(status[key]))
      else:
        data[key] = status[key]
    if ('started_sec' in data):
      if (float(data['started_sec']) < 10): # consider it running if last iteration is within 10 sec
        status['message'] = 'running'
    vals = { rhash : data }
    return vals




