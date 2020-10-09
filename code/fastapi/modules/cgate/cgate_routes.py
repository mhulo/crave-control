from main.web_imports import *
from .classes.cgate import *


rc = RedisCache()
router = APIRouter()


@router.get('/api/cgate/test1/{q}/')
def CgateTest1(q: str):
  x = Cgate().Test(q)
  return { 'val' : x }  


@router.get('/api/cgate/test2/')
def CgateTest2():
  bar = {}
  bar['aa'] = 'ee'
  bar['xx'] = 'ss'
  rc.JSet('foo', bar)
  x = rc.JGet('foo')

  return { "val" : x }


@router.get('/api/cgate/test3/')
async def CgateTest3():
  html = '<html><body><h1>Look hey! HTML!</h1></body></html>'
  return HTMLResponse(html)


@router.get('/api/cgate/levels/')  
def CgateLevelsShow():
  return Cgate().LevelsShow()


@router.get('/app/ws/')
async def WsView():
  html = Cgate().TestHtml()
  return HTMLResponse(html)


@router.get('/app/redis/set/{q}/')
def WsSet(q: str):
  rc.Set('foo', q)
  return HTMLResponse('set to ' + q)


@router.get('/app/redis/get/foo/')
def WsGet():
  q = rc.Get('foo')
  return HTMLResponse('foo=' + q)


@router.get('/app/redis/get/ts/')
def WsGet():
  q = rc.Get('ts')
  return HTMLResponse('ts=' + q)







