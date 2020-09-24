<?php require_once "/code/src/widgets.php"; ?>
<?php require_once "/code/src/widget_components.php"; ?>
<?php require_once "/code/config/websocket_config.php"; ?>
<?php

    $interfaces_arr = array();
    $groups_arr = array();
    $sections_arr = array();

    $widgets_json_file = "/code/config/widgets_config.json";
    $widgets_conf_obj = json_decode(file_get_contents($widgets_json_file), true);
    $json_err = json_last_error_msg();
    if ($json_err != 'No error'){
      echo "error with file: ". $widgets_json_file . '<br>';
      echo $json_err;
      exit();
    }

    // use the widgets config json to create an interfaces array, a groups array and a sections array with what widgets are in each group
    foreach ($widgets_conf_obj as $id => $params) {

        $interfaces_arr[] = $params['listener_interface'];
        foreach ($params['groups'] as $group) {
            $groups_arr[] = $group;
            $sections_arr[$group][] = $id;
        }
    }

    $interfaces_arr = array_keys(array_flip($interfaces_arr));
    $interfaces_str = "['" . implode("', '", $interfaces_arr) . "']";

    $groups_arr = array_keys(array_flip($groups_arr));

    $top_groups_str = "";
    foreach ($groups_arr as $i => $val) {
      if ($i == 0) { $top_groups_str .= "            <a name=\"t" . $i . "\" href=\"#scroll-tab-" . $i . "\" class=\"topnav mdl-layout__tab is-active\"><div class=\"navtext\">" . $val . "</div></a>\n"; }
      else { $top_groups_str .= "            <a name=\"t" . $i . "\" href=\"#scroll-tab-" . $i . "\" class=\"topnav mdl-layout__tab\"><div class=\"navtext\">" . $val . "</div></a>\n"; }
    }

    $left_groups_str = "";
    foreach ($groups_arr as $i => $val) {
        $left_groups_str .= "           <li class=\"mdl-list__item\">\n";
        if ($i == 0) { $left_groups_str .= "                <button name=\"t" . $i . "\" class=\"leftnav mdl-button mdl-js-button mdl-js-ripple-effect is-active\">" . $val . "</button>\n"; }
        else { $left_groups_str .= "                <button name=\"t" . $i . "\" class=\"leftnav mdl-button mdl-js-button mdl-js-ripple-effect\">" . $val . "</button>\n"; }
        $left_groups_str .= "            </li>\n";
    }

    $sects_str = "";
    $pagenum = 0;
    foreach ($sections_arr as $group => $group_widgets) {
        if ($pagenum == 0) { $sects_str .= "          <section class=\"mdl-layout__tab-panel is-active\" id=\"scroll-tab-" . $pagenum . "\">"; }
        else { $sects_str .= "          <section class=\"mdl-layout__tab-panel\" id=\"scroll-tab-" . $pagenum . "\">"; }
        $sects_str .= "            <div class=\"mdl-grid\">";

        foreach ($group_widgets as $widget_id) {

            $widget_obj = new crave_widget($pagenum,$widget_id,$widgets_conf_obj);
            $call_func = "get_" . $widgets_conf_obj[$widget_id]['ui_type'];
            $sects_str .= $widget_obj->$call_func();

        }

        $sects_str .= "            </div>\n";
        $sects_str .= "          </section>\n\n";
        $pagenum++;
    }
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="crave control web app.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>Crave Control</title>

    <!-- Add to homescreen for Chrome on Android -->
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" sizes="192x192" href="images/android-desktop.png">

    <!-- Add to homescreen for Safari on iOS -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Material Design Lite">
    <link rel="apple-touch-icon-precomposed" href="images/ios-desktop.png">

    <meta name="theme-color" content="#202020" />

    <!-- Tile icon for Win8 (144x144 + tile color) -->
    <meta name="msapplication-TileImage" content="images/touch/ms-touch-icon-144x144-precomposed.png">
    <meta name="msapplication-TileColor" content="#3372DF">

    <link rel="shortcut icon" href="/public/img/favicon.png">

    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="/public/css/mdl_styles.css">
    <link rel="stylesheet" href="/public/css/styles.css">

    <script src="https://code.getmdl.io/1.3.0/material.min.js"></script> <!-- for mdl -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <!-- for jquery -->
    <script src="/public/js/widget_refresh_functions.js"></script>
    <script>
        $(document).ready(function(){

          ws_host_addr = '<?php echo CONST_ws_host; ?>';
          ws_host_ports = [];
          ws_host_ports['cgate'] = '<?php echo CONST_cgate_ws_port; ?>';
          ws_host_ports['advair'] = '<?php echo CONST_advair_ws_port; ?>';
          ws_sockets = [];
	        ws_last_msg_time = [];

          listner_addresses_arr = <?php echo $interfaces_str; ?>;

          setTimeout(function() {
              spawn_listener_interfaces();
          },1000 );

          $('.leftnav').on('click', function(){
            $('.topnav[name='+this.name+']')[0].click();
            $('.leftnav').removeClass('is-active');
            $('.leftnav[name='+this.name+']').addClass('is-active');
          });

          $('.topnav').on('click', function(){
            $('.leftnav').removeClass('is-active');
            $('.leftnav[name='+this.name+']').addClass('is-active');
          });

        });
    </script>
  </head>
  <body>
    <div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">

      <header class="mdl-layout__header mdl-color-text--white">
        <div class="mdl-layout__header-row">
          <span class="mdl-layout-title">&lt; crave control &gt;</span>
          <div class="mdl-layout-spacer"></div>
          <div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable">
            <label class="mdl-button mdl-js-button mdl-button--icon" for="search">
              <i class="material-icons">search</i>
            </label>
            <div class="mdl-textfield__expandable-holder">
              <input class="mdl-textfield__input" type="text" id="search">
              <label class="mdl-textfield__label" for="search">Enter your query...</label>
            </div>
          </div>
          <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn">
            <i class="material-icons">more_vert</i>
          </button>
          <ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn">
            <li class="mdl-menu__item">About</li>
            <li class="mdl-menu__item">Contact</li>
            <li class="mdl-menu__item">Legal information</li>
          </ul>
        </div>
          <!-- top tabs -->
          <div class="mdl-layout__tab-bar mdl-js-ripple-effect">
<?php echo $top_groups_str; ?>
          </div>
      </header>

      <main class="mdl-layout__content">

        <div class="leftside">
          <ul class="mdl-list">
<?php echo $left_groups_str; ?>
          </ul>
        </div> <!-- end leftside -->

        <div class="rightside">
<?php echo $sects_str; ?>
        </div> <!-- end rightside -->

      </main>

    </div> <!-- end mdl layout -->
  </body>
</html>