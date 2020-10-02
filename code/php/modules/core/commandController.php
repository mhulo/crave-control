<?php 

  require_once '/code/modules/cgate/cgateCommon.php';

  class commandController
  {

  	public function __construct()
    {

    }

    public function runCommand($q)
    {
      // runs action methods based on a command
      $commands_json_file = '/code/config/commands_config.json';
      $command = json_decode(file_get_contents($commands_json_file), true);
      $json_err = json_last_error_msg();
      if ($json_err != 'No error'){
        echo "error with file: ". $commands_json_file . '<br>';
        echo $json_err;
        exit();
      }
      $res = '';
      foreach ($command[$_GET['cmd']]['actions'] as $action) { // iterate through all the actions in the command
        $r = [];
        $r['params'] = $_GET; // the params that come from the widget
        foreach ($action['params'] as $key => $value) { // override any params from the command
          $r['params'][$key] = $value;
        }
        $r = json_encode($r);
        $res .= useContr('modules/' . $action['method'], json_decode($r));
      }
      return $res;
    }

    public function redisShow($redis, $chan, $msg)
    {
      echo 'got message:' . $msg . ' on channel ' . $chan;
      exit();
    }

    public function redisSet()
    {

      $redis = new Redis();
      $redis->connect('redis', 6379);

      $cgate_data = '{ "cgate__NET1_254_56_0__level": "80", "cgate__NET1_254_56_3__level": "20" }';
      $redis->set('cgate_data', $cgate_data);
      //$redis->publish('events', $cgate_data);

      echo 'data set';
    }

    public function redisGet()
    {

      $redis = new Redis(); 
      $redis->connect('redis', 6379);
      //$redis->subscribe(['events'], array($this, 'redisShow'));

      print_r($redis->keys("*"));
      echo '<br><br>*************<br>';

    }

  }

?>