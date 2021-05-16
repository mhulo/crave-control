from main.main_common import *

class CoreAction:

  # core actions
  async def DelayMs(self, data):
    await asyncio.sleep(int(data['time_ms'])/1000)
    return { 'slept' : data['time_ms'] }


  async def SetDeviceVal(self, data):

    # grab the devices and params
    # grab the devices module and address from devices_conf
    # for each device run SetDevice for given module/address

    act_meth = 'SetDevice'
    acts = []
    
    for d in data['devices']:
      d_arr = d.split('.')
      device = devices_conf[d_arr[0]][d_arr[1]]
      act_data = { 'device': d, **device, **data['params'] }
      act_mod = data['modules'][d_arr[0]]
      act_obj = getattr(act_mod, act_meth)
      is_async = inspect.iscoroutinefunction(act_obj)

      if (is_async == True):
        resp = await act_obj(act_data)
      else:
        resp = act_obj(act_data)

      a = {}
      a['data'] = act_data
      a['response'] = resp
      acts.append(a)
      await asyncio.sleep(0.01)

    ret_val = {}
    ret_val['cmd'] = data['cmd']
    ret_val['act_data'] = act_data
    ret_val['sub_actions'] = acts
    
    
    #data['modules'] = None
    #return data
    return ret_val



