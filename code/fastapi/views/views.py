from main.main_imports import *

class Views:

  def Admin(self):

    html = """
<!DOCTYPE html>
<html>
<head>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <!-- for jquery -->
<script language="javascript" type="text/javascript">  
  $(document).ready(function(){

    $('#event_start').click(function() {
      $.ajax({url: "/api/core/event/start/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#event_stop').click(function() {
      $.ajax({url: "/api/core/event/stop/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#event_status').click(function() {
      $.ajax({url: "/api/core/event/status/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#event_state').click(function() {
      $.ajax({url: "/api/core/event/state/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });

    $('#cgate_start').click(function() {
      $.ajax({url: "/api/cgate/start/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#cgate_stop').click(function() {
      $.ajax({url: "/api/cgate/stop/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#cgate_status').click(function() {
      $.ajax({url: "/api/cgate/status/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });
    $('#cgate_state').click(function() {
      $.ajax({url: "/api/cgate/state/", success: function(result){
        alert(JSON.stringify(result));
       }});
    });

    $('#hue_start').click(function() {
      $.ajax({url: "/api/hue/start", success: function(result){
        alert(result);
       }});
    });
    $('#hue_stop').click(function() {
      $.ajax({url: "/api/hue/stop", success: function(result){
        alert(result);
       }});
    });
    $('#hue_levels').click(function() {
      $.ajax({url: "/api/hue/levels", success: function(result){
        alert(JSON.stringify(result));
       }});
    });

  });
</script>

</head>
<body>
  <table border="1">
    <tr>
      <td align="center">Interface</td>
      <td width="100"></td>
      <td width="100"></td>
      <td width="100"></td>
      <td width="100"></td>
    </tr>
    <tr>
      <td id="event_light">Event Listner [event]</td>
      <td align="center"><button id="event_start">Start</button></td>
      <td align="center"><button id="event_stop">Stop</button></td>
      <td align="center"><button id="event_status">Status</button></td>
      <td align="center"><button id="event_state">State</button></td>
    </tr>
    <tr>
      <td id="cgate_light">Clipsal C-Bus [cgate]</td>
      <td align="center"><button id="cgate_start">Start</button></td>
      <td align="center"><button id="cgate_stop">Stop</button></td>
      <td align="center"><button id="cgate_status">Status</button></td>
      <td align="center"><button id="cgate_state">State</button></td>
    </tr>
    <tr>
      <td>Philips Hue [hue]</td>
      <td align="center"><button id="hue_start">Start</button></td>
      <td align="center"><button id="hue_stop">Stop</button></td>
      <td align="center"></td>
      <td align="center"><button id="hue_levels">State</button></td>
    </tr>
  </table>

</body>
</html>
"""
    return html

