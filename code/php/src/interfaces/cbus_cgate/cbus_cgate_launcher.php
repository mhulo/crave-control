<?php

	if ($_GET["interface"] == "cbus_cgate") {

		$run_file = "keep_running.txt";

		if ($_GET["action"] == "start") {

			// create a file that the daemon while loop can check to see if it should continue or not
			$handle = fopen($run_file, "w") or die("cannot create file:  ". $run_file); //implicitly creates file
			fclose($handle);
			exec("php cbus_cgate_interface.php", $output);
			var_dump($output);

		}
		elseif ($_GET["action"] == "stop") {

			// delete the file so the while loop will stop
			unlink($run_file);
		}

	}
