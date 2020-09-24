<?php require_once "cbus_cgate_config.php"; ?>
<?php require_once "cbus_cgate_functions.php"; ?>
<?php

	/** returns status info from port 20023, something like;
	 *{
	 *	"HOME1-254-56-1" : "255",
	 *	"HOME1-254-56-2" : 77",
	 *	"HOME1-254-56-7" : 255",
	 *	"HOME1-254-56-12" : 255
	 *}
	 */

	$all_levels_str = cbus_cgate_send_message("get_all");
	//echo $all_levels_str;

	// now return the levels to the browser as json	
	header("Content-Type: application/json;charset=utf-8");
	echo cgate_to_json($all_levels_str);
