<?php 


  class redisController
  {
    public function __construct()
    {
      //$this->run_file = '/code/daemons/ws_running.txt';
    }

    public function connect()
    {
      try {
        $redis = new Redis();
        $redis->connect('redis', 6379, 2); // 2 is 2-sec timeout
        $redis->ping();
        return $redis;
      }
      catch (Exception $e) {
        //throw new Exception("redis conection failed: " . $e->getMessage());
        return false;
      }
    }

    public function rand()
    {
      // create random id that the daemon can use to identify itself
      return substr(md5(rand()), 0, 6);
    }

    public function startDaemonOld($q)
    {
      // create a file that the daemon while loop can check to see if it should continue or not
      $handle = fopen($this->run_file, "w") or die("cannot create file:  ". $this->run_file); //implicitly creates file
      fclose($handle);
      exec("php /code/modules/core/websocketDaemon.php", $output);
      $resp = print_r($output, true);
      return $resp;
    }

    public function stopDaemon($q)
    {
      // delete the file so the while loop will stop
      unlink($this->run_file);
      return 'stopped';
    }

  }

?>