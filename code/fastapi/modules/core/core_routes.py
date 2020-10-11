from main.main_imports import *
from modules.core.classes.core_event import *


router = APIRouter()
ev = CoreEvent()


@router.websocket("/wss/core/{client_id}/")
async def event_client_daemon(websocket: WebSocket, client_id: int):
  await ev.ClientDaemon(websocket, client_id)


@router.get("/api/core/event_server/start/")
async def event_server_daemon_start():
  await ev.ServerDaemon()


@router.get('/app/wss/test/')
def websocket_test():
  resp = ev.TestHtml()
  return HTMLResponse(resp)


@router.get('/app/redis/set/{q}/')
def redis_set(q: str):
  CoreRedis().Set('foo', q)
  return HTMLResponse('set to ' + q)








