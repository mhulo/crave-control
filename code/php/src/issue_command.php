<?php require_once "core_functions.php"; ?>
<?php require_once "action_functions.php"; ?>
<?php require_once "interfaces/cbus_cgate/cbus_cgate_config.php"; ?>
<?php require_once "interfaces/cbus_cgate/cbus_cgate_functions.php"; ?>
<?php require_once "interfaces/advair_ma5/advair_ma5_config.php"; ?>
<?php require_once "interfaces/advair_ma5/advair_ma5_functions.php"; ?>
<?php

  /**
   * only needs get params, works out what actions to run for the given $_GET['cmd']
   * and then what function for each action, then runs each action one at a time
   */
  set_time_limit(5);

  function run_command() { 
    $command = json_decode(file_get_contents("../config/commands_config.json"), true);
    foreach ($command[$_GET['cmd']]['actions'] as $action) { // iterate through all the actions in the command
        $action['action_function']($action['action_params']); // run each action - which are all php functions
        set_time_limit(5);
    }
  }

 run_command();