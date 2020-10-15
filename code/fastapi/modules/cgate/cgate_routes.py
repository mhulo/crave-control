from main.main_imports import *
from .classes.cgate import *


router = APIRouter()


@router.get("/api/cgate/start/")
async def cgate_start():
  resp = await Cgate().Start()
  return resp


@router.get('/api/cgate/levels/')  
def cgate_levels():
  resp = Cgate().Levels()
  return resp


@router.get('/api/cgate/ping/')  
def cgate_ping():
  resp = Cgate().Ping()
  return resp



