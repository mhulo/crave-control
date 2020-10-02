<?php

    class crave_component
    {
        public $widget_div_id;
        public $val_type;
        public $widget_command;
        public $listener_interface;
        public $listener_id;

        /**
         * Creates the base crave_component object which can then the various methods to insert all the widget components on the pages in html.
         *
         * @param string $widget_div_id Takes the id of the widget div so that the components be named and addressed based off that eg. "1_w0001".
         * @param string $widget_command Takes the id of the command as specified in the widgets_config.json file eg. "command_1".
         * @param string $listener_interface Takes the name of the listener_interface for this widget eg. "cgate".
         * @param string $listener_id Takes the name of the listener_id for the widget eg. "HOME1_254_56_12".
         */
        public function __construct($widget_div_id,$widget_command,$listener_interface,$listener_id)
        {
            $this->widget_div_id = $widget_div_id;
            $this->widget_command = $widget_command;
            $this->listener_interface = $listener_interface;
            $this->listener_id = $listener_id;
        }

        /**
         * Creates the base crave_component object which can then the various methods to insert all the widget components on the pages in html.
         *
         * @param string $comp_type Takes name of the component type that is being inserted eg. "dimmer" or "switch".
         * @param string $comp_subtype Takes name of the component subtype that is being inserted eg. "mdl1" or "mdc".
         * @param object $comp_id Takes the unique id of the component so that the divs in the generated html will have unique ids eg. "c01"
         * @param object $val_type Takes the name type of value this component will be working with and listening to eg. "level" or "set_temp"
         * @return string $ret_str Returns the string of html for this component
         */
        public function get_listener($comp_type,$comp_subtype,$comp_id,$val_type)
        {
            // eg. comp_type = slider or switch
            // eg. comp_subtype = mdl1 or mdc1 (ie. material design lite or material design components)

            $comp_div_id = $this->widget_div_id . "_" . $comp_id;

            $ret_str  = "    <input value=\"x\" class=\"hdn_lst listener_value " . $this->listener_interface . "__" . $this->listener_id . "__" . $val_type . "\"";
            $ret_str .= " onchange=\"listener_val_changed('" . $comp_div_id . "');\"";
            $ret_str .= " >\n";
            $ret_str .= "    <input value=\"0\" class=\"hdn_lst listener_time\"";
            $ret_str .= " onchange=\"" . $comp_type . "_listener_time_changed('" . $comp_subtype . "', '" . $comp_div_id . "');\"";
            $ret_str .= " >\n";
            $ret_str .= "    <input value=\"0\" class=\"hdn_lst updated_time\">\n";
            $ret_str .= "    <input value=\"x\" class=\"hdn_lst value_by_listener\">\n";

            return $ret_str;
        }

        /**
         * Creates the html string for the specific crave_component which will be inserted by the widget.
         *
         * @param object $comp_id Takes the unique id of the component so that the divs in the generated html will have unique ids eg. "c01"
         * @param object $val_type Takes the name type of value this component will be working with and listening to eg. "level" or "set_temp"
         * @return string $ret_str Returns the string of html for this component
         */
        public function get_slider_mdl1($comp_id,$val_type)
        {
            $comp_div_id = $this->widget_div_id . "_" . $comp_id;

            $ret_str  = "    <p class=\"component_value_elem\">\n";
            $ret_str .= "        <input id=\"" . $comp_div_id . "_main\" class=\"component_value mdl-slider mdl-js-slider slider_mdl1\" type=\"range\" min=\"0\" max=\"100\" value=\"0\" tabindex=\"0\"";
            $ret_str .= " onchange=\"slider_value_changed(this.value,'mdl1','" . $comp_div_id . "','" . $this->widget_command . "');\"";
            $ret_str .= " >\n";
            $ret_str .= "     </p>\n";
            $ret_str .= $this->get_listener("slider", "mdl1", $comp_id, $val_type);

            return $ret_str;
        }

        /**
         * Creates the html string for the specific crave_component which will be inserted by the widget.
         *
         * @param object $comp_id Takes the unique id of the component so that the divs in the generated html will have unique ids eg. "c01"
         * @param object $val_type Takes the name type of value this component will be working with and listening to eg. "level" or "set_temp"
         * @return string $ret_str Returns the string of html for this component
         */
        public function get_switch_mdl1($comp_id,$val_type)
        {
            $comp_div_id = $this->widget_div_id . "_" . $comp_id;

            $ret_str  = "    <label id=\"" . $comp_div_id . "_l\" for=\"" . $comp_div_id . "_main\" class=\"mdl-switch mdl-js-switch\">\n";
            $ret_str .= "        <input id=\"" . $comp_div_id . "_main\" type=\"checkbox\" class=\"widget_value switch_mdl1 mdl-switch__input\"";
            $ret_str .= " onchange=\"switch_value_changed(this.checked, 'mdl1', '" . $comp_div_id . "', '" . $this->widget_command . "');\"";
            $ret_str .= " >\n";
            $ret_str .= "    </label>\n";
            $ret_str .= $this->get_listener("switch", "mdl1", $comp_id, $val_type);

            return $ret_str;
        }
    }
