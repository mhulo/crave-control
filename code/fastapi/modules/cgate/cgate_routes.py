from main.main_common import *
from modules.cgate.cgate import *


router = APIRouter()


async def background_start(ifx):
  await Cgate(ifx).Start()


@router.get('/start/')
async def background_start(background_tasks: BackgroundTasks):
  background_tasks.add_task(background_start, Request.state.ifx)
  resp = { 'message' : 'cgate daemon: started' }
  return resp


@router.get('/stop/')  
async def cgate_stop():
  resp = Cgate(Request.state.ifx).Stop()
  resp = { 'message' : 'cgate daemon: stopped' }
  return resp


@router.get('/state/')
def cgate_state():
  resp = Cgate(Request.state.ifx).State()
  return resp


@router.get('/status/')  
def cgate_status():
  resp = Cgate(Request.state.ifx).Status()
  return resp


@router.get('/ping/')  
def cgate_ping():
  resp = Cgate(Request.state.ifx).Ping()
  return resp




