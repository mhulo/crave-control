<?php
	/*
	Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
	Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
	version: 2017-06-25
	www.cravetechnology.com.au
	*/
?>
<?php
    // --- this is where you start inserting all the action functions for all the various widgets --- //
    // --- many will use basic dim or on/off functions but there is endless possibilities for scenes --- //


	function advair_ma5_power($action_params)
	{
		$send_msg = "http://" . CONST_advair_ma5_host_url . ":" . CONST_advair_ma5_host_port . "/setAircon?json={\"ac1\":{\"info\":{\"state\":\"" . $_GET['val'] . "\"}}}";
		issue_curl_cmd($send_msg);
	}

	function advair_ma5_zone_perc($action_params)
	{
		$device = explode("_", $action_params['device_id']);
		$rounded_val = round($_GET['val'] / 5 ) * 5;
		$send_msg = "http://" . CONST_advair_ma5_host_url . ":" . CONST_advair_ma5_host_port . "/setAircon?json={\"" . $device[0] . "\":{\"zones\":{\"" . $device[1] . "\":{\"value\":\"" . $rounded_val . "\"}}}}";
		issue_curl_cmd($send_msg);
	}
?>
