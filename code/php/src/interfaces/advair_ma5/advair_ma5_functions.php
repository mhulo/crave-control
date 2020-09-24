<?php require_once "advair_ma5_config.php"; ?>
<?php

    function ma5_to_json($ma5_text)
    {
        $interface = "advair_ma5";
        $used_main_fields = array("setTemp", "state", "airconErrorCode", "fan", "filterCleanStatus", "mode", "myZone");
        $used_zone_fields = array("error", "measuredTemp", "name", "setTemp", "state", "value");
        $ret_str = "";

        $ma5_text_obj = json_decode($ma5_text);
        $aircons_obj = $ma5_text_obj->aircons;

        foreach ($aircons_obj as $aircon => $aircon_vals_obj) {

            //first iterate through the main info for this ac
            foreach ($aircon_vals_obj->info as $main_info_key => $main_info_val) {
            	if (in_array($main_info_key, $used_main_fields)) {
		    		$ret_str .= "    \"" . $interface . "__" . $aircon . "_main__" . $main_info_key . "\" : \"" .  $main_info_val . "\",\n";
				}
            }

            //now iterate through each zone
            foreach ($aircon_vals_obj->zones as $zone_key => $zone_vals) {
	            foreach ($zone_vals as $zone_info_key => $zone_info_val) {
	            	if (in_array($zone_info_key, $used_zone_fields)) {
		    		$ret_str .= "    \"" . $interface . "__" . $aircon . "_" . $zone_key . "__" . $zone_info_key . "\" : \"" .  $zone_info_val . "\",\n";
					}
	            }
            }
        }

        return "{\n" . substr($ret_str,0,-2) . "\n}";
    }