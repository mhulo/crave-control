<?php 

  class coreCommon
  {

  	public function __construct() {

    }

    public function hitCurl($cmd_url) {

      $cSession = curl_init(); 
      curl_setopt($cSession,CURLOPT_URL,$cmd_url);
      curl_setopt($cSession,CURLOPT_RETURNTRANSFER,true);
      curl_setopt($cSession,CURLOPT_HEADER, false); 
      $curl_result=curl_exec($cSession);
      curl_close($cSession);
      return $curl_result;
    }

  }

?>