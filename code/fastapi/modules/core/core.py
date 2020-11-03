from main.main_common import *
from .classes.core_event import *
from .classes.core_action import *


class Core:

  def __init__(self, ifx):
    self.conf = get_interface_conf(ifx)
    self.redis = Request.state.redis
    self.ws = Request.state.ws
    self.event = CoreEvent()
    self.action = CoreAction()


  async def RunAction(self, modules, module, act_meth, data):
    if (module == 'core'):
      act_mod = getattr(modules['core'], 'action')
    else:
      act_mod = modules[module]

    act_obj = getattr(act_mod, act_meth)
    is_async = inspect.iscoroutinefunction(act_obj)

    if (is_async == True):
      ret_val = await getattr(act_mod, act_meth)(data)
    else:
      ret_val = getattr(act_mod, act_meth)(data)

    await asyncio.sleep(0.01)

    return ret_val


  async def RunCommand(self, request, modules):
    ret_val = {}
    cmd = request.query_params['cmd']
    i = 1

    for action in commands_conf[cmd]['actions']:
      method = action['method'].split('@')
      ret_val[i] = await self.RunAction(modules, method[0], method[1], {**action['params'], **request.query_params})
      i += 1

    return ret_val


  def WidgetsConf(self):
    return widgets_conf


