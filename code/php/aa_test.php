<?php require_once "src/cards.php"; ?>
<?php require_once "config/websocket_config.php"; ?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="crave control web app.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>Crave Control</title>

    <script src="https://code.getmdl.io/1.3.0/material.min.js"></script> <!-- for mdl -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <!-- for jquery -->
    <script src="public/js/card_refresh_functions.js"></script>
    <script>

        function get_live_status(interface,refr) {        

            // get a refreshed set of values for the given interface at a certain refresh rate
            // can have different refresh rates for each interface

            switch(interface) {
                case 'advair_ma5':

                    //create a new websocket object.
                    advair_ma5_socket_uri = "ws://"+ws_host_addr+":"+ws_host_port_advair_ma5+"/interfaces/"+interface+"/"+interface+"_interface.php?"; 
                    advair_ma5_socket = new WebSocket(advair_ma5_socket_uri);

                    advair_ma5_socket.onopen = function(ev) { // connection is open 
                        console.log('socket connected to '+interface+' interface');
                    };

                    // message received on websocket from server
                    advair_ma5_socket.onmessage = function(ev) {
                        var result = JSON.parse(ev.data); // daemon via websocket sends json data
                        //$.each(result, function(i,field){
                        //    if ($('.'+i).val() != field) { // if the value from the network is different
                        console.log('change detected\n');
                        console.log(result);
                        //        $('.'+i).val(field); // update it
                        // address would be advair_ma5__ac1_z01
                        var temp = result['aircons']['ac1']['info']['setTemp'];
                        var z1_damper = result['aircons']['ac1']['zones']['z01']['value'];
                        $('#res').html('res='+z1_damper);
                        //    }
                        //});
                    };

                    advair_ma5_socket.onerror   = function(ev){
                        console.log('socket error on '+interface+' interface');
                    }; 
                    advair_ma5_socket.onclose   = function(ev){
                        console.log('socket disconnected from '+interface+' interface');
                        //try to reconnect in 5 seconds
                        setTimeout(function(){get_live_status(interface,refr)}, 5000);
                    };

                    break;
            }
        }

        $(document).ready(function(){

          ws_host_addr = '<?php echo CONST_ws_host; ?>';
          ws_host_port_advair_ma5 = '<?php echo CONST_advair_ma5_ws_port; ?>';
          listner_addresses_arr = ['advair_ma5'];

          setTimeout(function() {
              spawn_listener_interfaces();
          },1000 );

        });
    </script>
  </head>
  <body>
    <div id="res"></div>
  </body>
</html>