from main.main_imports import *

class CoreWss:

  def __init__(self):
    self.rc = CoreRedis()
    self.clients = {}


  async def ClientDaemon(self, websocket: WebSocket, client_id: int):
    # https://stackoverflow.com/questions/62413893/how-to-send-websocket-updates-to-any-connected-clients-while-running-a-while-tru
    await self.Connect(websocket, client_id)
    try:
      await self.Broadcast(f"Client #{client_id} connected")
      await self.SendUpdates()
      while True:
        data = await websocket.receive_text()
        await self.Broadcast(f"Client #{client_id} data: {data}")
    except WebSocketDisconnect:
      self.Disconnect(client_id)
      await self.Broadcast(f"Client #{client_id} disconnected")


  async def ServerDaemon(self):

    daemon_id = str(time())
    self.rc.Set('wss_daemon_id', daemon_id)
    instance_id = daemon_id
    cached_val_data = {}

    while (instance_id == daemon_id):
      change_data = await self.DataChanged()
      latest_val_data = await self.SendUpdates(cached_val_data)
      instance_id = change_data['wss_daemon_id']
      cached_val_data = latest_val_data


  # wait for a data change then return
  async def DataChanged(self):
    cached_change_data = self.GetChangeData()
    latest_change_data = cached_change_data
    while (cached_change_data == latest_change_data):
      latest_change_data = self.GetChangeData()
      await asyncio.sleep(300/1000) # 300ms
    await self.Broadcast(f"changed")
    return latest_change_data


  # grab latest data and broadcast it
  async def SendUpdates(self, cached_val_data = {}):
    latest_val_data = self.GetValData()
    for key in latest_val_data:
      send = True
      if (key in cached_val_data):
        if (latest_val_data[key] == cached_val_data[key]):
          send = False
      if (send == True):
        await self.Broadcast(f"Server says: {key} changed to: {latest_val_data[key]}")
    return latest_val_data


  def GetChangeData(self):
    data_keys = ['wss_daemon_id', 'last_updated']
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


  async def Connect(self, websocket: WebSocket, client_id: int):
    await websocket.accept()
    self.clients[client_id] = websocket


  def Disconnect(self, client_id: int):
    if (client_id in self.clients):
      del self.clients[key]


  async def Broadcast(self, message: str):
    for key in self.clients:
      try:
        await self.clients[key].send_text(message)
      except:
        self.Disconnect(key)


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
            var ws = new WebSocket(`ws://localhost:8888/wss/${client_id}/`);
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



