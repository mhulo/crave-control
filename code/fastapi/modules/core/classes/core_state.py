from modules.core.classes.core_redis import *
from modules.core.classes.core_ws import *

class CoreState:

  def __init__(self):
    self.core_redis = CoreRedis()
    self.core_ws = CoreWs(self.core_redis)

