from main.main_imports import *

class MainWs:

  def __init__(self, redis):
    self.clients = {}
    self.redis = redis


  # client websocket daemon
  async def Start(self, websocket: WebSocket, client_id: int):
    # https://stackoverflow.com/questions/62413893/how-to-send-websocket-updates-to-any-connected-clients-while-running-a-while-tru
    await self.Connect(websocket, client_id)
    try:
      await self.Broadcast(f'client #{client_id} connected')
      vals_keys = ['foo']
      vals_data = self.redis.GetData(vals_keys)
      await self.Broadcast(vals_data)
      while True:
        data = await websocket.receive_text()
        if (data == 'ping'):
          await self.Send('pong', client_id)
    except WebSocketDisconnect:
      self.Disconnect(client_id)
      await self.Broadcast(f'client #{client_id} disconnected')


  async def Connect(self, websocket: WebSocket, client_id: int):
    await websocket.accept()
    self.clients[client_id] = websocket


  def Disconnect(self, client_id: int):
    if (client_id in self.clients):
      del self.clients[client_id]


  async def Broadcast(self, message: str):
    for key in self.clients:
        await self.Send(message, key)


  async def Send(self, message: str, client_id: int):
    try:
      await self.clients[client_id].send_text(message)
    except:
      self.Disconnect(client_id)


  def TestHtml(self):

    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WS Test</h1>
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
            var ws = new WebSocket(`ws://localhost:8888/ws/core/${client_id}/`);
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



