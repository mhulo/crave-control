from main.web_imports import *

rc = RedisCache()
app = FastAPI(debug=True)

class CoreWss:
  def __init__(self):
    self.active_connections: List[WebSocket] = []


  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.active_connections.append(websocket)


  def disconnect(self, websocket: WebSocket):
    if (websocket in self.active_connections):
      self.active_connections.remove(websocket)


  async def broadcast(self, message: str):
    for connection in self.active_connections:
      try:
        await connection.send_text(message)
      except:
        self.disconnect(connection)


wss = CoreWss()

def get_change_data():
  data_keys = ['ws_daemon_id', 'last_updated']
  data = {}
  for key in data_keys:
    data[key] = rc.Get(key)
  return data


def get_val_data():
  data_keys = ['foo']
  data = {}
  for key in data_keys:
    data[key] = rc.Get(key)
  return data


# wait for a data change then return
async def data_changed():
  cached_change_data = get_change_data()
  latest_change_data = cached_change_data
  while (cached_change_data == latest_change_data):
    latest_change_data = get_change_data()
    await asyncio.sleep(300/1000) # 300ms
  return latest_change_data


# grab latest data and broadcast it
async def send_updates(cached_val_data = {}):
  latest_val_data = get_val_data()
  for key in latest_val_data:
    send = True
    if (key in cached_val_data):
      if (latest_val_data[key] == cached_val_data[key]):
        send = False
    if (send == True):
      await wss.broadcast(f"Server says: {key} changed to: {latest_val_data[key]}")
  return latest_val_data


@app.get("/ws/start/")
async def start_ws_svr():

  daemon_id = str(time())
  rc.Set('ws_daemon_id', daemon_id)
  instance_id = daemon_id
  cached_val_data = {}

  while (instance_id == daemon_id):
    change_data = await data_changed()
    latest_val_data = await send_updates(cached_val_data)
    instance_id = change_data['ws_daemon_id']
    cached_val_data = latest_val_data

  return HTMLResponse('ws server stopped')


@app.websocket("/ws/{client_id}")
async def ws_client(websocket: WebSocket, client_id: int):
  await wss.connect(websocket)
  try:
    await wss.broadcast(f"Client #{client_id} joined the chat")
    await send_updates()
    while True:
      data = await websocket.receive_text()
      await wss.send_personal_message(f"You wrote: {data}", websocket)
      await wss.broadcast(f"Client #{client_id} says: {data}")
  except WebSocketDisconnect:
    wss.disconnect(websocket)
    await wss.broadcast(f"Client #{client_id} left the chat")


@app.get('/wss/test/')
async def CgateTest3():
  ts = str(time())
  html = '<html><body><h1>Look hey! HTML!' + ts + '</h1></body></html>'
  return HTMLResponse(html)

