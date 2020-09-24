<?php require_once "advair_ma5_config.php"; ?>
<?php require_once "../../../config/websocket_config.php"; ?>
<?php require_once "../../core_functions.php"; ?>
<?php require_once "advair_ma5_functions.php"; ?>
<?php

	/** returns status via the mayair5 getSystemData command, something like;
	 *{
     *	"advair_ma5__ac1_main__setTemp" : "24",
     *	"advair_ma5__ac1_main__state" : "on",
     *	"advair_ma5__ac1_main__airconErrorCode" : "AA3",
     *	"advair_ma5__ac1_main__fan" : "low",
     *	"advair_ma5__ac1_main__filterCleanStatus" : "0",
     *	"advair_ma5__ac1_main__mode" : "heat",
     *	....
	 *}
	 */

	$all_levels_str = issue_curl_cmd("http://" . CONST_advair_ma5_host_url . ":" . CONST_advair_ma5_host_port . "/getSystemData");;

	// now return the levels to the browser as json	
	header("Content-Type: application/json;charset=utf-8");

	if ((isset($_GET["type"])) && ($_GET["type"] == "raw")) { echo $all_levels_str; }
	else { echo ma5_to_json($all_levels_str); }
