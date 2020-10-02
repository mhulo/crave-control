<?php

  require_once '/code/modules/hue/hueCommon.php';
  require_once "/code/modules/core/redisController.php";

  $d = new hueDaemon();
  $d->start_daemon();


  //*******************************************

   class hueDaemon
  {

    public function __construct() {
    	$this->force_update = true;
    	$this->cached_data = '';
    	$this->last_change = 0;
      $this->hue =  new hueCommon;
      $this->redis = new redisController;
      $this->rc = $this->redis->connect();
    }

    public function start_daemon() {

      if ($this->rc == false) { echo 'redis conection fail'; exit(); } 
      else {

        // **** temporarily set this so that it runs for a bit from the browser to test ***
        //set_time_limit(60);
        $arg_id = $_SERVER['argv'][1];
        $daemon_id = $this->rc->get('hue_daemon_id');

        //start endless loop, so that our script doesn't stop
        while ($daemon_id == $arg_id) {

          try { 
            $this->rc->ping();
          }
          catch (Exception $e) {
            $this->rc = $this->redis->connect();
          }

          $curl_url = $this->hue->bridge_url . 'lights/';
          $response = $this->hue->hitCurl('GET', $curl_url, null);
          $latest_data = $this->hue->hueToJson($response);

          if (($latest_data != $this->cached_data) || ($force_update == true)) { // if its different - tell everyone and update levels and last change time
            
            $this->rc->set('hue_data', $latest_data);
            $this->last_change = round(microtime(true) * 1000);
            $this->cached_data = $latest_data;
            $force_update = false; // reset this ahead of the next iteration of the loop
          }

          if ((round(microtime(true) * 1000) - $this->last_change) < 600000) {
            usleep(2000000); // sleep for 2000ms then go again
          }
          else { // ie. if no action for 10 mins, go into sleep mode
            usleep(5000000); // sleep for 5000ms then go again
          }

          $daemon_id = $this->rc->get('hue_daemon_id');

        } // end while loop

      } // end else - ie. end could connect to redis

      echo "stopped"; 
        
    } // end start_ws_daemon

  }

