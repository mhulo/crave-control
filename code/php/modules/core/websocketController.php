<?php 

  require_once '/code/modules/core/redisController.php';


  class websocketController
  {

  	public function __construct()
    {
      //$this->cgate =  new cgateCommon;
      $this->redis =  new redisController;
    }

    public function startDaemon($q)
    {
      // create an id that the daemon while loop can check to see if it should continue or not
      $rc = $this->redis->connect();
      $id = $this->redis->rand();
      $rc->set('ws_daemon_id', $id);
      exec('php /code/modules/core/websocketDaemon.php '. $id, $output);
      $resp = print_r($output, true);
      return $resp;
    }

    public function stopDaemon($q)
    {
      // reset the id so the while loop will stop
      $rc = $this->redis->connect();
      $rc->set('ws_daemon_id', '0');
      return 'stopped';
    }

  }

?>