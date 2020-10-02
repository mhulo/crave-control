<?php

  require_once '/code/modules/cgate/cgateCommon.php';
  require_once "/code/modules/core/redisController.php";

  $d = new cgateDaemon();
  $d->start_daemon();


  //*******************************************

   class cgateDaemon
  {

    public function __construct() {
      $this->force_update = true;
      $this->cached_data = '';
      $this->last_change = 0;
      $this->cgate =  new cgateCommon;
      $this->redis = new redisController;
      $this->rc = $this->redis->connect();
    }

    public function start_daemon() {

      $cgate_stream = fsockopen($this->cgate->host_url, $this->cgate->change_tcp_port, $errno, $errstr);
      stream_set_blocking($cgate_stream, false);
      if (!$cgate_stream) { echo 'cgate connection fail'; exit(); } // error: could not connect to status-change port
      elseif ($this->rc == false) { echo 'redis conection fail'; exit(); } 
      else {

        // **** temporarily set this so that it runs for a bit from the browser to test ***
        //set_time_limit(60);
        $arg_id = $_SERVER['argv'][1];
        $daemon_id = $this->rc->get('cgate_daemon_id');

        //start endless loop, so that our script doesn't stop
        while ($daemon_id == $arg_id) {

          try { 
            $this->rc->ping();
          }
          catch (Exception $e) {
            $this->rc = $this->redis->connect();
          }

          $cgate_event = fgets($cgate_stream, 1024); // see if there is a status-update message ready to go

          // if there was a c-gate event, or the last change in data was less than 10 sec ago, then keep polling the current levels to make sure we have the right levels
          if (($cgate_event != '') || ((round(microtime(true) * 1000) - $this->last_change) < 10000) || ($this->cached_data == '') || ($force_update == true)) {
            $response = $this->cgate->messageSend($this->cgate->get_all_msg);
            $latest_data = $this->cgate->cgateToJson($response);
          }

          if (($latest_data != $this->cached_data) || ($force_update == true)) { // if its different - tell everyone and update levels and last change time
            
            $this->rc->set('cgate_data', $latest_data);
            $this->last_change = round(microtime(true) * 1000);
            $this->cached_data = $latest_data;
            $force_update = false; // reset this ahead of the next iteration of the loop
          }

          if ((round(microtime(true) * 1000) - $this->last_change) < 600000) {
            usleep(200000); // sleep for 200ms then go again
          }
          else { // ie. if no action for 10 mins, go into sleep mode
            usleep(1000000); // sleep for 1000ms then go again
          }

          $daemon_id = $this->rc->get('cgate_daemon_id');

        } // end while loop

        fclose($cgate_stream); // close the status connection

      } // end else - ie. end could connect to c-gate

      echo "stopped"; 
        
    } // end start_ws_daemon

  }

