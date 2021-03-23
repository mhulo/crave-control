from main.main_common import *

# load redis and websockets into state for all modules to use
from main.main_state import *
Request.state = MainState()

app = FastAPI(debug=True)

hosts = ['localhost', '192.168.2.19', '192.168.2.20', '192.168.2.237']
origins = []
for host in hosts:
  origins += ['https://' + host, 'http://' + host + ':4000']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# autoload routers for active modules in modules_conf
for k, v in interfaces_conf.items():
  if (v['active'] == True):
    mod_file = import_module('modules.' + v['module_name'] + '.' + v['module_name'] + '_routes')
    mod_prefix = '/api/' + k
    app.include_router(mod_file.router, prefix=mod_prefix)


# commented out below because middleware breaks background
# tasks due to a starlette bug at the time of writing
# could use asyncio.create_task instead of background_task
#
# set the interface name as ifx in state based on the path
#@app.middleware('http')
#async def add_xx(request: Request, call_next):
#  ifx = ifx(request)
#  request.state.ifx = ifx
#  response = await call_next(request)
#  return response


# mount the core static dir
app.mount('/app/static', StaticFiles(directory='main/static'), name='core_static')
templates = Jinja2Templates(directory='main/templates')


# app (view) routes
@app.get('/app/', response_class=HTMLResponse)
async def app_index(request: Request):
    return templates.TemplateResponse('index.html', { 'request': request })


@app.get('/app/admin/', response_class=HTMLResponse)
async def app_admin(request: Request):
    return templates.TemplateResponse('admin.html', { 'request': request })


@app.get('/app/ws_test/', response_class=HTMLResponse)
async def app_ws_test(request: Request):
    return templates.TemplateResponse('ws_test.html', { 'request': request })


