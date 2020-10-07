from main.main_imports import *
from .classes.cgate import *


rc = RedisCache()
router = APIRouter()


@router.get('/api/cgate/test1/{q}/')
def CgateTest1(q: str):
  x = Cgate().Test(q)
  return { "val" : x }  


@router.get('/api/cgate/test2/')
def CgateTest2():
  bar = {}
  bar['aa'] = 'ee'
  bar['xx'] = 'yy'

  rc.JSet('foo', bar)
  x = rc.JGet('foo')

  return { "val" : x }


@router.get("/api/cgate/test3/", response_class=HTMLResponse)
async def CgateTest3():
  return '<html><body><h1>Look ma! HTML!</h1></body></html>'


@router.get('/api/cgate/levels/')  
def CgateLevelsShow():
  return Cgate().LevelsShow()


