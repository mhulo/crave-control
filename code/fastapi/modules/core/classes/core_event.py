from main.main_imports import *

class CoreEvent:

  def __init__(self):
    self.redis = Request.state.redis
    self.ws = Request.state.ws


  # server websocket daemon
  async def Start(self):
    daemon_id = str(time())
    self.redis.Set('event_server.daemon_id', daemon_id)
    instance_id = daemon_id
    cached_val_data = {}
    while (instance_id == daemon_id):
      change_data = await self.DataChanged()
      latest_val_data = self.GetValData()
      await self.HandleEvent(latest_val_data, cached_val_data)
      instance_id = change_data['event_server.daemon_id']
      cached_val_data = latest_val_data


  # wait for a data change then return
  async def DataChanged(self):
    cached_change_data = self.GetChangeData()
    latest_change_data = cached_change_data
    while (cached_change_data == latest_change_data):
      latest_change_data = self.GetChangeData()
      await asyncio.sleep(0.3) # 300ms
    return latest_change_data


  # grab latest data then handle changes and broadcast updates
  async def HandleEvent(self, latest_val_data, cached_val_data = {}):
    for key in latest_val_data:
      send = True
      if (key in cached_val_data):
        if (latest_val_data[key] == cached_val_data[key]):
          send = False
      if (send == True):
        await self.ws.Broadcast(f'server says: {key} changed to: {latest_val_data[key]}')


  def GetChangeData(self):
    data_keys = ['event_server.daemon_id', 'last_updated']
    data = {}
    for key in data_keys:
      data[key] = self.redis.Get(key)
    return data


  def GetValData(self):
    data_keys = ['foo']
    data = {}
    for key in data_keys:
      data[key] = self.redis.Get(key)
    return data



