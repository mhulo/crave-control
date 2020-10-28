from main.main_imports import *
from modules.cgate.cgate import *


router = APIRouter()
cgate = Cgate()


@router.get('/api/cgate/start/')
async def cgate_start(background_tasks: BackgroundTasks):
  background_tasks.add_task(cgate.Start)
  resp = { 'message' : 'cgate daemon: started' }
  return resp


@router.get('/api/cgate/stop/')  
async def cgate_stop():
  resp = cgate.Stop()
  resp = { 'message' : 'cgate daemon: stopped' }
  return resp


@router.get('/api/cgate/state/')  
def cgate_state():
  resp = cgate.State()
  return resp


@router.get('/api/cgate/status/')  
def cgate_status():
  resp = cgate.Status()
  return resp


@router.get('/api/cgate/ping/')  
def cgate_ping():
  resp = cgate.Ping()
  return resp



