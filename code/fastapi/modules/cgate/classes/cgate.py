from main.main_imports import *
 

class Cgate:

  def __init__(self):
    self.rc = CoreRedis()
    self.wss = CoreWss()


  async def StartDaemon(self):

    daemon_id = str(time())
    self.rc.Set('cgate_daemon_id', daemon_id)
    instance_id = daemon_id
    cached_val_data = {}

    while (instance_id == daemon_id):
      change_data = await self.data_changed()
      latest_val_data = await self.send_updates(cached_val_data)
      instance_id = change_data['cgate_daemon_id']
      cached_val_data = latest_val_data

    return { 'message' : 'ws server stopped', 'iid' : instance_id, 'did' : daemon_id }


  def LevelsShow(self):

    #cmd = 'noop'
    cmd = 'get //NET1/254/56/* level'

    resp_text = self.CommandSend(cmd)
    resp_json = self.CgateToJson(resp_text)

    return resp_json


  def CommandSend(self, cmd):

    # connect
    cr = '\r\n'
    bcr = b'\r\n'
    timeout = 10 #seconds

    tn = telnetlib.Telnet('cgate', 20023)

    # read welcome message
    resp1 = tn.read_until(bcr,timeout).decode('utf-8')

    # send command
    cmd = cmd + cr
    tn.write(cmd.encode('utf-8'))

    last_line = False
    resp2 = ''

    # read response to command
    while (last_line == False):
      read_buffer = tn.read_until(bcr,timeout).decode('utf-8')
      if ('-' not in read_buffer):
        last_line = True # // ie. last line has no '-' ie '300 //' not '300-//'
      resp2 += read_buffer

    tn.close()

    return resp2


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








