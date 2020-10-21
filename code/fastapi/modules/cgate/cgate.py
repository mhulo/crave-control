from main.main_imports import *

class Cgate:

  def __init__(self):
    self.event_timeout = .001
    self.command_timeout = 1
    self.mod_name = 'cgate'
    #####
    self.daemon_key = self.mod_name + '_daemon'
    self.state_key = self.mod_name + '_state'
    self.redis = Request.state.redis
    self.ws = Request.state.ws


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
        with Telnet('cgate', 20025) as conn:
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
    cmd = 'get //NET1/254/56/* level'
    resp_text = self.Send(cmd)
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Ping(self):
    cmd = 'noop'
    resp_text = self.Send(cmd)
    ret_val = self.CgateToJson(resp_text)
    return ret_val


  def Send(self, cmd):
    with Telnet() as conn:
      try:
        conn.open('cgate', 20023)
        resp1 = self.Read(conn, self.command_timeout) # read welcome msg
        conn.write((cmd + '\r\n').encode('utf-8'))
        resp2 = self.Read(conn, self.command_timeout) # read resp from cmd
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
      if (row != ''):
        if ('level=' in row):
          pos1 = row.index('//')+2
          pos2 = row.index(':')
          pos3 = row.index('l=')+2
          row_id = 'cgate__' + row[pos1:pos2].replace('/', '_') + '__level'
          row_level = round(int(row[pos3:]) * (100/255))
          if (row_level > 100): row_level = 100
          if (row_level < 0): row_level = 0
          resp[row_id] = str(row_level)
        else:
          resp[i] = row
          i += 1
    return resp

