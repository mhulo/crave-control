
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au

//////////////////////////////////////////////////////////////
  var cards = {

    dimmer_1 : function(wgt_obj) {

      wgt_div_id = wgt_obj['page_num'] + '_' + wgt_obj['item_num'] + '_' + wgt_obj['card_id'];
      comp_div_id = wgt_div_id + '_slider';

      ret_str  = '<div class="cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop">\n';
      ret_str += ' <div class="label_row">\n';
      ret_str += '   <span>' + wgt_obj['label'] + '</span>\n';
      ret_str += '   <span id="' + comp_div_id + '_label" class="level_label">0%</span>\n';
      ret_str += '   <button class="mdl-button mdl-js-button mdl-button--fab" onclick="toggle_faves(\'' + comp_div_id + '\');"><i class="material-icons">keyboard_arrow_down</i></button>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="interface_row">\n';
      ret_str += '   <span>' + wgt_obj['devices'][0] + ' | </span>\n';
      ret_str += '   <span id="' + comp_div_id + '_listener_label" class="mdl_dimmer_listener_label">0%</span>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="icon_row">\n';
      ret_str += '   <button id="' + comp_div_id + '_icon" class="card_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'' + wgt_obj['card_id'] + '\',\'' + comp_div_id + '\',\'toggle\');"><i class="material-icons">lightbulb_outline</i></button>\n';
      ret_str += '   <div id="' + comp_div_id + '" class="component_container slider_mdl1">';

      ret_str += get_slider_1(comp_div_id, wgt_obj, 'brightness');
      ret_str += get_listener_1(comp_div_id, wgt_obj, 'slider', 'brightness');

      ret_str += '   </div>\n';
      ret_str += ' </div>\n';

      ret_str += ' <div id="' + comp_div_id + '_faves" class="faves_row">\n';
      ret_str += '   <button class="f1 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'' + wgt_obj['card_id'] + '\',\'' + comp_div_id + '\',\'minus\');"><i class="material-icons">remove</i></button>\n';
      ret_str += '   <button class="f2 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'' + wgt_obj['card_id'] + '\',\'' + comp_div_id + '\',\'' + wgt_obj['fave_1'] + '\');"><span>' + wgt_obj['fave_1'] + '%</span></button>\n';
      ret_str += '   <button class="f4 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'' + wgt_obj['card_id'] + '\',\'' + comp_div_id + '\',\'plus\');"><i class="material-icons">add</i></button>\n';
      ret_str += '   <button class="f3 mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="slider_adjust(\'' + wgt_obj['card_id'] + '\',\'' + comp_div_id + '\',\'' + wgt_obj['fave_2'] + '\');"><span>' + wgt_obj['fave_2'] + '%</span></button>\n';
      ret_str += ' </div>\n';

      ret_str += '</div>\n';

      return ret_str;
    },

    switch_1 : function(wgt_obj) {

      wgt_div_id = wgt_obj['page_num'] + '_' + wgt_obj['item_num'] + '_' + wgt_obj['card_id'];
      comp_div_id = wgt_div_id + '_toggle';

      ret_str  = '<div class="cvcard mdl-cell mdl-cell--8-col mdl-cell--6-col-desktop">\n';
      ret_str += ' <div class="label_row">\n';
      ret_str += '   <span>' + wgt_obj['label'] + '</span>\n';
      ret_str += '   <span id="' + comp_div_id + '_label" class="level_label">OFF</span>\n';
      ret_str += '   <button class="mdl-button mdl-js-button mdl-button--fab" onclick="toggle_faves(\'' + comp_div_id + '\');"><i class="material-icons">keyboard_arrow_down</i></button>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="interface_row">\n';
      ret_str += '   <span>' + wgt_obj['devices'][0] + ' | </span>\n';
      ret_str += '   <span id="' + comp_div_id + '_listener_label" class="mdl_dimmer_listener_label">off</span>\n';
      ret_str += ' </div>\n';
      ret_str += ' <div class="icon_row">\n';
      ret_str += '   <button id="' + comp_div_id + '_icon" class="card_icon mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect" onclick="switch_adjust(\'' + comp_div_id + '\',\'toggle\');"><i class="material-icons">lightbulb_outline</i></button>\n';
      ret_str += '   <div id="' + comp_div_id + '" class="component_container slider_mdl1">';

      ret_str += get_switch_1(comp_div_id, wgt_obj, 'power');
      ret_str += get_listener_1(comp_div_id, wgt_obj, 'switch', 'power');

      ret_str += '   </div>\n';
      ret_str += ' </div>\n';

      ret_str += ' <div id="' + comp_div_id + '_faves" class="faves_row">\n';
      ret_str += ' </div>\n';

      ret_str += '</div>\n';

      return ret_str;
    }

  };

//////////////////////////////////////////////////////////////
