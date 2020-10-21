
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au

//////////////////////////////////////////////////////////////
  var widgets = {

    dimmer_1 : function(page_num, item_num, widget_id, widget_obj) {

      widget_div_id = page_num + '_' + item_num + '_' + widget_id;
      comp_div_id = widget_div_id + '_slider';
      listener_type = 'slider_mdl1';

      ret_str  = '<div class="cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop">\n';
      ret_str += ' <div class="label_row">\n';
      ret_str += '   <span>' + widget_obj['name'] + '</span>\n';
      ret_str += '   <span id="' + comp_div_id + '_label" class="level_label">0%</span>\n';
      ret_str += '   <button class="mdl-button mdl-js-button mdl-button--fab" onclick="toggle_faves(\'' + comp_div_id + '\');"><i class="material-icons">keyboard_arrow_down</i></button>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="interface_row">\n';
      ret_str += '   <span>' + widget_obj['listener_interface'] + ' | ' + widget_obj['listener_device_id'] + ' | </span>\n';
      ret_str += '   <span id="' + comp_div_id + '_listener_label" class="mdl_dimmer_listener_label">0%</span>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="icon_row">\n';
      ret_str += '   <button id="' + comp_div_id + '_icon" class="widget_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'toggle\');"><i class="material-icons">lightbulb_outline</i></button>\n';
      ret_str += '   <div id="' + comp_div_id + '" class="component_container slider_mdl1">';

      ret_str += get_slider_mdl1(comp_div_id, widget_obj);
      ret_str += get_listener(comp_div_id, widget_obj, listener_type);

      ret_str += '   </div>\n';
      ret_str += ' </div>\n';

      ret_str += ' <div id="' + comp_div_id + '_faves" class="faves_row">\n';
      ret_str += '   <button class="f1 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'minus\');"><i class="material-icons">remove</i></button>\n';
      ret_str += '   <button class="f2 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'' + widget_obj['fave_percentage_1'] + '\');"><span>' + widget_obj['fave_percentage_1'] + '%</span></button>\n';
      ret_str += '   <button class="f4 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'plus\');"><i class="material-icons">add</i></button>\n';
      ret_str += '   <button class="f3 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'' + widget_obj['fave_percentage_2'] + '\');"><span>' + widget_obj['fave_percentage_2'] + '%</span></button>\n';
      ret_str += ' </div>\n';

      ret_str += '</div>\n';

      return ret_str;
    },

    switch_1 : function(page_num, item_num, widget_id, widget_obj) {

      widget_div_id = page_num + '_' + item_num + '_' + widget_id;
      comp_div_id = widget_div_id + '_toggle';
      listener_type = 'toggle_mdl1';

      ret_str  = '<div class="cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop">\n';
      ret_str += ' <div class="label_row">\n';
      ret_str += '   <span>' + widget_obj['name'] + '</span>\n';
      ret_str += '   <span id="' + comp_div_id + '_label" class="level_label">0%</span>\n';
      ret_str += '   <button class="mdl-button mdl-js-button mdl-button--fab" onclick="toggle_faves(\'' + comp_div_id + '\');"><i class="material-icons">keyboard_arrow_down</i></button>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="interface_row">\n';
      ret_str += '   <span>' + widget_obj['listener_interface'] + ' | ' + widget_obj['listener_device_id'] + ' | </span>\n';
      ret_str += '   <span id="' + comp_div_id + '_listener_label" class="mdl_dimmer_listener_label">0%</span>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="icon_row">\n';
      ret_str += '   <button id="' + comp_div_id + '_icon" class="widget_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'mdl1\',\'' + comp_div_id + '\',\'toggle\');"><i class="material-icons">lightbulb_outline</i></button>\n';
      ret_str += '   <div id="' + comp_div_id + '" class="component_container slider_mdl1">';

      ret_str += get_slider_mdl1(comp_div_id, widget_obj);
      ret_str += get_listener(comp_div_id, widget_obj, listener_type);

      ret_str += '   </div>\n';
      ret_str += ' </div>\n';

      ret_str += ' <div id="' + comp_div_id + '_faves" class="faves_row">\n';
      ret_str += ' </div>\n';

      ret_str += '</div>\n';

      return ret_str;
    }

  };

//////////////////////////////////////////////////////////////
