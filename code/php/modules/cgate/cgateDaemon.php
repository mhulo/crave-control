<?php 

  require_once '/code/modules/cgate/cgateCommon.php';
  require_once '/code/modules/core/websocket.php';
  require_once "/code/config/websocket_config.php";

  $cgate_wsocket = new crave_wsocket('cgate', CONST_cgate_ws_port);
  $cgate_wsocket->start_ws_daemon();
