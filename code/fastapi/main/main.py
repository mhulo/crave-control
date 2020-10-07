from main.main_imports import *

from modules.cgate import cgate_router

app = FastAPI(debug=True)

app.include_router(cgate_router.router)

