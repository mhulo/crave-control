from main.main_common import *

class CoreEvent:

  def __init__(self):
    self.mod_name = 'core'
    #####
    self.daemon_key = self.mod_name + '_daemon'
    self.redis = Request.state.redis
    self.ws = Request.state.ws


  # event server daemon
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    instance_id = started_ts
    self.redis.HSet(self.daemon_key, { 'instance_id' : instance_id , 'started_ts' : started_ts })
    self.redis.HSet(self.daemon_key, { 'message' : 'started',  'loop_ts' : str(time()) })
    self.redis.HSet('state', { self.mod_name : '' })
    cached_state = {}
    cached_updated_ts = 0
    while (this_id == instance_id):
      updated_ts = float(self.redis.HGet('state', 'updated_ts'))
      if (updated_ts != cached_updated_ts):
        state = self.redis.GetState()
        await self.HandleEvent(state, cached_state)
        cached_state = state
      self.redis.HSet(self.daemon_key, { 'loop_ts' : str(time()) })
      instance_id = self.redis.HGet(self.daemon_key, 'instance_id')
      cached_updated_ts = updated_ts
      await asyncio.sleep(0.25) # 250ms


  def Stop(self):
    self.redis.HSet(self.daemon_key, { 'instance_id' : '0',  'message' : 'stopped' })
    self.redis.HSet('state', { self.mod_name : '{'+'}' } )


  def Status(self):
    ret_val = self.redis.GetStatus(self.daemon_key)
    return ret_val


  def State(self):
    ret_val = self.redis.GetState()
    return ret_val


  # grab latest data then handle changes and broadcast updates
  async def HandleEvent(self, state={}, cached_state={}):
    change_data = {}
    for key in state:
      if (key == 'updated_ts'):
        change_data[key] = str(datetime.fromtimestamp(float(state[key])))
      elif (key in cached_state):
        if (state[key] != cached_state[key]):
          change_data[key] = state[key]
      else:
        change_data[key] = state[key]
    if (change_data != {}):
      await self.ws.Broadcast(json.dumps(change_data))





