<?php

$router->get('/admin/', function($request) { return useView('admin/index', $request); });
$router->get('/home/', function($request) { return useView('home/index', $request); });
$router->get('//', function($request) { return useView('home/index', $request); });

$router->get('/api/cgate/level_dim/{device_id}/{set_val}/{ramp_time}', function($request) { return useContr('modules/cgate/cgateController@levelDim', $request); });
$router->get('/api/cgate/level_toggle/{device_id}/{set_val}', function($request) { return useContr('modules/cgate/cgateController@levelToggle', $request); });
$router->get('/api/cgate/levels', function($request) { return useContr('modules/cgate/cgateController@levelsShow', $request); });
$router->get('/api/cgate/start', function($request) { return useContr('modules/cgate/cgateController@startDaemon', $request); });
$router->get('/api/cgate/stop', function($request) { return useContr('modules/cgate/cgateController@stopDaemon', $request); });
$router->get('/api/cgate/noop', function($request) { return useContr('modules/cgate/cgateController@noopTest', $request); });

$router->get('/api/action/{module}/level_dim/{device_id}/{set_val}/{ramp_time}', function($request) { return useContr('modules/core/actionController@levelDim', $request); });
$router->get('/api/command/run/{command_params}', function($request) { return useContr('modules/core/commandController@runCommand', $request); });
