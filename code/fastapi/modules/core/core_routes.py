from main.main_imports import *


router = APIRouter()
ws = CoreWss()

@router.websocket("/wss/{client_id}/")
async def wss_client_daemon(websocket: WebSocket, client_id: int):
  await ws.ClientDaemon(websocket, client_id)


@router.get("/api/wss/server/start/")
async def wss_server_daemon():
  await ws.ServerDaemon()


@router.get('/app/wss/test/')
def WssTest():
  resp = ws.TestHtml()
  return HTMLResponse(resp)


@router.get('/app/redis/set/{q}/')
def RedisSet(q: str):
  CoreRedis().Set('foo', q)
  return HTMLResponse('set to ' + q)








