<?php 

  class hueCommon
  {
  	public $var1;

  	public function __construct() {

      $this->bridge_url = 'http://192.168.2.223/api/nA54rAAXRvvNMoSuOPcxE9y7gzhH9qVzdo5Of2M0/';
    }

    public function hitCurl($meth, $curl_url, $curl_data)
    {
        $ch = curl_init();
        if ($ch === false) {
            throw new Exception('failed to initialize');
        }

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_URL, $curl_url);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        if (($meth == "POST") || ($meth == "PUT")) {
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($meth));
            curl_setopt($ch, CURLOPT_POSTFIELDS, $curl_data);
        }

        $result = curl_exec($ch);

        if ($result === false) {
            throw new Exception(curl_error($ch), curl_errno($ch));
        }
        curl_close($ch);

        return $result;
    }

    public function hueToJson($hue_data)
    {

      $levels = '';
      $data = json_decode($hue_data);
      foreach ($data as $key => $val) {
        if ($val != '') {
          $row_state = $val->state->on;
          if ($row_state == true) {
            $row_level = round($val->state->bri * (100/255));
          }
          else {
            $row_level = 0;
          }
          $levels .= "    \"hue__" . $key . "__level\" : \"" . $row_level . "\",\n";
        }
      }
      return "{\n" . substr($levels,0,-2) . "\n}";
    }

  }

?>