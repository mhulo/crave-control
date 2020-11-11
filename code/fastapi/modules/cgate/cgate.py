from main.main_common import *

class Cgate:

  def __init__(self, ifx):
    self.conf = get_interface_conf(ifx)
    self.daemon_key = self.conf['interface'] + '_daemon'
    self.state_key = self.conf['interface'] + '_state'
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
    return ret_val


  def SetBrightness(self, data):
    level = round(int(data['brightness']) * (255/100))
    if ('ramp_time' in data):
      ramp_time = data['ramp_time']
    else:
      ramp_time = self.conf['ramp_time']
    msg = 'ramp //' + self.DeviceIdToCgateId(data['address']) + ' ' + str(level) + ' ' + str(ramp_time) + 's'
    resp_text = self.Send(msg)
    ret_val = { msg : self.CgateToJson(resp_text) }
    return ret_val


  def SetPower(self, data):
    level = str(data['power']).lower()
    msg = level + ' //' + self.DeviceIdToCgateId(data['address'])
    resp_text = self.Send(msg)
    ret_val = { msg : self.CgateToJson(resp_text) }
    return ret_val


  # wait for updates and then load state to redis
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    instance_id = started_ts
    self.redis.HSet(self.daemon_key, { 'instance_id' : instance_id , 'started_ts' : started_ts })
    self.redis.HSet(self.daemon_key, { 'message' : 'started',  'loop_ts' : str(time()) })
    self.redis.HSet('state', { self.conf['interface'] : '' })
    retries = 0
    max_retries = 1 # fail fast if cant connect first go - could be config issue. 
    updated_ts = 0
    checked_ts = 0
    cached_state = '{{}}' #json string
    while ((retries < max_retries) and (this_id == instance_id)):
      try:
        with Telnet(self.conf['host'], self.conf['change_port']) as conn:
          max_retries = 10
          while (this_id == instance_id):
            updated_diff = time() - updated_ts
            checked_diff = time() - checked_ts
            resp = self.Read(conn, self.conf['event_timeout'])
            if ((resp != '') or (updated_diff < 10) or (checked_diff > 100)):
              state = json.dumps(self.State())
              checked_ts = time()
              if (state != cached_state): # comparison of json strings
                updated_ts = time()
                self.redis.HSet('state', { self.conf['interface'] : state })
                cached_state = state
            instance_id = self.redis.HGet(self.daemon_key, 'instance_id')
            self.redis.HSet(self.daemon_key, { 'loop_ts' : str(time()) })
            if (updated_diff < 600):
              await asyncio.sleep(0.5) # 500ms
            else:
              await asyncio.sleep(1.5) # 1.5s (sleep mode)
            retries = 0
      except Exception as e:
        self.redis.HSet(self.daemon_key, { 'message' : 'error - ' + str(e) + ' could not connect to host/port' })
        instance_id = self.redis.HGet(self.daemon_key, 'instance_id')
        retries += 1
        await asyncio.sleep(2)


  def Stop(self):
    self.redis.HSet(self.daemon_key, { 'instance_id' : '0',  'message' : 'stopped' })
    self.redis.HSet('state', { self.conf['interface'] : '{'+'}' })


  def Status(self):
    ret_val = self.redis.GetStatus(self.daemon_key)
    return ret_val


  def State(self):
    ret_val = {}
    ifx_vals = self.StateRaw()
    for k, v in devices_conf[self.conf['interface']].items():
      ret_val[k] = {}
      ret_val[k]['address'] = v['address']
      if ('level' in ifx_vals[v['address']]):
        ret_val[k]['power'] = self.LevelToPower(ifx_vals[v['address']]['level'])
        ret_val[k]['brightness'] = round(int(ifx_vals[v['address']]['level']) * (100/255))   
    return ret_val


  def StateRaw(self):
    ret_val = {}
    msg = 'get //' + self.conf['project'] + '/' + self.conf['network'] + '/' + self.conf['app'] + '/* level'
    resp_text = str(self.Send(msg))
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Ping(self):
    msg = 'noop'
    resp_text = self.Send(msg)
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Send(self, msg):
    with Telnet() as conn:
      try:
        conn.open(self.conf['host'], self.conf['command_port'])
        resp1 = self.Read(conn, self.conf['command_timeout']) # read welcome msg
        conn.write((msg + '\r\n').encode('utf-8'))
        resp2 = self.Read(conn, self.conf['command_timeout']) # read resp msg
        ret_val = resp2
      except Exception as e:
        ret_val = { 'message' : 'error: ' + str(e) + ' could not connect to host/port' }
      return ret_val


  def Read(self, conn, timeout):
    bcr = b'\r\n'
    resp = ''
    read_more = True
    lines = 0
    while ((read_more == True) and (lines < 1000)):
      try:
        read_buffer = conn.read_until(bcr,timeout).decode('utf-8')
      except:
        read_buffer = ''
      resp += read_buffer
      if ((read_buffer == '') or ('-//' not in read_buffer)):
        read_more = False
      lines += 1
    return resp


  def CgateToJson(self, cgate_text):
    i = 1
    resp = {}
    text_arr = cgate_text.split('\r\n')
    for row in text_arr:
      row = row.upper()
      if (row != ''):
        if ('level=' in row.lower()):
          pos1 = row.index('//')+2
          pos2 = row.index(':')
          pos3 = row.index('L=')+2
          row_id = row[pos1:pos2].replace('/', '_')
          row_level = int(row[pos3:])
          if (row_level > 255): row_level = 255
          if (row_level < 0): row_level = 0
          resp[row_id] = {}
          resp[row_id]['level'] = str(row_level)
        else:
          resp[i] = row
          i += 1
    return resp


  def DeviceIdToCgateId(self, device_id):
    resp = device_id.replace('_', '/')
    return resp


  def LevelToPower(self, level):
    pwr = 'off'
    if (int(level) > 0):
      pwr = 'on'
    return pwr

