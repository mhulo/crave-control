import json
import redis

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



