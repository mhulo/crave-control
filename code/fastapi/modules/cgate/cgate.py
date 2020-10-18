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


  # wait for cgate updates and then load state to redis
  async def Start(self):
    started_ts = str(time())
    this_id = started_ts
    instance_id = started_ts
    self.redis.HSet(self.daemon_key, { 'instance_id' : instance_id , 'started_ts' : started_ts })
    last_change = 0
    cached_state = '' #json string
    i = 0
    with Telnet() as conn:
      while (i < 10):
        try:
          conn.open('cgate', 20025)
          self.redis.HSet(self.daemon_key, { 'message' : 'started',  'last_iteration_ts' : str(time()) })
          while (this_id == instance_id):
            last_change_diff = time() - last_change
            resp = self.Read(conn, self.event_timeout)
            if ((resp != '') or (last_change_diff < 10) or (last_change_diff > 100)):
              state = json.dumps(self.State())
            if (state != cached_state): # comparison of json strings
              self.redis.HSet('state', { 'cgate' : state })
              cached_state = state
              last_change = time()
            instance_id = self.redis.HGet(self.daemon_key, 'instance_id')
            self.redis.HSet(self.daemon_key, { 'last_iteration_ts' : str(time()) })
            if (last_change_diff < 10):
              await asyncio.sleep(0.25) # 250ms
            else:
              await asyncio.sleep(2) # 2s (sleep mode)
        except Exception as e:
          self.redis.HSet(self.daemon_key, { 'message' : 'error - ' + str(e) + ' could not connect to host/port' })
        i += 1
        await asyncio.sleep(2) # 2s


  def Stop(self):
    self.redis.HSet('cgate_daemon', { 'instance_id' : '0',  'message' : 'stopped' })


  def Status(self):
    status = self.redis.HGetAll(self.daemon_key)
    if ('started_ts' in status):
      status['started_ts'] = datetime.fromtimestamp(float(status['started_ts']))
    if ('last_iteration_ts' in status):
      iteration_diff = time() - float(status['last_iteration_ts'])
      status['last_iteration_sec'] = iteration_diff
      if (iteration_diff < 10): # consider it running if last iteration is within 10 sec
        status['message'] = 'running'
      status['last_iteration_ts'] = datetime.fromtimestamp(float(status['last_iteration_ts']))
    ret_val = { self.daemon_key : status }
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
          row_level = row[pos3:]
          resp[row_id] = row_level
        else:
          resp[i] = row
          i += 1
    return resp

