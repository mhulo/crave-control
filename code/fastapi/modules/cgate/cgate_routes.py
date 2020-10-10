from main.main_imports import *
from .classes.cgate import *


router = APIRouter()


@router.get('/app/cgate/wstest/')
def CgateWsTest():
  resp = Cgate().WsTest()
  return HTMLResponse(resp)


@router.get('/app/cgate/get/')  
def CgatePing():
  resp = CoreRedis().Get('wss_clients')
  return HTMLResponse(resp)


@router.get("/api/cgate/start/")
async def cgate_start_daemon():
  resp = await Cgate().StartDaemon()
  return resp


@router.get('/api/cgate/levels/')  
def CgateLevelsShow():
  resp = Cgate().LevelsShow()
  return resp


