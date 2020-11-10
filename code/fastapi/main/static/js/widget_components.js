
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au


//////////////////////////////////////////////////////////////
  function get_listener_1(comp_div_id, comp_obj, listener_type, state_key) {
    // eg. comp_type = slider or switch
    // eg. comp_subtype = mdl1 or mdc1 (ie. material design lite or material design components)

    ret_str  = '<input value="x" class="hdn_lst listener_value ' + safe_class(comp_obj['devices'][0]) + '__' + state_key + '"';
    ret_str += ' onchange="listener_val_changed(\'' + comp_div_id + '\');"';
    ret_str += ' >\n';
    ret_str += '<input value="0" class="hdn_lst listener_time"';
    ret_str += ' onchange="' + listener_type + '_listener_time_changed(\'' + comp_div_id + '\');"';
    ret_str += ' >\n';
    ret_str += '<input value="0" class="hdn_lst updated_time">\n';
    ret_str += '<input value="x" class="hdn_lst value_by_listener">\n';

    return ret_str;
  }

  //////////////////////////////////////////////////////////////
  function get_slider_1(comp_div_id, comp_obj, state_key) {

    var cmd = '';
    if ('command' in comp_obj) { cmd = comp_obj['command']; }
    else { cmd = 'set_widget_val'; }

    ret_str  = '<p class="component_value_elem">\n';
    ret_str += '  <input id="' + comp_div_id + '_main" class="component_value mdl-slider mdl-js-slider slider_mdl1" type="range" min="0" max="100" value="0" tabindex="0"';
    ret_str += ' onchange="slider_value_changed(\'' + comp_div_id + '\',\'' + cmd + '\',\'' + state_key + '\',this.value,\'' + comp_obj['widget_id'] + '\');"';
    ret_str += ' >\n';
    ret_str += '</p>\n';

    return ret_str;
  }

  //////////////////////////////////////////////////////////////
  function get_switch_1(comp_div_id, comp_obj, state_key) {

    var cmd = '';
    if ('command' in comp_obj) { cmd = comp_obj['command']; }
    else { cmd = 'set_widget_val'; }

    ret_str  = '<label id="' + comp_div_id + '_l" for="' + comp_div_id + '_main" class="mdl-switch mdl-js-switch">\n';
    ret_str += ' <input id="' + comp_div_id + '_main" type="checkbox" class="widget_value switch_mdl1 mdl-switch__input"';
    ret_str += ' onchange="switch_value_changed(\'' + comp_div_id + '\',\'' + cmd + '\',\'' + state_key + '\',this.checked,\'' + comp_obj['widget_id'] + '\');"';
    ret_str += ' >\n';
    ret_str += '</label>\n';

    return ret_str;
  }