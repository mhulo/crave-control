<?php require_once "advair_ma5_config.php"; ?>
<?php require_once "../../../config/websocket_config.php"; ?>
<?php require_once "../../core_functions.php"; ?>
<?php require_once "advair_ma5_functions.php"; ?>
<?php

	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // create TCP/IP sream socket
	socket_set_option($socket, SOL_SOCKET, SO_REUSEADDR, 1); // set to be a reuseable port
	socket_bind($socket, 0, CONST_advair_ma5_ws_port); // bind socket to specified host
	socket_listen($socket); // start listening for connections on $socket

	// variables for socket_select
	$write=NULL;
	$exceptions=NULL;

	//create the list of sockets we are managing, and first up add the server/daemon socket to the list
	$client_sockets = [$socket];
	$levels_data = "";
	$last_change = 0; // the last time anything changed in ms timestamp
	$new_socket_client = false;

	// **** temporarily set this so that it runs for a bit from the browser ***
	//set_time_limit(60);

	//start endless loop, so that our script doesn't stop
	while ((file_exists("interfaces/advair_ma5/keep_running.txt")) || (file_exists("keep_running.txt"))) {

		// essentiallly poll for a change to any socket within the $client_sockets array and
		// then create and update a new array called $changed_sockets which will be an array of whatever sockets changed
		// ie. !!! socket_select actually changes the $changed_sockets array !!!
		// this will wait 10 microseconds for a change then just go
		$changed_sockets = $client_sockets; // need a variable for socket_select to mess with, so start with our client sockets array
		socket_select($changed_sockets, $write, $exceptions, 0, 10);

		// if our listen socket had a change then that means we have a new connection
		if (in_array($socket, $changed_sockets)) {
			$socket_new = socket_accept($socket); //find out what socket just connected to our listen socket and call it $socket_new
			$client_sockets[] = $socket_new; //add $socket_new to client array
			$header = socket_read($socket_new, 1024); //read header data sent by the socket
			perform_ws_handshake($header, $socket_new, CONST_ws_host, CONST_ws_port); //perform websocket handshake

			// now just to make sure that this new client has the latest levels set a var to trigger a message to be sent
			$new_socket_client = true;

			//we dont want our listen socket to be one of the sockets we iterate through for the next bit of this iteration of the while loop so take it out
			$found_socket = array_search($socket, $changed_sockets);
			unset($changed_sockets[$found_socket]);
		}

		//loop through all sockets that had a change (ie. except for our listen one - the server / daemon - that we just removed)
		foreach ($changed_sockets as $changed_socket) {

			// detect that someone disconnected because there was a change, but no message
			$buf = @socket_read($changed_socket, 1024, PHP_NORMAL_READ);
			if ($buf === false) { // check disconnected client
				$found_socket = array_search($changed_socket, $client_sockets);
				unset($client_sockets[$found_socket]); // remove client for $client_sockets array
			}
		}

		// keep polling the current levels to make sure we have the right levels
		$latest_data = issue_curl_cmd("http://" . CONST_advair_ma5_host_url . ":" . CONST_advair_ma5_host_port . "/getSystemData");

        if (($latest_data != $levels_data) || ($new_socket_client == true)) { // if its different - tell everyone and update levels and last change time
			$response = websocket_message_mask(ma5_to_json($latest_data));
			websocket_send_message($response);

			if ($latest_data != $levels_data) {
				$last_change = round(microtime(true) * 1000);
				$levels_data = $latest_data; // update the global with the fresh levels data
			}

			$new_socket_client = false;
		}

		if ((round(microtime(true) * 1000) - $last_change) < 60000) {
			usleep(1000000); // sleep for 1000ms then go again
		}
		else { // ie. if no action for 1 min, go into sleep mode
			usleep(3000000); // sleep for 3000ms then go again
		}

	} // end while loop

	echo "stopped";
