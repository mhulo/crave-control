<?php 

  require_once '/code/modules/cgate/cgateCommon.php';
  require_once '/code/modules/core/redisController.php';

  class cgateController
  {
  	public $var1;

  	public function __construct()
    {
      $this->cgate =  new cgateCommon;
      $this->redis =  new redisController;
    }

    public function noopTest($q)
    {
      // issue a noop command to test if cgate is responding
      $send_msg = 'noop';
      $result_msg = $this->cgate->messageSend($send_msg);
      return $send_msg . '  ::  ' . $result_msg;
    }

    public function startDaemon($q)
    {
      // create an id that the daemon while loop can check to see if it should continue or not
      $rc = $this->redis->connect();
      $id = $this->redis->rand();
      $rc->set('cgate_daemon_id', $id);
      exec('php /code/modules/cgate/cgateDaemon.php '. $id, $output);
      $resp = print_r($output, true);
      return $resp;
    }

    public function stopDaemon($q)
    {
      // reset the id so the while loop will stop
      $rc = $this->redis->connect();
      $rc->set('cgate_daemon_id', '0');
      return 'stopped';
    }

    public function levelsShow($q)
    {
      // takes $device_id, $dim_value, $ramp_time
      // if $dim_value is null in the config params, then it will use the
      // input from the card which is how you can achieve group dimming

      // issue a get command and get the status of the whole network for lighting
      $result_msg = $this->cgate->messageSend($this->cgate->get_all_msg);
      header("Content-Type: application/json;charset=utf-8");
      return $this->cgate->cgateToJson($result_msg);
    }

    public function levelDim($q)
    {
      // takes $device_id, $set_value, $ramp_time
      // if $set_value is null in the config params, then it will use the
      // input from the card which is how you can achieve scene dimming

      $send_msg = 'RAMP //' . $this->cgate->deviceIdTocgateId($q->device_id) . ' ' . round((($q->set_val/100)*255),0) . ' ' . $q->ramp_time . 's';
      $result_msg = $this->cgate->messageSend($send_msg);
      return 'c-gate sent:' . $send_msg . '    c-gate returned:' . $result_msg . '<br>';
    }

    public function levelToggle($q)
    {
      // takes $device_id
      // if $set_value is null in the config params, then it will use the
      // input from the card which is how you can achieve discrete on/off

      if ($q->set_val == '100') { $msg_val = 'ON'; }
      else { $msg_val = 'OFF'; }

      $send_msg = $msg_val . ' //' . $this->cgate->deviceIdTocgateId($q->device_id);

      $result_msg = $this->cgate->messageSend($send_msg);
      return 'c-gate sent:' . $send_msg . '    c-gate returned:' . $result_msg . '<br>';
    }

  }

?>