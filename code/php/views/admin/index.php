<!DOCTYPE html>
<html>
<head>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <!-- for jquery -->
<script language="javascript" type="text/javascript">  
	$(document).ready(function(){

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

		$('#advair_start').click(function() {
		  $.ajax({url: "/code/src/interfaces/advair_ma5/advair_ma5_launcher.php?interface=advair_ma5&action=start", success: function(result){
		    alert(result);
		  }});
		});
		$('#advair_stop').click(function() {
		    $.ajax({url: "/code/src/interfaces/advair_ma5/advair_ma5_launcher.php?interface=advair_ma5&action=stop", success: function(result){
		  }});
		});

	});
</script>

</head>
<body>
	<table border="1">
		<tr>
			<td>Interface</td>
			<td width="100"></td>
			<td width="100"></td>
			<td width="100"></td>
			<td width="100"></td>
		</tr>
		<tr>
			<td>C-bus C-Gate</td>
			<td align="center"><button id="cgate_start">Start</button></td>
			<td align="center"><button id="cgate_stop">Stop</button></td>
			<td align="center"><button id="cgate_noop">Test</button></td>
			<td align="center"><button id="cgate_levels">Levels</button></td>
		</tr>
		<tr>
			<td>Advantage-Air MyAir5</td>
			<td align="center"><button id="advair_start">Start</button></td>
			<td align="center"><button id="advair_stop">Stop</button></td>
			<td align="center"></td>
			<td align="center"></td>
		</tr>
	</table>

</body>
</html>