from main.main_imports import *
from .classes.core_event import *
from .classes.core_action import *

from modules.core.config.commands_conf import * 
from modules.core.config.widgets_conf import *


class Core:

  def __init__(self):
    self.redis = Request.state.redis
    self.ws = Request.state.ws
    self.event = CoreEvent()
    self.action = CoreAction()


  def CommandRun(self, request, modules):
    ret_val = {}
    cmd = request.query_params['cmd']
    i = 1
    for action in commands_conf[cmd]['actions']:
      method = action['method'].split('@')
      ret_val[i] = getattr(modules[method[0]], method[1])({**action['params'], **request.query_params})

    return ret_val


  def WidgetsConf(self):
    ret_val = { 'aa' : 'conf' }
    return widgets_conf



