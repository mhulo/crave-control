import telnetlib

class Cgate:

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


  def TestHtml(self):

    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
    return html





