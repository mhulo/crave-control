<?php

    class crave_widget
    {
        public $pagenum;
        public $widget_id;
        public $widgets_conf_obj;

        /**
         * Creates the base crave_widget object which can then the various methods to insert all the widgets on the pages in html.
         *
         * @param int $pagenum Takes the index of the page that the widget is to be shown on. Used so that duplicate widgets can be shown on different pages but with unique id's.
         * @param string $widget_id Takes the top level key for each widget based on what is in the widgets_config.json file.
         * @param object $widgets_conf_obj Takes the json decoded object from the widgets_config.json file.
         */
        public function __construct($pagenum,$widget_id,$widgets_conf_obj)
        {
            $this->pagenum = $pagenum;
            $this->widget_id = $widget_id;
            $this->widgets_conf_obj = $widgets_conf_obj;
        }

        /**
         * @return string $ret_str Returns a string containing html to insert a dimmer_1 widget which is for lights and uses various MDL components.
         */
        public function get_dimmer_1()
        {
            $widget_div_id = $this->pagenum . "_" . $this->widget_id;
            $widget_comp_obj = new crave_component($widget_div_id,$this->widgets_conf_obj[$this->widget_id]["command"],$this->widgets_conf_obj[$this->widget_id]["listener_interface"],$this->widgets_conf_obj[$this->widget_id]["listener_device_id"]);

            $c01_id = "c01";
            $c01_val_type = "level";
            $c01_div_id = $widget_div_id . "_" . $c01_id;

            $ret_str  = "<div class=\"cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop\">\n";
            $ret_str .= " <div class=\"label_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['name'] . "</span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_label\" class=\"level_label\">0%</span>\n";
            $ret_str .= "   <button class=\"mdl-button mdl-js-button mdl-button--fab\" onclick=\"toggle_faves('" . $c01_div_id . "');\"><i class=\"material-icons\">keyboard_arrow_down</i></button>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"interface_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['listener_interface'] . " | " . $this->widgets_conf_obj[$this->widget_id]['listener_device_id'] . " | </span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_listener_label\" class=\"mdl_dimmer_listener_label\">0%</span>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"icon_row\">\n";
            $ret_str .= "   <button id=\"" . $c01_div_id . "_icon\" class=\"widget_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','toggle');\"><i class=\"material-icons\">lightbulb_outline</i></button>\n";
            $ret_str .= "   <div id=\"" . $c01_div_id . "\" class=\"component_container slider_mdl1\">";
            $ret_str .= $widget_comp_obj->get_slider_mdl1($c01_id,$c01_val_type);
            $ret_str .= "   </div>\n";
            $ret_str .= " </div>\n";

            $ret_str .= " <div id=\"" . $c01_div_id . "_faves\" class=\"faves_row\">\n";
            $ret_str .= "   <button class=\"f1 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','minus');\"><i class=\"material-icons\">remove</i></button>\n";
            $ret_str .= "   <button class=\"f2 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_1'] . "');\"><span>" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_1'] . "%</span></button>\n";
            $ret_str .= "   <button class=\"f4 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','plus');\"><i class=\"material-icons\">add</i></button>\n";
            $ret_str .= "   <button class=\"f3 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_2'] . "');\"><span>" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_2'] . "%</span></button>\n";
            $ret_str .= " </div>\n";

            $ret_str .= "</div>\n";

            return $ret_str;
        }

        /**
         * @return string $ret_str Returns a string containing html to insert a switch_1 widget which is for lights and uses various MDL components.
         */
        public function get_switch_1()
        {
            $widget_div_id = $this->pagenum . "_" . $this->widget_id;
            $widget_comp_obj = new crave_component($widget_div_id,$this->widgets_conf_obj[$this->widget_id]["command"],$this->widgets_conf_obj[$this->widget_id]["listener_interface"],$this->widgets_conf_obj[$this->widget_id]["listener_device_id"]);

            $c01_id = "c01";
            $c01_val_type = "level";
            $c01_div_id = $widget_div_id . "_" . $c01_id;

            $ret_str  = "<div class=\"cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop\">\n";
            $ret_str .= " <div class=\"label_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['name'] . "</span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_label\" class=\"level_label\">OFF</span>\n";
            $ret_str .= "   <button class=\"mdl-button mdl-js-button mdl-button--fab\" onclick=\"toggle_faves('" . $c01_div_id . "');\"><i class=\"material-icons\">keyboard_arrow_down</i></button>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"interface_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['listener_interface'] . " | " . $this->widgets_conf_obj[$this->widget_id]['listener_device_id'] . " | </span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_listener_label\" class=\"mdl_dimmer_listener_label\">0%</span>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"icon_row\">\n";
            $ret_str .= "   <button id=\"" . $c01_div_id . "_icon\" class=\"widget_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"switch_adjust('mdl1','" . $c01_div_id . "','toggle');\"><i class=\"material-icons\">lightbulb_outline</i></button>\n";
            $ret_str .= "   <div id=\"" . $c01_div_id . "\" class=\"component_container slider_mdl1\">";
            $ret_str .= $widget_comp_obj->get_switch_mdl1($c01_id,$c01_val_type);
            $ret_str .= "  </div>\n";
            $ret_str .= " </div>\n";

            $ret_str .= " <div id=\"" . $c01_div_id . "_faves\" class=\"faves_row\">\n";
            $ret_str .= " </div>\n";

            $ret_str .= "</div>\n";

            return $ret_str;
        }

        /**
         * @return string $ret_str Returns a string containing html to insert a ac_zone_1 widget which is for aircon and uses various MDL components.
         */
        public function get_aczone_1()
        {
            $widget_div_id = $this->pagenum . "_" . $this->widget_id;
            $widget_comp_obj = new crave_component($widget_div_id,$this->widgets_conf_obj[$this->widget_id]["command"],$this->widgets_conf_obj[$this->widget_id]["listener_interface"],$this->widgets_conf_obj[$this->widget_id]["listener_device_id"]);

            $c01_id = "c01";
            $c01_val_type = "value";
            $c01_div_id = $widget_div_id . "_" . $c01_id;

            $ret_str  = "<div class=\"cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop\">\n";
            $ret_str .= " <div class=\"label_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['name'] . "</span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_label\" class=\"value_label\">0%</span>\n";
            $ret_str .= "   <button class=\"mdl-button mdl-js-button mdl-button--fab\" onclick=\"toggle_faves('" . $c01_div_id . "');\"><i class=\"material-icons\">keyboard_arrow_down</i></button>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"interface_row\">\n";
            $ret_str .= "   <span>" . $this->widgets_conf_obj[$this->widget_id]['listener_interface'] . " | " . $this->widgets_conf_obj[$this->widget_id]['listener_device_id'] . " | </span>\n";
            $ret_str .= "   <span id=\"" . $c01_div_id . "_listener_label\" class=\"mdl_dimmer_listener_label\">0%</span>\n";
            $ret_str .= " </div>\n";
            $ret_str .= " <div class=\"icon_row\">\n";
            $ret_str .= "   <button id=\"" . $c01_div_id . "_icon\" class=\"widget_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','toggle');\"><i class=\"material-icons\">lightbulb_outline</i></button>\n";
            $ret_str .= "   <div id=\"" . $c01_div_id . "\" class=\"component_container slider_mdl1\">";
            $ret_str .= $widget_comp_obj->get_slider_mdl1($c01_id,$c01_val_type);
            $ret_str .= "   </div>\n";
            $ret_str .= " </div>\n";

            $ret_str .= " <div id=\"" . $c01_div_id . "_faves\" class=\"faves_row\">\n";
            $ret_str .= "   <button class=\"f1 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','minus');\"><i class=\"material-icons\">remove</i></button>\n";
            $ret_str .= "   <button class=\"f2 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_1'] . "');\"><span>" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_1'] . "%</span></button>\n";
            $ret_str .= "   <button class=\"f4 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','plus');\"><i class=\"material-icons\">add</i></button>\n";
            $ret_str .= "   <button class=\"f3 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect\" onclick=\"slider_adjust('mdl1','" . $c01_div_id . "','" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_2'] . "');\"><span>" . $this->widgets_conf_obj[$this->widget_id]['fave_percentage_2'] . "%</span></button>\n";
            $ret_str .= " </div>\n";

            $ret_str .= "</div>\n";

            return $ret_str;
        }
    }