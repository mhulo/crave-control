from main.main_common import *
from modules.hue.hue import *


router = APIRouter()


async def background_hue_start(r):
  ifx = get_ifx(r)
  await Hue(ifx).Start()


@router.get('/start/')
async def hue_start(request: Request, background_tasks: BackgroundTasks):
  background_tasks.add_task(background_hue_start, request)
  resp = { 'message' : 'hue daemon: started' }
  return resp


@router.get('/stop/')  
async def hue_stop(request: Request):
  ifx = get_ifx(request)
  resp = Hue(ifx).Stop()
  resp = { 'message' : 'hue daemon: stopped' }
  return resp


@router.get('/state/')
def hue_state(request: Request):
  ifx = get_ifx(request)
  resp = Hue(ifx).State()
  return resp


@router.get('/state_raw/')
def hue_state_raw(request: Request):
  ifx = get_ifx(request)
  resp = Hue(ifx).StateRaw().json()
  return resp


@router.get('/status/')  
def hue_status(request: Request):
  ifx = get_ifx(request)
  resp = Hue(ifx).Status()
  return resp


@router.get('/ping/')  
def hue_ping(request: Request):
  ifx = get_ifx(request)
  resp = Hue(ifx).Ping()
  return resp


