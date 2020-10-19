from main.main_imports import *
from main.main_settings import *

# autoload modules in main_settings
modules = {}
for i in active_modules:
  mod_file = import_module('modules.' + i.lower() + '.' + i.lower())
  mod_class = getattr(mod_file, i)()
  modules[i.lower()] = mod_class


router = APIRouter()


# event routes
@router.get("/api/core/event/start/")
async def core_event_start(background_tasks: BackgroundTasks):
  #await modules['core'].event.Start()
  background_tasks.add_task(modules['core'].event.Start)
  resp = { 'message' : 'cgate daemon: started' }
  return resp


@router.get('/api/core/event/stop/')  
async def core_event_stop():
  resp = modules['core'].event.Stop()
  resp = { 'message' : 'event daemon: stopped' }
  return resp


@router.get('/api/core/event/state/')  
def core_event_state():
  resp = modules['core'].event.State()
  return resp


@router.get('/api/core/event/status/')  
def core_event_status():
  resp = modules['core'].event.Status()
  return resp


# ws routes
@router.websocket("/ws/core/{client_id}/")
async def core_ws_start(websocket: WebSocket, client_id: int):
  await modules['core'].ws.Start(websocket, client_id)


@router.get('/api/core/ws/broadcast/{q}/')
async def core_ws_broadcast(q: str):
  await modules['core'].ws.Broadcast(q)
  return { 'message' : 'sent' }


@router.get('/app/core/ws/test/')
def core_ws_test():
  resp = modules['core'].ws.TestHtml()
  return HTMLResponse(resp)


# redis routes
@router.get('/app/core/redis/set/{q}/')
def core_redis_set(q: str):
  modules['core'].redis.Set('foo', q)
  return HTMLResponse('set to ' + q)


@router.get('/app/core/redis/get/')
def core_redis_get():
  resp = modules['core'].redis.JGet('cgate_state')
  return resp








