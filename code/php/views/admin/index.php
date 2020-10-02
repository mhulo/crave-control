<!DOCTYPE html>
<html>
<head>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <!-- for jquery -->
<script language="javascript" type="text/javascript">  
	$(document).ready(function(){

		$('#ws_start').click(function() {
		  $.ajax({url: "/api/websockets/start", success: function(result){
		    alert(result);
		   }});
		});
		$('#ws_stop').click(function() {
		  $.ajax({url: "/api/websockets/stop", success: function(result){
		    alert(result);
		   }});
		});

		$('#cgate_start').click(function() {
		  $.ajax({url: "/api/cgate/start", success: function(result){
		    alert(result);
		   }});
		});
		$('#cgate_stop').click(function() {
		  $.ajax({url: "/api/cgate/stop", success: function(result){
		    alert(result);
		   }});
		});
		$('#cgate_noop').click(function() {
		  $.ajax({url: "/api/cgate/noop", success: function(result){
		    alert(result);
		   }});
		});
		$('#cgate_levels').click(function() {
		  $.ajax({url: "/api/cgate/levels", success: function(result){
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
			<td>Websockets</td>
			<td align="center"><button id="ws_start">Start</button></td>
			<td align="center"><button id="ws_stop">Stop</button></td>
			<td align="center"></td>
			<td align="center"></td>
		</tr>
		<tr>
			<td>Clipsal C-Bus [cgate]</td>
			<td align="center"><button id="cgate_start">Start</button></td>
			<td align="center"><button id="cgate_stop">Stop</button></td>
			<td align="center"><button id="cgate_noop">Test</button></td>
			<td align="center"><button id="cgate_levels">Levels</button></td>
		</tr>
		<tr>
			<td>Philips Hue [hue]</td>
			<td align="center"><button id="hue_start">Start</button></td>
			<td align="center"><button id="hue_stop">Stop</button></td>
			<td align="center"></td>
			<td align="center"><button id="hue_levels">Levels</button></td>
		</tr>
	</table>

</body>
</html>