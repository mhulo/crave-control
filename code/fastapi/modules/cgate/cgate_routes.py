from main.main_common import *
from modules.cgate.cgate import *


router = APIRouter()


async def background_start(r):
  ifx = get_ifx(r)
  await Cgate(ifx).Start()


@router.get('/start/')
async def cgate_start(request: Request, background_tasks: BackgroundTasks):
  background_tasks.add_task(background_start, request)
  resp = { 'message' : 'cgate daemon: started' }
  return resp


@router.get('/stop/')  
async def cgate_stop(request: Request):
  ifx = get_ifx(request)
  resp = Cgate(ifx).Stop()
  resp = { 'message' : 'cgate daemon: stopped' }
  return resp


@router.get('/state/')
def cgate_state(request: Request):
  ifx = get_ifx(request)
  resp = Cgate(ifx).State()
  return resp


@router.get('/status/')  
def cgate_status(request: Request):
  ifx = get_ifx(request)
  resp = Cgate(ifx).Status()
  return resp


@router.get('/ping/')  
def cgate_ping(request: Request):
  ifx = get_ifx(request)
  resp = Cgate(ifx).Ping()
  return resp


