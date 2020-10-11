from main.main_imports import *
from .classes.cgate import *


router = APIRouter()


@router.get('/app/cgate/get/')  
def cgate_ping():
  resp = CoreRedis().Get('wss_clients')
  return HTMLResponse(resp)


@router.get("/api/cgate/start/")
async def cgate_start_daemon():
  resp = await Cgate().StartDaemon()
  return resp


@router.get('/api/cgate/levels/')  
def cgate_levels_show():
  resp = Cgate().LevelsShow()
  return resp


