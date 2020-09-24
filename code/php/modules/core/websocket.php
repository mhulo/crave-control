<?php

  class crave_wsocket
  {
    public $client_sockets;

    public function __construct($module_name, $module_port) {
      $this->client_sockets = [];
      $this->module_name = $module_name;
      $this->module_port = $module_port;
      $this->cgate =  new cgateCommon;
      $this->run_file = '/code/daemons/' . $this->module_name . '_running.txt';
      $this->sockets_file = '/code/daemons/' . $this->module_name . '_sock_data.txt';
    }

    public function websocket_send_message($msg) {

      foreach($this->client_sockets as $write_socket) {
          $sent_ok = @socket_write($write_socket,$msg,strlen($msg));
          if ($sent_ok === false) {
              unset($this->client_sockets[$write_socket]);
          }
      }
      return true;
    }

    // unmask incoming framed message
    public function websocket_message_unmask($text) {

      $length = ord($text[1]) & 127;
      if($length == 126) {
          $masks = substr($text, 4, 4);
          $data = substr($text, 8);
      }
      elseif($length == 127) {
          $masks = substr($text, 10, 4);
          $data = substr($text, 14);
      }
      else {
          $masks = substr($text, 2, 4);
          $data = substr($text, 6);
      }
      $text = "";
      for ($i = 0; $i < strlen($data); ++$i) {
          $text .= $data[$i] ^ $masks[$i%4];
      }
      return $text;
    }

    // encode message for transfer to client.
    public function websocket_message_mask($text) {

      $b1 = 0x80 | (0x1 & 0x0f);
      $length = strlen($text);
      
      if($length <= 125)
          $header = pack('CC', $b1, $length);
      elseif($length > 125 && $length < 65536)
          $header = pack('CCn', $b1, 126, $length);
      elseif($length >= 65536)
          $header = pack('CCNN', $b1, 127, $length);
      return $header.$text;
    }

    // handshake with new client.
    public function perform_ws_handshake($receved_header, $client_conn, $host, $port) {

      $headers = array();
      $lines = preg_split("/\r\n/", $receved_header);
      foreach($lines as $line)
      {
          $line = chop($line);
          if(preg_match('/\A(\S+): (.*)\z/', $line, $matches))
          {
              $headers[$matches[1]] = $matches[2];
          }
      }

      $secKey = $headers['Sec-WebSocket-Key'];
      $secAccept = base64_encode(pack('H*', sha1($secKey . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')));
      //handshake header
      $upgrade  = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" .
      "Upgrade: websocket\r\n" .
      "Connection: Upgrade\r\n" .
      "WebSocket-Origin: $host\r\n" .
      "WebSocket-Location: ws://$host:$port/crave/index.php\r\n".
      "Sec-WebSocket-Accept:$secAccept\r\n\r\n";
      socket_write($client_conn,$upgrade,strlen($upgrade));
    }

    public function start_ws_daemon() {
        
        $debug_mode = 0;
        $socket_data_file = fopen($this->sockets_file, 'w');

        $svr_socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // create TCP/IP stream socket
        socket_set_option($svr_socket, SOL_SOCKET, SO_REUSEADDR, 1); // set to be a reuseable port
        socket_bind($svr_socket, 0, $this->module_port); // bind socket to specified host
        socket_listen($svr_socket); // start listening for connections on $svr_socket

        if ($debug_mode == 1) {
            $txt0 = "running since: " . date("Y-m-d H:i:s") . "\n\n";
            $txt0 .= "listen socket:\n";
            ob_start();
            var_dump($svr_socket);
            $txt0 .= ob_get_clean();
            fwrite($socket_data_file, $txt0);
        }

        // variables for socket_select
        $write = NULL;
        $exceptions = NULL;

        //create the list of sockets we are managing, and first up add the server/daemon socket to the list
        $this->client_sockets = [$svr_socket];
        $levels_data = "";
        $last_change = 0; // the last time anything changed in ms timestamp
        $force_update = false;

        $cgate_stream = fsockopen($this->cgate->host_url, $this->cgate->change_tcp_port, $errno, $errstr);
        stream_set_blocking($cgate_stream, false);
        if (!$cgate_stream) { echo "could not connect to c-gate"; exit(); } // error: could not connect to status-change port
        else {

          // **** temporarily set this so that it runs for a bit from the browser ***
          //set_time_limit(60);

          //start endless loop, so that our script doesn't stop
          while (file_exists($this->run_file)) {

            // essentiallly socket_select waits for a change to any socket within the $client_sockets array and
            // then creates and updates a new array called $changed_sockets which will be an array of whatever sockets changed
            // ie. !!! socket_select actually changes the $changed_sockets array !!!
            // this will wait 10 microseconds for a change then just go
            $changed_sockets = $this->client_sockets; // need a variable for socket_select to mess with, so start with our client sockets array
            socket_select($changed_sockets, $write, $exceptions, 0, 10);

            // if our listen socket had a change then that means we have a new connection
            if (in_array($svr_socket, $changed_sockets)) {
              $socket_new = socket_accept($svr_socket); //find out what socket just connected to our listen socket and call it $socket_new
              $this->client_sockets[] = $socket_new; //add $svr_socket_new to client array
              $header = socket_read($socket_new, 1024); //read header data sent by the socket
              $this->perform_ws_handshake($header, $socket_new, CONST_ws_host, $this->module_port); //perform websocket handshake

              if ($debug_mode == 1) {
                $txt1 = "\nadd event:\n";
                ob_start();
                var_dump($this->client_sockets);
                $txt1 .= ob_get_clean();
                fwrite($socket_data_file, $txt1);
                fwrite($socket_data_file, "\n\n" . $levels_data);
              }

              // set a var to trigger a message to be sent to make sure that this new client has the latest levels
              $force_update = true;

              //we dont want our listen socket to be one of the sockets we iterate through for the next bit of this iteration of the while loop so take it out
              $listen_socket = array_search($svr_socket, $changed_sockets);
              unset($changed_sockets[$listen_socket]);
            }

            //loop through all sockets that had a change (ie. except for our listen one - the server / daemon - that we just removed)
            foreach ($changed_sockets as $changed_socket) {

              //check for any incomming data
              while(socket_recv($changed_socket, $buf, 1024, 0) >= 1)
              {
                $received_text = $this->websocket_message_unmask($buf); //unmask data

                if ($debug_mode == 1) {
                  $txt2 = "\nreceive event:\n";
                  if (ord($received_text) == "3") { $txt2 .= "close msg\n"; }
                  else { $txt2 .= $received_text . "\n"; }
                  ob_start();
                  var_dump($this->client_sockets);
                  $txt2 .= ob_get_clean();
                  fwrite($socket_data_file, $txt2);
                }

                //prepare data to be sent to client
                $response_text = $this->websocket_message_mask("pong");
                $this->websocket_send_message($response_text); //send data

                // set a var to trigger a message to be sent to make sure that everyone has the latest levels in response to the action that triggered the ping
                $force_update = true;

                break 2; //exits the while and this iteration of foreach
              }

              // detect that someone disconnected because there was a change, but no message
              $buf = @socket_read($changed_socket, 1024, PHP_NORMAL_READ);

              if ($buf === false) { // check disconnected client
                $found_socket = array_search($changed_socket, $this->client_sockets);
                unset($this->client_sockets[$found_socket]); // remove client for $client_sockets array

                if ($debug_mode == 1) {
                  $txt3 = "\nremove event:\n";
                  ob_start();
                  var_dump($this->client_sockets);
                  $txt3 .= ob_get_clean();
                  fwrite($socket_data_file, $txt3);
                }
              }
            }

            $cgate_event = fgets($cgate_stream, 1024); // see if there is a status-update message ready to go

            // if there was a c-gate event, or the last change in data was less than 10 sec ago, then keep polling the current levels to make sure we have the right levels
            if (($cgate_event != "") || ((round(microtime(true) * 1000) - $last_change) < 10000) || ($levels_data == "") || ($force_update == true)) {
              $all_levels_response = $this->cgate->messageSend($this->cgate->get_all_msg);
              //error_log('resp:' . $all_levels_response);
              $latest_data = $this->cgate->cgateToJson($all_levels_response);
            }

            if (($latest_data != $levels_data) || ($force_update == true)) { // if its different - tell everyone and update levels and last change time
              $response = $this->websocket_message_mask($latest_data);
              $this->websocket_send_message($response);

              if ($latest_data != $levels_data) {
                $last_change = round(microtime(true) * 1000);
                $levels_data = $latest_data; // update the global with the fresh levels data
              }

              $force_update = false; // reset this ahead of the next iteration of the loop
            }

            if ((round(microtime(true) * 1000) - $last_change) < 600000) {
              usleep(200000); // sleep for 200ms then go again
            }
            else { // ie. if no action for 10 mins, go into sleep mode
              usleep(1000000); // sleep for 1000ms then go again
            }

          } // end while loop

          fclose($cgate_stream); // close the status connection

          fclose($socket_data_file);
          //unlink("sock_data.txt");

      } // end else - ie. end could connect to c-gate

      echo "stopped"; 
        
    } // end start_ws_daemon

  }
