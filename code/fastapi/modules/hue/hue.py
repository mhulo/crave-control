from main.main_common import *
from rgbxy import Converter
from rgbxy import GamutA
from rgbxy import GamutB
from rgbxy import GamutC
import math

class Hue:

  def __init__(self, ifx):
    self.conf = get_interface_conf(ifx)
    self.ifx_key = 'ifx_' + self.conf['interface']
    self.redis = Request.state.redis
    self.ws = Request.state.ws


  def SetDevice(self, data):
    ret_val = []
    if ('brightness' in data):
      resp = self.SetBrightness(data)
      ret_val.append(resp)
    if ('power' in data):
      resp = self.SetPower(data)
      ret_val.append(resp)
    if ('rgb' in data):
      resp = self.SetRgb(data)
      ret_val.append(resp)
  
    x = {}
    x['trace'] = data
    ret_val.append(x)

    return ret_val


  def SetBrightness(self, data):
    set_brightness = round(int(data['brightness']) * (254/100))
    if (set_brightness > 0):
      set_power = True
    else:
      set_power = False
    set_data = { 'bri' : set_brightness, 'on' : set_power }
    endpoint = 'lights/' + data['address'] + '/state'
    res = self.HitHue(endpoint, 'put', json.dumps(set_data))
    ret_val = res.json()
    return ret_val


  def SetPower(self, data):
    if (str(data['power']).lower() == 'on'):
      set_power = True
    else:
      set_power = False
    set_data = { 'on' : set_power }
    endpoint = 'lights/' + data['address'] + '/state'
    res = self.HitHue(endpoint, 'put', json.dumps(set_data))
    ret_val = res.json()
    return ret_val


  def SetRgb(self, data):
    set_xy = self.RgbToXy('c', data['rgb'])
    set_data = { 'xy' : set_xy }
    endpoint = 'lights/' + data['address'] + '/state'
    res = self.HitHue(endpoint, 'put', json.dumps(set_data))
    ret_val = res.json()
    return ret_val


  # wait for updates and then load state to redis
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    loop_id = started_ts
    self.redis.HSet(self.ifx_key, {
      'loop_id': loop_id ,
      'loop_ts': started_ts,
      'started_ts': started_ts,
      'updated_ts': started_ts,
      'message':  'started',
      'state': '{'+'}'
    })
    retries = 0
    max_retries = 1 # fail fast if cant connect first go - could be config issue. 
    updated_ts = 0
    cached_state = '{'+'}' #json string
    while ((retries < max_retries) and (this_id == loop_id)):
      loop_id = self.redis.HGet(self.ifx_key, 'loop_id')
      ifx_vals = self.StateRaw()
      if (ifx_vals.status_code == 200):
        retries = 0
        max_retries = 100
        updated_diff = time() - updated_ts
        state_raw = ifx_vals.json()
        state = json.dumps(self.ProcessState(state_raw))
        if (state != cached_state): # comparison of json strings
          updated_ts = time()
          self.redis.HSet(self.ifx_key, {
            'state' : state,
            'updated_ts' : updated_ts
          })
          self.redis.HSet('ifx_core', {
            'updated_ts' : updated_ts
          })
          cached_state = state

        self.redis.HSet(self.ifx_key, { 'loop_ts' : str(time()) })
        if (updated_diff < 600):
          await asyncio.sleep(0.5) # 500ms
        else:
          await asyncio.sleep(1.5) # 1.5s (sleep mode)
      else:
        self.redis.HSet(self.ifx_key, { 'message' : 'error - could not connect to bridge' })
        retries += 1
        await asyncio.sleep(retries) # will wait longer and longer if not connecting


  def Stop(self):
    self.redis.HSet(self.ifx_key, {
      'loop_id': '0',
      'message': 'stopped' ,
      'state': '{'+'}'
    })


  def Test(self):
    state = self.redis.GetState()
    device = 'hue.master_led_strip'
    device_arr = device.split('.')
    device_state = state[device_arr[0]][device_arr[1]]
    ret_val = device_state
    return ret_val


  def Status(self):
    ret_val = self.redis.GetStatus(self.daemon_key)
    return ret_val


  def State(self):
    ifx_vals = self.StateRaw()
    if (ifx_vals.status_code == 200):
      state_raw = ifx_vals.json()
      ret_val = self.ProcessState(state_raw)
    else:
      ret_val = { 'message' : 'error - could not connect to bridge' }  
    return ret_val


  def StateRaw(self):
    res = self.HitHue('lights/', 'get')
    ret_val = res
    return ret_val


  def ProcessState(self, state_raw):
    ret_val = {}
    ifx_vals = state_raw
    for k, v in devices_conf[self.conf['interface']].items():
      ret_val[k] = {}
      ret_val[k]['address'] = v['address']
      if ('state' in ifx_vals[v['address']]):
        # get power
        ret_val[k]['power'] = self.LevelToPower(ifx_vals[v['address']]['state']['on'])

        # get brightness
        ret_val[k]['brightness'] = 0
        if ('bri' in ifx_vals[v['address']]['state']):
          if (ret_val[k]['power'] == 'on'):
            ret_val[k]['brightness'] = round(int(ifx_vals[v['address']]['state']['bri']) * (100/255))

        # get color from xy and gamut
        ct = None
        xy = None
        gamut = None
        rgb = None
        if ('ct' in ifx_vals[v['address']]['state']):
          ct = ifx_vals[v['address']]['state']['ct']
        if ('xy' in ifx_vals[v['address']]['state']):
          xy = ifx_vals[v['address']]['state']['xy']
        if ('capabilities' in ifx_vals[v['address']]):
          if ('control' in ifx_vals[v['address']]['capabilities']):
            if ('colorgamuttype' in ifx_vals[v['address']]['capabilities']['control']):
              gamut = ifx_vals[v['address']]['capabilities']['control']['colorgamuttype']
        if ((xy != None) and (gamut != None)):
          rgb = self.XyToRgb(gamut, xy[0], xy[1])
        ret_val[k] = {
          **ret_val[k],
          'ct': ct, 
          'xy': xy,
          'gamut': gamut,
          'rgb': rgb
        }

    return ret_val


  def Ping(self):
    res = self.HitHue('config/', 'get')
    ret_val = res.json()
    return ret_val


  def HitHue(self, endpoint, typ, data=None):
    url = self.conf['bridge_url'] + endpoint
    headers = { 'Content-Type' : 'application/json;charset=utf-8' }
    if (typ == 'get'):
      resp = requests.get(url, headers=headers, verify=False)
    elif (typ == 'put'):
      resp = requests.put(url, data=data, headers=headers, verify=False)
    else:
      resp = requests.post(url, data=data, headers=headers, verify=False)
    return resp


  def LevelToPower(self, state):
    pwr = 'off'
    if (state == True):
      pwr = 'on'
    return pwr


  def GetGamut(self, gamut):
    if (gamut.lower() == 'a'):
      conv = Converter(GamutA)
    elif (gamut.lower() == 'c'):
      conv = Converter(GamutC)   
    else:
      conv = Converter(GamutB)
    return conv


  def XyToRgb(self, gamut, x, y):
    conv = self.GetGamut(gamut)
    rgb = conv.xy_to_rgb(x, y)
    return rgb


  def RgbToXy(self, gamut, rgb):
    conv = self.GetGamut(gamut)
    xy = conv.rgb_to_xy(*rgb)
    return xy

