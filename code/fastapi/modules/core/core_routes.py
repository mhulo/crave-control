from main.main_imports import *
from modules.core.classes.core_state import *
from modules.core.classes.core_event import *

router = APIRouter()
Request.state = CoreState()

core_redis = Request.state.core_redis
core_ws = Request.state.core_ws
core_event = CoreEvent()


# event routes
@router.websocket("/ws/{client_id}/")
async def ws_start(websocket: WebSocket, client_id: int):
  await core_ws.Start(websocket, client_id)


@router.get("/api/event/start/")
async def event_start():
  await core_event.Start()


@router.get('/app/ws/test/')
def ws_test():
  resp = core_ws.TestHtml()
  return HTMLResponse(resp)


@router.get('/api/ws/broadcast/{q}/')
async def ws_broadcast(q: str):
  await core_ws.Broadcast(q)
  return { 'message' : 'sent' }


# redis routes
@router.get('/app/redis/set/{q}/')
def redis_set(q: str):
  core_redis.Set('foo', q)
  return HTMLResponse('set to ' + q)








