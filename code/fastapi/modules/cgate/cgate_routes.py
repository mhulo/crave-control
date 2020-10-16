from main.main_imports import *
from modules.cgate.cgate import *


router = APIRouter()
cgate = Cgate()


@router.get("/api/cgate/start/")
async def cgate_start():
  resp = await cgate.Start()
  return resp


@router.get('/api/cgate/state/')  
def cgate_state():
  resp = cgate.State()
  return resp


@router.get('/api/cgate/ping/')  
def cgate_ping():
  resp = cgate.Ping()
  return resp



