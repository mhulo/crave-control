from main.main_imports import *

class CoreEvent:

  def __init__(self):
    self.rc = CoreRedis()
    self.clients = {}


  async def ClientDaemon(self, websocket: WebSocket, client_id: int):
    # https://stackoverflow.com/questions/62413893/how-to-send-websocket-updates-to-any-connected-clients-while-running-a-while-tru
    await self.WsConnect(websocket, client_id)
    try:
      await self.WsBroadcast(f'client #{client_id} connected')
      latest_val_data = self.GetValData()
      await self.HandleEvent(latest_val_data)
      while True:
        data = await websocket.receive_text()
        if (data == 'ping'):
          await self.WsSend('pong', websocket)
    except WebSocketDisconnect:
      self.WsDisconnect(client_id)
      await self.WsBroadcast(f'client #{client_id} disconnected')


  async def ServerDaemon(self):
    daemon_id = str(time())
    self.rc.Set('event_server.daemon_id', daemon_id)
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
        await self.WsBroadcast(f'server says: {key} changed to: {latest_val_data[key]}')


  def GetChangeData(self):
    data_keys = ['event_server.daemon_id', 'last_updated']
    data = {}
    for key in data_keys:
      data[key] = self.rc.Get(key)
    return data


  def GetValData(self):
    data_keys = ['foo']
    data = {}
    for key in data_keys:
      data[key] = self.rc.Get(key)
    return data


  async def WsConnect(self, websocket: WebSocket, client_id: int):
    await websocket.accept()
    self.clients[client_id] = websocket


  def WsDisconnect(self, client_id: int):
    if (client_id in self.clients):
      del self.clients[key]


  async def WsBroadcast(self, message: str):
    for key in self.clients:
      try:
        await self.clients[key].send_text(message)
      except:
        self.WsDisconnect(key)


  async def WsSend(self, message: str, websocket: WebSocket):
    await websocket.send_text(message)


  def TestHtml(self):

    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8888/wss/core/${client_id}/`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
    return html



