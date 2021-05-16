from main.main_common import *

class CoreEvent:

  def __init__(self):
    self.ifx_key = 'ifx_core'
    self.redis = Request.state.redis
    self.ws = Request.state.ws


  # event server daemon
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    loop_id = started_ts
    self.redis.HSet(self.ifx_key, {
      'loop_id': loop_id ,
      'loop_ts': started_ts,
      'started_ts': started_ts,
      'updated_ts': started_ts,
      'message':  'started',
      'state': '{'+'}'
    })
    cached_state = {}
    cached_updated_ts = 0
    while (this_id == loop_id):
      updated_ts = float(self.redis.HGet(self.ifx_key, 'updated_ts'))
      if (updated_ts != cached_updated_ts):
        state = self.redis.GetState()
        await self.HandleEvent(state, cached_state)
        cached_state = state
      self.redis.HSet(self.ifx_key, { 'loop_ts' : str(time()) })
      loop_id = self.redis.HGet(self.ifx_key, 'loop_id')
      cached_updated_ts = updated_ts
      await asyncio.sleep(0.25) # 250ms


  def Stop(self):
    self.redis.HSet(self.ifx_key, {
      'loop_id': '0', 
      'message' : 'stopped',
      'state': '{'+'}'
    })


  def Status(self):
    ret_val = self.redis.GetStatus(self.daemon_key)
    return ret_val


  def State(self):
    ret_val = self.redis.GetState()
    return ret_val


  # iterate through latest ifx_state
  # then broadcast updates and meta
  # then process meta rules based on updates
  async def HandleEvent(self, state={}, cached_state={}):
    change_data = {}
    # add all changed ifx_state to a change_data dict
    for key in state:
      if (key == 'updated_ts'):
        change_data[key] = str(datetime.fromtimestamp(float(state[key])))
      elif (key in cached_state):
        if (state[key] != cached_state[key]):
          change_data[key] = state[key]
      else:
        change_data[key] = state[key]

    # broadcast changed ifx_state via websocket
    if (change_data != {}):
      await self.ws.Broadcast(json.dumps(change_data))

    # process updated ifx_meta (can include derived vals)
    # save updated ifx_meta to redis

    # process rules based on ifx_state and ifx_meta 




