<?php 

  class cgateCommon
  {
  	public $var1;

  	public function __construct() {
      $this->cr = chr(0x0D) . chr(0x0A); // carriage return
      $this->host_url = 'cgate'; // c-gate host name / IP address
      $this->change_tcp_port = '20025'; // c-gate status change port
      $this->command_tcp_port = '20023'; // c-gate send-command interface port
      $this->project = 'NET1'; // your c-gate project name eg. home1
      $this->network = '254'; // the number of your c-bus network - will expand to allow multiple networks in future releases.
      $this->app = '56'; // the number of your c-bus network - will expand to allow multiple networks in future releases.
      $this->get_all_msg = "get //" . $this->project . "/" . $this->network . "/" . $this->app . "/* level";
    }

    public function messageSend($msg)
    {
      // sent the message to cgate on the command port

      $fp = fsockopen($this->host_url, $this->command_tcp_port, $errno, $errstr);
      if (!$fp) { $result2 = "-"; } // error: could not connect to command interface port
      else {
        fgets($fp, 1024); // get the command port welcome message
        fputs($fp, $msg . $this->cr); // write the $msg string to the socket to request the status info

        $last_response_line = false;

        $result2 = "";
        while (!$last_response_line) {
          $buffer = fgets($fp, 4096);
          if (strpos($buffer,"300-//") === false) { $last_response_line = true; } // ie. the last line will not have the dash and will just be '300 //' not '300-//'
          $result2 .= $buffer;
        }
  
        fclose($fp); // close the connection
      }
      return $result2;
    }

    public function cgateToJson($cgate_text)
    {

      $levels = "";
      $str_arr = explode("\n",$cgate_text);
      foreach ($str_arr as $key => $val) {
        if ($val != "") {
          $row_id = str_replace("/","_",substr($val,(strpos($val,"//")+2),(strpos($val,":")-strpos($val,"//")-2)));
          $row_level_str = intval(trim(substr($val,(strpos($val,"l=")+2)))); 
          $row_level = round($row_level_str * (100/255));
          if ($row_level > 100) { $row_level = 100; }
          if ($row_level < 0) { $row_level = 0; }
          $levels .= "    \"cgate__" . $row_id . "__level\" : \"" . $row_level . "\",\n";
        }
      }
      return "{\n" . substr($levels,0,-2) . "\n}";
    }

    public function deviceIdTocgateId($device_id)
    {

    return str_replace("_","/",$device_id);
    }

  }

?>