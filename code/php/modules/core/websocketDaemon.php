<?php

  require_once "/code/config/websocket_config.php";
  require_once "/code/modules/core/redisController.php";

  $d = new wsocketDaemon();
  $d->start_daemon();


  //*******************************************


  class wsocketDaemon
  {

    public function __construct() {
      $this->debug_mode = 0;
      $this->client_sockets = [];
      $this->ws_host = CONST_ws_host;
      $this->ws_port = CONST_ws_port;
      $this->force_update = false;
      $this->cached_data = [];
      $this->last_change = 0; // the last time anything changed in ms timestamp
      $this->redis = new redisController;
      $this->rc = $this->redis->connect();
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
    public function unmask($frame) {

      $len = ord($frame[1]) & 127;
      if ($len === 126) { $ofs = 8; }
      elseif ($len === 127) { $ofs = 14; }
      else { $ofs = 6; }

      $text = '';
      for ($i = $ofs; $i < strlen($frame); $i++) {
        $text .= $frame[$i] ^ $frame[$ofs - 4 + ($i - $ofs) % 4];
      }

      if (ord($text) == '3') {
        $text = 'notice: socket disconnected';
      }
      elseif ($len == '0') {
        $text = 'notice: new socket connected';
      }

      return $text;
    }

    // encode message for transfer to client.
    public function mask($text) {

      $b1 = 0x80 | (0x1 & 0x0f);
      $length = strlen($text);
      
      if($length <= 125) { $header = pack('CC', $b1, $length); }
      elseif($length > 125 && $length < 65536) { $header = pack('CCn', $b1, 126, $length); }
      elseif($length >= 65536) { $header = pack('CCNN', $b1, 127, $length); }
      return $header.$text;
    }

    // handshake with new client.
    public function perform_ws_handshake($receved_header, $client_conn, $host, $port) {

      $headers = array();
      $lines = preg_split("/\r\n/", $receved_header);
      foreach($lines as $line) {

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
        "WebSocket-Location: ws://$host:$port/index.php\r\n".
        "Sec-WebSocket-Accept:$secAccept\r\n\r\n";
      socket_write($client_conn,$upgrade,strlen($upgrade));
    }

    public function log_info($ev_name, $ev_data) {
      if ($this->debug_mode == 1) {

        ob_start();
        var_dump($ev_data);
        $ev_str = ob_get_clean();

        $log = '<br>-------------------';
        $log .= '<br>timestamp: ' . date("Y-m-d H:i:s");
        $log .= '<br>event: ' . $ev_name;
        $log .= '<br>' . $ev_str;

        $old_info = $this->rc->get('ws_log');
        $new_info = $log . substr($old_info, 0, 100000);
        $this->rc->set('ws_log', $new_info);
      }
    }

    public function send_changes() {

      $latest_data = [];

      $keys_arr = $this->rc->keys('*');
      foreach($keys_arr as $key) {
        if (strpos($key, '_data') != false) {
          $latest_data[$key] = $this->rc->get($key);

          if (($latest_data[$key] != $this->cached_data[$key]) || ($this->force_update == true)) { // if its different - tell everyone and update levels and last change time
            $response = $this->mask($latest_data[$key]);
            $this->websocket_send_message($response);
            $this->log_info('data sent', $latest_data[$key]);

            if ($latest_data[$key] != $this->cached_data[$key]) {
              $this->last_change = round(microtime(true) * 1000);
              $this->cached_data[$key] = $latest_data[$key]; // update the class property with the fresh data
            }
          }
        }
      }

      $this->force_update = false; // reset this

    }

    public function init_cache() {

      $keys_arr = $this->rc->keys('*');
      foreach($keys_arr as $key) {
        if (strpos($key, '_data') != false) {
          $this->cached_data[$key] = '';
        }
      }

    }

    public function start_daemon() {
        
      $svr_socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // create TCP/IP stream socket
      socket_set_option($svr_socket, SOL_SOCKET, SO_REUSEADDR, 1); // set to be a reuseable port
      socket_bind($svr_socket, 0, $this->ws_port); // bind socket to specified host
      socket_listen($svr_socket); // start listening for connections on $svr_socket

      // variables for socket_select
      $write = NULL;
      $exceptions = NULL;

      //create the list of sockets we are managing, and first up add the server/daemon socket to the list
      $this->client_sockets = [$svr_socket];

      if ($this->rc == false) { echo 'redis conection fail'; exit(); } 
      else {

        $this->init_cache();
        $this->rc->set('ws_log', '');
        $this->log_info('process started', $svr_socket);

        // **** temporarily set this so that it runs for a bit from the browser to test ***
        //set_time_limit(60);
        $arg_id = $_SERVER['argv'][1];
        $daemon_id = $this->rc->get('ws_daemon_id');

        //start endless loop, so that our script doesn't stop
        while ($daemon_id == $arg_id) {

          try { 
            $this->rc->ping();
          }
          catch (Exception $e) {
            $this->rc = $this->redis->connect();
          }

          // essentiallly socket_select waits for a change to any socket within the $client_sockets array and
          // then mutates the $changed_sockets array into an array of whatever sockets changed
          // this will wait 10 microseconds for a change then just go
          $changed_sockets = $this->client_sockets; // need a variable for socket_select to mess with, so start with our client sockets array
          socket_select($changed_sockets, $write, $exceptions, 0, 10);

          // if our listen socket had a change then that means we have a new connection
          if (in_array($svr_socket, $changed_sockets)) {
            $socket_new = socket_accept($svr_socket); //find out what socket just connected to our listen socket and call it $socket_new
            $this->client_sockets[] = $socket_new; //add $svr_socket_new to client array
            $header = socket_read($socket_new, 1024); //read header data sent by the socket
            $this->perform_ws_handshake($header, $socket_new, $this->ws_host, $this->ws_port); //perform websocket handshake
            $this->log_info('socket added', $this->client_sockets);

            $this->force_update = true; // trigger update to all clients

            //remove listen socket from array of sockets to iterate through for the next bit
            $listen_socket = array_search($svr_socket, $changed_sockets);
            unset($changed_sockets[$listen_socket]);
          }

          //loop through all sockets that had a change (ie. except for our listen one - the server / daemon - that we just removed)
          foreach ($changed_sockets as $changed_socket) {

            //check for any incomming data
            while(socket_recv($changed_socket, $buf, 1024, 0) >= 1) {

              $unmasked = $this->unmask($buf);
              $this->log_info('data received', $unmasked);

              if ($unmasked == 'ping') {
                $response = $this->mask("pong"); // whatever the message just send a pong as only expecting ping or close
                $this->websocket_send_message($response); //send data
                $this->log_info('pong sent', 'pong');
              }

              $this->force_update = true; // trigger update to all clients

              break 2; //exits the while and this iteration of foreach
            }

            // detect that someone disconnected because there was a change, but no message
            $buf = @socket_read($changed_socket, 1024, PHP_NORMAL_READ);

            if ($buf === false) { // check disconnected client
              $found_socket = array_search($changed_socket, $this->client_sockets);
              unset($this->client_sockets[$found_socket]); // remove client for $client_sockets array
              $this->log_info('socket removed', $this->client_sockets);
            }
          }

          $this->send_changes();

          if ((round(microtime(true) * 1000) - $this->last_change) < 600000) {
            usleep(200000); // sleep for 200ms then go again
          }
          else { // ie. if no action for 10 mins, go into sleep mode
            usleep(1000000); // sleep for 1000ms then go again
          }

          $daemon_id = $this->rc->get('ws_daemon_id');

        } // end while loop

      } // end else - ie. end could connect to c-gate

      echo "stopped"; 
      
    } // end start_ws_daemon

  }
