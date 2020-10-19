from main.main_imports import *
from views.views import *


router = APIRouter()
views = Views()

@router.get('/app/admin/')
def app_admin():
  resp = views.Admin()
  return HTMLResponse(resp)




