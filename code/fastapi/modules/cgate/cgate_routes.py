from main.main_imports import *
from .classes.cgate import *


router = APIRouter()


@router.get('/app/cgate/get/')  
def cgate_ping():
  resp = CoreRedis().Get('wss_clients')
  return HTMLResponse(resp)


@router.get("/api/cgate/start/")
async def cgate_start():
  resp = await Cgate().Start()
  return resp


@router.get('/api/cgate/levels/')  
def cgate_levels_show():
  resp = Cgate().LevelsShow()
  return resp


@router.get('/api/cgate/change/')  
async def cgate_changed():
  resp = await Cgate().Changed()
  return { 'cgate said' : resp }


