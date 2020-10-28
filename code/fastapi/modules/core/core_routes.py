from main.main_imports import *
from main.main_settings import *

# autoload modules in main_settings so that core 
# can access everything required for the actions
modules = {}
for i in active_modules:
  mod_file = import_module('modules.' + i.lower() + '.' + i.lower())
  mod_class = getattr(mod_file, i)()
  modules[i.lower()] = mod_class


router = APIRouter()
templates = Jinja2Templates(directory='modules/core/templates')


# app (view) routes
@router.get('/app/', response_class=HTMLResponse)
async def core_index(request: Request):
    return templates.TemplateResponse('index.html', { 'request': request })


@router.get('/app/admin/', response_class=HTMLResponse)
async def core_admin(request: Request):
    return templates.TemplateResponse('admin.html', { 'request': request })


@router.get('/app/ws_test/', response_class=HTMLResponse)
async def core_ws_test(request: Request):
    return templates.TemplateResponse('ws_test.html', { 'request': request })


# wss routes
@router.websocket("/wss/core/{client_id}/")
async def core_ws_start(websocket: WebSocket, client_id: int):
  await modules['core'].ws.Start(websocket, client_id)


# api routes
@router.get("/api/core/run_command/")
async def core_run_command(request: Request):
  ret_val = await modules['core'].RunCommand(request, modules)
  return ret_val


@router.get("/api/core/widgets_conf/")
def core_widgets_conf():
  return modules['core'].WidgetsConf()


@router.get("/api/core/event/start/")
async def core_event_start(background_tasks: BackgroundTasks):
  background_tasks.add_task(modules['core'].event.Start)
  resp = { 'message' : 'event daemon: started' }
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


@router.get('/api/core/ws/broadcast/{q}/')
async def core_ws_broadcast(q: str):
  await modules['core'].ws.Broadcast(q)
  return { 'message' : 'sent' }


