<?php 

  require_once '/code/modules/cgate/cgateCommon.php';

  class actionController
  {

  	public function __construct()
    {
      //$this->cgate =  new cgateCommon;
    }

    public function addSceneDelay($q)
    {
      // takes $delay_in_sec
      $delay = $q->delay_in_sec;
      set_time_limit($delay+5);
      sleep($delay);
      return "added " . $delay . " seconds of scene delay <br>\n";
    }

    public function levelDim($q)
    {
      // takes $device_id, $set_value, $ramp_time
      // if $set_value is null in the config params, then it will use the
      // input from the card which is how you can achieve scene dimming
      $r['params'] = $q;
      $r = (object) $r;
      return useContr('modules/' . $q->module . '/' . $q->module . 'Controller@levelDim', $r);
    }

    public function levelToggle($q)
    {
      // takes $device_id
      // if $set_value is null in the config params, then it will use the
      // input from the card which is how you can achieve discrete on/off
      $r['params'] = $q;
      $r = (object) $r;
      return useContr('modules/' . $q->module . '/' . $q->module . 'Controller@levelToggle', $r);
    }

  }

?>