from main.main_imports import *

class CoreEvent:

  def __init__(self):
    self.mod_name = 'core'
    #####
    self.daemon_key = self.mod_name + '_daemon'
    self.redis = Request.state.redis
    self.ws = Request.state.ws

  # server websocket daemon
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    instance_id = started_ts
    self.redis.HSet(self.daemon_key, { 'instance_id' : instance_id , 'started_ts' : started_ts })
    cached_state = {} # dict of json strings
    i = 0
    while (i < 10):
      while (this_id == instance_id):
        # could look at a global last_changed
        state = self.redis.HGetAll('state')
        await self.HandleEvent(state, cached_state)
        instance_id = self.redis.HGet(self.daemon_key, 'instance_id')
        cached_state = state
        self.redis.HSet(self.daemon_key, { 'last_iteration_ts' : str(time()) })
        await asyncio.sleep(0.25) # 250ms


  # grab latest data then handle changes and broadcast updates
  async def HandleEvent(self, state = {}, cached_state = {}):
    change_data = {}
    for key in state:
      if (key in cached_state):
        if (state[key] != cached_state[key]):
          change_data[key] = json.loads(state[key])
    if (change_data = {}):
      await self.ws.Broadcast(json.dumps(change_data))





