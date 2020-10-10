from main.main_imports import *

from modules.core import core_routes
from modules.cgate import cgate_routes

app = FastAPI(debug=True)

app.include_router(core_routes.router)
app.include_router(cgate_routes.router)

