from main.main_imports import *

class Cgate:

  def __init__(self):
    self.redis = Request.state.redis
    self.ws = Request.state.ws
    self.event_timeout = .001
    self.command_timeout = 2


  # wait for cgate updates and then load state to redis
  async def Start(self):
    instance_id = str(time())
    self.redis.Set('cgate.daemon_id', instance_id)
    daemon_id = instance_id
    last_change = 0
    cached_state = '' #json string
    with Telnet() as conn:
      try:
        conn.open('cgate', 20025)
        while (daemon_id == instance_id):
          last_change_diff = time() - last_change
          resp = self.Read(conn, self.event_timeout)
          if ((resp != '') or (last_change_diff < 10) or (last_change_diff > 100)):
            state = json.dumps(self.State())
          if (state != cached_state): # comparison of json strings
            self.redis.Set('cgate.state', state)
            cached_state = state
            last_change = time()
          daemon_id = self.redis.Get('cgate.daemon_id')
          if (last_change_diff < 10):
            await asyncio.sleep(0.2) # 200ms
          else:
            await asyncio.sleep(2) # 2s (sleep mode)          
        return { 'message' : 'ws server stopped', 'iid' : instance_id, 'did' : daemon_id }
      except Exception as e:
        return { 'message' : 'error: ' + str(e) + ' could not connect to host/port' }


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

