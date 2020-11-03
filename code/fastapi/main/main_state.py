from main.main_redis import *
from main.main_ws import *

class MainState:

  def __init__(self):
    self.redis = MainRedis()
    self.ws = MainWs(self.redis)
    self.ifx = None

