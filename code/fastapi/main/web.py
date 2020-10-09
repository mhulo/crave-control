from main.web_imports import *

from modules.cgate import cgate_routes

app = FastAPI(debug=True)

app.include_router(cgate_routes.router)

