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

    function add_scene_delay($action_params)
    {
        // takes $delay_in_sec
        $del = $action_params['delay_in_sec'];
        set_time_limit($del+5);
        sleep($del);
        echo "added " . $del . " seconds of scene delay <br>\n";
    }

	function cbus_cgate_light_dim1($action_params)
	{
		// takes $device_id, $dim_value, $ramp_time
        // if $dim_value is null in the config params, then it will use the
        // input from the widget which is how you can achieve group dimming
        if ($action_params['dim_value'] == null) { $dim_val = $_GET['val']; }
		else { $dim_val = $action_params['dim_value']; }

		if ($action_params['ramp_time'] == null) { $ramp_val = $_GET['ramp']; }
		else { $ramp_tm = $action_params['ramp_time']; }

		$send_msg = "RAMP //" . deviceid_to_cgate_id($action_params['device_id']) . " " . round((($dim_val/100)*255),0) . " " . $ramp_tm . "s";
		$result_msg = cbus_cgate_send_message($send_msg);
        echo "c-gate sent:" . $send_msg . "    c-gate returned:" . $result_msg . "<br>\n";
	}

	function cbus_cgate_device_toggle1($action_params)
	{
		// takes $device_id
        // if $set_value is null in the config params, then it will use the
        // input from the widget which is how you can achieve group dimming
        if ($action_params['set_value'] == null) { $set_val = $_GET['val']; }
		else { $set_val = $action_params['set_value']; }

		if ($set_val == 100) { $msg_val = "ON"; }
		else { $msg_val = "OFF"; }

		$send_msg = $msg_val . " //" . deviceid_to_cgate_id($action_params['device_id']);

		$result_msg = cbus_cgate_send_message($send_msg);
        echo "c-gate sent:" . $send_msg . "    c-gate returned:" . $result_msg . "<br>\n";
	}

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
