from main.main_common import *


# autoload (create references to) modules in main_settings so that core 
# can access everything required for the actions
modules = {}
for k, v in interfaces_conf.items():
  if (v['active'] == True):
    mod_file = import_module('modules.' + v['module_name'] + '.' + v['module_name'])
    modules[k] = getattr(mod_file, to_classname(v['module_name']))(k)


router = APIRouter()


# wss routes
@router.websocket("/wss/{client_id}/")
async def core_ws_start(websocket: WebSocket, client_id: int):
  await modules['core'].ws.Start(websocket, client_id)


# api routes
@router.get("/run_command/")
async def core_run_command(request: Request):
  resp = await modules['core'].RunCommand(request, modules)
  return resp


@router.get("/cards_conf/")
def core_cards_conf():
  return modules['core'].CardsConf()


@router.get("/icons_conf/")
def core_icons_conf():
  return modules['core'].IconsConf()


@router.get('/state/')  
def core_event_state():
  resp = modules['core'].event.State()
  return resp


@router.get('/status/')  
def core_event_status():
  resp = modules['core'].event.Status()
  return resp


@router.get("/start/")
async def core_event_start(background_tasks: BackgroundTasks):
  background_tasks.add_task(modules['core'].event.Start)
  resp = { 'message' : 'event daemon: started' }
  return resp


@router.get('/start_debug/')  
async def core_event_start_debug():
  resp = await modules['core'].event.Start()
  resp = { 'message' : 'event daemon: started' }
  return resp


@router.get('/stop/')  
async def core_event_stop():
  resp = modules['core'].event.Stop()
  resp = { 'message' : 'event daemon: stopped' }
  return resp


@router.get('/ws/broadcast/{q}/')
async def core_ws_broadcast(q: str):
  await modules['core'].ws.Broadcast(q)
  return { 'message' : 'sent' }


@router.get('/redis/del/{hash_key}/')  
def core_event_status(hash_key: str):
  modules['core'].redis.HDel('state', hash_key)
  resp = { 'message' : 'redis hash ' + hash_key + ': deleted' }
  return resp


