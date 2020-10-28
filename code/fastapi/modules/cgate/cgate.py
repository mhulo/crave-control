from main.main_imports import *

class Cgate:

  def __init__(self):
    self.host = 'cgate' # cgate host name / IP address
    self.change_port = 20025 # cgate load change port
    self.command_port = 20023 # cgate command port
    self.project = 'NET1' # cgate project name as set up in cgate config xml file
    self.network = '254' # the number of your network for this interface
    self.app = '56' # the app for the lighting network - will expand to other apps in future
    ######
    self.event_timeout = .001
    self.command_timeout = 1
    self.mod_name = 'cgate'
    self.daemon_key = self.mod_name + '_daemon'
    self.state_key = self.mod_name + '_state'
    self.redis = Request.state.redis
    self.ws = Request.state.ws


  def SetBrightness(self, data):
    level = round(int(data['set_val']) * (255/100))
    msg = 'RAMP //' + self.DeviceIdToCgateId(data['device_id']) + ' ' + str(level) + ' ' + str(data['ramp_time']) + 's'
    resp_text = self.Send(msg)
    ret_val = { msg : self.CgateToJson(resp_text) }
    return ret_val


  def SetPower(self, data):
    if (int(data['set_val']) == 100):
      level = 'ON'
    else:
      level = 'OFF'
    msg = level + ' //' + self.DeviceIdToCgateId(data['device_id'])
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
    self.redis.HSet('state', { self.mod_name : '' })
    retries = 0
    max_retries = 1 # fail fast if cant connect first go - could be config issue. 
    updated_ts = 0
    checked_ts = 0
    cached_state = '{{}}' #json string
    while ((retries < max_retries) and (this_id == instance_id)):
      try:
        with Telnet(self.host, self.change_port) as conn:
          max_retries = 10
          while (this_id == instance_id):
            updated_diff = time() - updated_ts
            checked_diff = time() - checked_ts
            resp = self.Read(conn, self.event_timeout)
            if ((resp != '') or (updated_diff < 10) or (checked_diff > 100)):
              state = json.dumps(self.State())
              checked_ts = time()
              if (state != cached_state): # comparison of json strings
                updated_ts = time()
                self.redis.HSet('state', { self.mod_name : state })
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
    self.redis.HSet('state', { self.mod_name : '{'+'}' })


  def Status(self):
    ret_val = self.redis.GetStatus(self.daemon_key)
    return ret_val


  def State(self):
    msg = 'GET //' + self.project + '/' + self.network + '/' + self.app + '/* LEVEL'
    resp_text = self.Send(msg)
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Ping(self):
    msg = 'NOOP'
    resp_text = self.Send(msg)
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Send(self, msg):
    with Telnet() as conn:
      try:
        conn.open(self.host, self.command_port)
        resp1 = self.Read(conn, self.command_timeout) # read welcome msg
        conn.write((msg + '\r\n').encode('utf-8'))
        resp2 = self.Read(conn, self.command_timeout) # read resp msg
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
        if ('LEVEL=' in row):
          pos1 = row.index('//')+2
          pos2 = row.index(':')
          pos3 = row.index('L=')+2
          row_id = 'cgate__' + row[pos1:pos2].replace('/', '_') + '__level'
          row_level = round(int(row[pos3:]) * (100/255))
          if (row_level > 100): row_level = 100
          if (row_level < 0): row_level = 0
          resp[row_id] = str(row_level)
        else:
          resp[i] = row
          i += 1
    return resp


  def DeviceIdToCgateId(self, device_id):
    resp = device_id.replace('_', '/')
    return resp

