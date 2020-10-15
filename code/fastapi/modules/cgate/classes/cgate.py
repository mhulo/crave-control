from main.main_imports import *
from modules.core.classes.core_state import * 

class Cgate:

  def __init__(self):
    self.redis = Request.state.core_redis
    self.ws = Request.state.core_ws
    self.event_timeout = .001
    self.command_timeout = 2


  def Levels(self):

    cmd = 'get //NET1/254/56/* level'
    resp_text = self.Send(cmd)
    if ('error:' in resp_text):
      ret_val =  { 'message' : resp_text }
    else:
      #ret_val = self.CgateToJson(resp_text)
      ret_val = { 'message': resp_text }
    return ret_val


  def Ping(self):

    cmd = 'noop'
    resp = self.Send(cmd).replace('\r\n', '')
    ret_val = { 'message' : resp }
    return ret_val


  async def Start(self):

    instance_id = str(time())
    self.redis.Set('cgate_daemon_id', instance_id)
    daemon_id = instance_id
    cached_val_data = {}

    with Telnet() as conn:
      try:
        conn.open('cgate', 20025)
        while (daemon_id == instance_id):
          resp = self.Read(conn, self.event_timeout)
          if (resp != ''):
            await self.ws.Broadcast(f'cgate says: {resp}')
          daemon_id = self.redis.Get('cgate_daemon_id')
          await asyncio.sleep(0.2) # 200ms
        return { 'message' : 'ws server stopped', 'iid' : instance_id, 'did' : daemon_id }
      except Exception as e:
        return { 'message' : 'error: ' + str(e) + ' could not connect to host/port' }


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

    levels = {}
    text_arr = cgate_text.split('\r\n')
    for row in text_arr:
      if (row != ''):
        pos1 = row.index('//')+2
        pos2 = row.index(':')
        pos3 = row.index('l=')+2
        row_id = 'cgate__' + row[pos1:pos2].replace('/', '_') + '__level'
        row_level = row[pos3:]
        levels[row_id] = row_level

    return levels

