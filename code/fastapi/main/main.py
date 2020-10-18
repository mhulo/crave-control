from main.main_imports import *
from main.main_settings import *

# load redis and websockets into state for all modules to use
from main.main_state import *
Request.state = MainState()

app = FastAPI(debug=True)

# autoload routers listed in main_settings
for i in active_modules:
  mod_file = import_module('modules.' + i.lower() + '.' + i.lower() + '_routes')
  app.include_router(mod_file.router)


