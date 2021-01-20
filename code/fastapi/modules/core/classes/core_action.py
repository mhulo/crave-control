from main.main_common import *

class CoreAction:

  # core actions
  async def DelayMs(self, data):
    await asyncio.sleep(int(data['time_ms'])/1000)
    return { 'slept' : data['time_ms'] }


  async def SetCardVal(self, data):

    # grab the devices and command params from the cards_conf
    # grab the devices module and address from devices_conf
    # for each device run SetDevice for given module/address

    act_meth = 'SetDevice'
    card = cards_conf[data['wgt']]
    acts = []
    for d in card['devices']:
      d_arr = d.split('.')
      device = devices_conf[d_arr[0]][d_arr[1]]
      if ('command_params' in card):
        params = to_dict(card['command_params'])
      else:
        params = {}
      act_data = { 'device': d, **device, **params, data['set_key']: data['set_val']}
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
    ret_val['label'] = card['label']
    ret_val['command'] = data['cmd']
    ret_val['card'] = data['wgt']
    ret_val['sub_actions'] = acts
    return ret_val

    #ret_val['debug_data'] = { **card, **data }
    #return data



