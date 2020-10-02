<?php 

  require_once '/code/modules/hue/hueCommon.php';
  require_once '/code/modules/core/redisController.php';
  require_once '/code/modules/core/coreCommon.php';

  class hueController
  {
  	public $var1;

  	public function __construct()
    {
      $this->hue =  new hueCommon;
      $this->redis =  new redisController;
    }

    public function startDaemon($q)
    {
      // create an id that the daemon while loop can check to see if it should continue or not
      $rc = $this->redis->connect();
      $id = $this->redis->rand();
      $rc->set('hue_daemon_id', $id);
      exec('php /code/modules/hue/hueDaemon.php '. $id, $output);
      $resp = print_r($output, true);
      return $resp;
    }

    public function stopDaemon($q)
    {
      // reset the id so the while loop will stop
      $rc = $this->redis->connect();
      $rc->set('hue_daemon_id', '0');
      return 'stopped';
    }

    public function levelsShow($q)
    {
      // takes $device_id, $dim_value, $ramp_time
      // if $dim_value is null in the config params, then it will use the
      // input from the widget which is how you can achieve group dimming

      // issue a get command and get the status of the whole network for lighting
      $curl_url = $this->hue->bridge_url . 'lights/';
      $res = $this->hue->hitCurl('GET', $curl_url, null);

      header("Content-Type: application/json;charset=utf-8");
      return $this->hue->hueToJson($res);
      //return $ret_str;
    }

    public function levelDim($q)
    {
      // takes $device_id, $set_value, $ramp_time
      // if $set_value is null in the config params, then it will use the
      // input from the widget which is how you can achieve scene dimming

      $curl_url = $this->hue->bridge_url . 'lights/' . $q->device_id . '/state';
      $curl_data = '{"bri":' . round((($q->set_val/100)*254),0) . '}';
      $ret_str = $this->hue->hitCurl('PUT', $curl_url, $curl_data);
      return $ret_str;
    }

    public function levelToggle($q)
    {
      // takes $device_id
      // if $set_value is null in the config params, then it will use the
      // input from the widget which is how you can achieve discrete on/off

      if ($q->set_val == '100') { $on_state = 'true'; }
      else { $on_state = 'false'; }

      $curl_url = $this->hue->bridge_url . 'lights/' . $q->device_id . '/state';
      $curl_data = '{"on":' . $on_state . '}';
      $ret_str = $this->hue->hitCurl('PUT', $curl_url, $curl_data);
      return $ret_str;
    }

  }

?>