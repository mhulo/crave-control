from main.main_imports import *
from .classes.core_event import *

class Core:

  def __init__(self):
    self.redis = Request.state.redis
    self.ws = Request.state.ws
    self.event = CoreEvent()



