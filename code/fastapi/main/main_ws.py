from main.main_imports import *

class MainWs:

  def __init__(self, redis):
    self.clients = {}
    self.redis = redis


  # client websocket daemon
  async def Start(self, websocket: WebSocket, client_id: int):
    # https://stackoverflow.com/questions/62413893/how-to-send-websocket-updates-to-any-connected-clients-while-running-a-while-tru
    # make this ping every 30 sec
    await self.Connect(websocket, client_id)
    try:
      msg_data = { 'message' : 'client #' + str(client_id) + ' connected' }
      await self.Broadcast(json.dumps(msg_data))
      state_data = json.dumps(self.redis.GetState())
      await self.Broadcast(state_data)
      while True:
        data = await websocket.receive_text()
        if (data == 'ping'):
          await self.Send('pong', client_id)
    except WebSocketDisconnect:
      self.Disconnect(client_id)
      msg_data = { 'message' : 'client #' + str(client_id) + ' disconnected' }
      await self.Broadcast(json.dumps(msg_data))


  async def Connect(self, websocket: WebSocket, client_id: int):
    await websocket.accept()
    self.clients[client_id] = websocket


  def Disconnect(self, client_id: int):
    if (client_id in self.clients):
      del self.clients[client_id]


  async def Broadcast(self, message: str):
    for key in list(self.clients.keys()):
        await self.Send(message, key)


  async def Send(self, message: str, client_id: int):
    try:
      await self.clients[client_id].send_text(message)
    except:
      self.Disconnect(client_id)


