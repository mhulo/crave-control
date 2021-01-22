
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    $(document).on('click', '.leftnav', function() {
      $('.topnav[name='+this.name+']')[0].click();
      $('.leftnav').removeClass('is-active');
      $('.leftnav[name='+this.name+']').addClass('is-active');
    });

    $(document).on('click', '.toptnav', function() {
      $('.leftnav').removeClass('is-active');
      $('.leftnav[name='+this.name+']').addClass('is-active');
    });
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    var g_abort;
    var timeoutID;
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function get_rand_ext() {
        var currentTime = new Date();
        var rand_ext = currentTime.getTime();
        return rand_ext;
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function get_live_status() {        

        // get a refreshed set of values for the given interface
        //create a new websocket object.
        var wss = {}
        wss['id'] = Date.now();
        wss['host'] = location.hostname;
        if (location.protocol == 'https:') {
          wss['protocol'] = 'wss';
          wss['port'] = '';
        }
        else {
          wss['protocol'] = 'ws';
          wss['port'] = ':' + location.port;
        }

        socket_uri = wss['protocol'] + '://' + wss['host'] + wss['port'] + '/api/core/wss/' + wss['id'] + '/'; 
        ws_sockets = new WebSocket(socket_uri);

        ws_sockets.onopen = function(ev) { // connection is open 
          console.log('connected to websocket interface');
        };

        // message received on websocket from server
        ws_sockets.onmessage = function(ev){
          //console.log('got something');
          ws_last_msg_time = $.now(); // keep track of how recently anything was sent to this interface
          //console.log('last='+ws_last_msg_time[interface]);

          if (ev.data == 'pong') {
              console.log(ev.data+' received');
          }
          else {
            //console.log('ws data: ' + ev.data);
            var state_data = JSON.parse(ev.data); // daemon via websocket sends json data
            $.each(state_data, function(key1,val1){
              if (typeof val1 == 'string') {
                if (key1 == 'message') {
                  console.log(key1 + ': ' + val1);
                }
              }
              else {
                $.each(val1, function(key2,val2){
                  $.each(val2, function(key3,val3){
                    device_id = key1+'__'+key2+'__'+key3;
                    if (($('.'+device_id).length) && ($('.'+device_id).val() != val3)) { // if the value exists and is different to the network
                      $('.'+device_id).val(val3); // update it
                      $('.'+device_id).trigger('change');
                    }
                  });
                });
              }
            });
          }
        };

        ws_sockets.onerror   = function(ev){
          console.log('error on websocket interface');
        };

        ws_sockets.onclose   = function(ev){
          console.log('disconnected from websocket interface');
          //try to reconnect in 5 seconds

          setTimeout(function(){
            if (ws_sockets.readyState != 1) { // if something else hasn't triggered a re-connect already
              console.log('waited 5 secs.. reconnecting');
              get_live_status();
            }
          }, 5000);

        };
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////

    function check_socket_active() {

      if (ws_sockets.readyState == 1) {
          //console.log('got here');
          if ((($.now() - ws_last_msg_time) > 2000) && (($.now() - ws_last_msg_time) < 10000)) { // if update in the last 2 to 10 secs range, send a ping then go again
              ws_sockets.send('ping');
              console.log('ping sent');

              setTimeout(function() {
                  check_socket_active();
              },2000 ); // go again in 2 secs
          }
          else if (($.now() - ws_last_msg_time) > 10000)  { // if update longer than 10 secs ago, reconnect
              ws_sockets.close();
              get_live_status();
          }
      }
      else if (ws_sockets.readyState > 1) {
        get_live_status();
      }
    }

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_check_action_fired(comp_div_id) {

        listener_time = $('#'+comp_div_id+' .listener_time').val();
        listener_val = $('#'+comp_div_id+' .listener_value').val();
        if (listener_val == "x") { listener_val = 0; }
        comp_val = $('#'+comp_div_id+'_main').val();

        if ((($.now() - listener_time) > 6000) && (comp_val != listener_val)) { // no change at all and val still not same as listener, so set the card back to the listener val
            console.log('setting slider to: '+listener_val);
            $('#'+comp_div_id+' .listener_value').val(listener_val); // update the slider by faking a change on listener. need to do it this way so it wont fire any event.
            $('#'+comp_div_id+' .listener_value').trigger('change');
        }
        else {
            //console.log("something happened");
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function switch_check_action_fired(comp_div_id) {

      listener_time = $('#'+comp_div_id+' .listener_time').val();
      listener_val = $('#'+comp_div_id+' .listener_value').val();
      if (listener_val == "x") { listener_val = 'off'; }
      comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false

      if ((($.now() - listener_time) > 6000) && (comp_val != level_to_truefalse(listener_val))) { // no change at all and val still not same as listener, so set the card back to the listener val
        console.log('setting slider to: '+listener_val);
        $('#'+comp_div_id+' .listener_value').val(listener_val); // update the switch by faking a change on listener. need to do it this way so it wont fire any event.
        $('#'+comp_div_id+' .listener_value').trigger('change');
      }
      else {
        //console.log("something happened");
      }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_value_changed(comp_div_id, comp_command, state_key, comp_val, wgt_id) {

        $('#'+comp_div_id+'_label').html(comp_val+'%');
        if (comp_val == 0) { $('#'+comp_div_id+'_icon').removeClass('is-active'); }
        else { $('#'+comp_div_id+'_icon').addClass('is-active'); }

        listener_val = $('#'+comp_div_id+' .listener_value').val();
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val();

        if ((comp_val != listener_val) && // fire action if its different
            (comp_val != val_by_listener)) { // and it was a user action

            //console.log('comp_val='+comp_val);
            //console.log('listener_val='+listener_val);
            //console.log('val_by_listener='+val_by_listener);

            // fire the action and reset the last set by listener
            console.log('card command: '+comp_command+' --> card value/s: '+comp_val);
            var surl = '/api/core/run_command/?cmd='+comp_command+'&set_key='+state_key+'&set_val='+comp_val+'&wgt='+wgt_id+'&z='+get_rand_ext();
            $.get(surl, function(data, status){
                //console.log(surl);
            });
            $('#'+comp_div_id+' .value_by_listener').val('x');

            setTimeout(function() {
                check_socket_active();
            },2000 ); // send a ping or two to ensure the websocket it working if nothing is moving on its own within 2 secs

            setTimeout(function() {
                slider_check_action_fired(comp_div_id);
            },6000 ); // worry if 6s after firing the action nothing actually happened

        }

        updated_time_elem = $('#'+comp_div_id+' .updated_time');
        updated_time_elem.val($.now()); // update the timestamp regardless of user or listener related change
        updated_time_elem.trigger('change');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function switch_value_changed(comp_div_id, comp_command, state_key, comp_val, wgt_id) {

      if (comp_val == false) {
          label_val = 'OFF';
          $('#'+comp_div_id+'_icon').removeClass('is-active');
      }
      else { 
          label_val = 'ON';
          $('#'+comp_div_id+'_icon').addClass('is-active');
      }
      $('#'+comp_div_id+'_label').html(label_val);

      listener_val = $('#'+comp_div_id+' .listener_value').val();
      listener_time = $('#'+comp_div_id+' .listener_time').val();
      val_by_listener = $('#'+comp_div_id+' .value_by_listener').val();

      if ((comp_val != level_to_truefalse(listener_val)) && // fire action if its different
          (comp_val != val_by_listener)) { // and it was a user action
          // fire the action and reset the last set by listener
          console.log('card command: '+comp_command+' --> card value/s: '+truefalse_to_level(comp_val));
          var surl = '/api/core/run_command/?cmd='+comp_command+'&set_key='+state_key+'&set_val='+truefalse_to_level(comp_val)+'&wgt='+wgt_id+'&z='+get_rand_ext();
          $.get(surl, function(data, status){
          });
          $('#'+comp_div_id+' .value_by_listener').val('x');

          setTimeout(function() {
              switch_check_action_fired(comp_div_id);
          },6000 ); // worry if 6s after firing the action nothing actually happened
      }

      updated_time_elem = $('#'+comp_div_id+' .updated_time');
      updated_time_elem.val($.now()); // update the timestamp regardless of user or listener related change
      updated_time_elem.trigger('change');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function listener_val_changed(comp_div_id) {

      listener_val = $('#'+comp_div_id+' .listener_value').val();
      $('#'+comp_div_id+'_listener_label').html(listener_val);

      listener_time_elem = $('#'+comp_div_id+' .listener_time');
      listener_time_elem.val($.now());
      listener_time_elem.trigger('change');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_listener_time_changed(comp_div_id) {

        listener_val = $('#'+comp_div_id+' .listener_value').val();
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        updated_time = $('#'+comp_div_id+' .updated_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val();
        comp_val = $('#'+comp_div_id+'_main').val();

        // if the card was not updated for over 6sec
        // or if the card val was last set by the listener - still safe to update
        // but dont bother if its already the same
        if (((listener_time - updated_time > 6000) || (comp_val == val_by_listener))     
          && (listener_val != comp_val)) {

            $('#'+comp_div_id+' .value_by_listener').val(listener_val);
            $('#'+comp_div_id+' .value_by_listener').trigger('change');

            // update the actual card itself
            $('#'+comp_div_id+'_main')[0].MaterialSlider.change(listener_val);
            $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
        }

        if (listener_val != comp_val) { // ie if listener and card are different for any reason at this point try again soon
            setTimeout(function() {
                listener_time_elem = $('#'+comp_div_id+' .listener_time');
                listener_time_elem.val($.now());
                listener_time_elem.trigger('change');
            },250 ); // worry abt difference until it is the same by faking a chg in 250ms
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function switch_listener_time_changed(comp_div_id) {       

        listener_val = $('#'+comp_div_id+' .listener_value').val(); // on or off
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        updated_time = $('#'+comp_div_id+' .updated_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val(); // logical true or false

        comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false

        // if the card was not updated for over 6sec
        // or if the card val was last set by the listener - still safe to update
        // but dont bother if its already the same
        if (((listener_time - updated_time > 6000) || (comp_val == txt_to_logical(val_by_listener))) 
          && (level_to_truefalse(listener_val) != comp_val))  {

            val_by_listener_elem = $('#'+comp_div_id+' .value_by_listener');
            val_by_listener_elem.val(level_to_truefalse(listener_val));
            val_by_listener_elem.trigger('change');

            // update the actual card itself

            if (level_to_truefalse(listener_val) == true) {  $('#'+comp_div_id+'_l')[0].MaterialSwitch.on(); }
            else {  $('#'+comp_div_id+'_l')[0].MaterialSwitch.off(); }
            $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this

        }

        if (level_to_truefalse(listener_val) != comp_val) { // ie if listener and card are different for any reason at this point try again soon
            setTimeout(function() {
                listener_time_elem = $('#'+comp_div_id+' .listener_time');
                listener_time_elem.val($.now());
                listener_time_elem.trigger('change');
            },250 ); // worry abt difference until it is the same by faking a chg in 250ms
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_adjust(wgt_id, comp_div_id, set_to) {

      comp_val = $('#'+comp_div_id+'_main').val();
      if (set_to == "toggle") {
        if (comp_val == 0) { new_val = 'on'; }
        else { new_val = 'off'; }
        console.log('card command: set_power --> card value/s: '+new_val);
        var surl = '/api/core/run_command/?cmd=set_card_val&set_key=power&set_val='+new_val+'&wgt='+wgt_id+'&z='+get_rand_ext();
        $.get(surl, function(data, status){
            //console.log(surl);
        });
      }
      else {
        if ((set_to == "plus") && (comp_val < 100)) { new_val = parseInt(comp_val)+1; }
        else if ((set_to == "minus") && (comp_val > 0)) { new_val = parseInt(comp_val)-1; }
        else { new_val = parseInt(set_to); }

        // now update the slider
        $('#'+comp_div_id+'_main')[0].MaterialSlider.change(new_val);
        $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
      }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    //function adjust_switch(component_div_id,set_to) {
    function switch_adjust(comp_div_id,set_to) {

      comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false
      new_val = comp_val;

      if ((set_to == "toggle") && (comp_val == false)) {
        $('#'+comp_div_id+'_l')[0].MaterialSwitch.on();
        $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
      }
      else if ((set_to == "toggle") && (comp_val == true)) {
        $('#'+comp_div_id+'_l')[0].MaterialSwitch.off();
        $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
      }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function toggle_faves(component_div_id) {
        if ($('#'+component_div_id+'_faves').hasClass("is-active")) {
            $('#'+component_div_id+'_faves').removeClass("is-active");
        }
        else {
            $('#'+component_div_id+'_faves').addClass("is-active");
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function level_to_truefalse(level) {
        output = false;
        if (level.toLowerCase() == 'on') { output = true; }
        return output;
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function truefalse_to_level(truefalse) {
        output = 'off';
        if (truefalse == true) { output = 'on'; }
        return output;
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function txt_to_logical(truefalse) {
        output = null;
        if (truefalse == "true") { output = true; }
        if (truefalse == "false") { output = false; }
        return output;
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function generate_layout() {
      layout =  '<div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">';
      layout += '  <header class="mdl-layout__header mdl-color-text--white">';
      layout += '    <div class="mdl-layout__header-row">';
      layout += '      <span class="mdl-layout-title">&lt; crave control &gt;</span>';
      layout += '      <div class="mdl-layout-spacer"></div>';
      layout += '      <div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable">';
      layout += '        <label class="mdl-button mdl-js-button mdl-button--icon" for="search">';
      layout += '          <i class="material-icons">search</i>';
      layout += '        </label>';
      layout += '        <div class="mdl-textfield__expandable-holder">';
      layout += '          <input class="mdl-textfield__input" type="text" id="search">';
      layout += '          <label class="mdl-textfield__label" for="search">Enter your query...</label>';
      layout += '        </div>';
      layout += '      </div>';
      layout += '      <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn">';
      layout += '        <i class="material-icons">more_vert</i>';
      layout += '      </button>';
      layout += '      <ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn">';
      layout += '        <li class="mdl-menu__item">About</li>';
      layout += '        <li class="mdl-menu__item">Contact</li>';
      layout += '        <li class="mdl-menu__item">Legal information</li>';
      layout += '      </ul>';
      layout += '    </div>';
      layout += '    <div class="mdl-layout__tab-bar mdl-js-ripple-effect" id="top-list"></div>';
      layout += '  </header>';
      layout += '  <main class="mdl-layout__content">';
      layout += '    <div class="leftside">';
      layout += '      <ul class="mdl-list" id="left-list"></ul>';
      layout += '    </div>';
      layout += '    <div class="rightside" id="card-elems">';
      layout += '    </div>';
      layout += '  </main>';
      layout += '</div>';
      $('body').html(layout);
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function generate_comps(cards_conf) {
      // generate the sections
      sections = {};
      $.each(cards_conf, function(key1,val1) {
        $.each(val1['groups'], function(key2,val2) {
          if (!(val2 in sections)) { sections[val2] = []; }
          sections[val2].push(key1);
        });
      });

      // generate the groups
      groups = Object.keys(sections);

      // generate left group tabs
      left_groups = ''
      $.each(groups, function(key,val) {
        if (key == 0) { actv = ' is-active'; }
        else { actv = ''; }
        left_groups += '<li class="mdl-list__item">\n';
        left_groups += '<button name="t' + key + '" class="leftnav mdl-button mdl-js-button mdl-js-ripple-effect' + actv + '">' + val + '</button>\n';
        left_groups += '</li>\n';
      });
      $('#left-list').html(left_groups);

      // generate top group tabs
      top_groups = ''
      $.each(groups, function(key,val) {
        if (key == 0) { actv = ' is-active'; }
        else { actv = ''; }
        top_groups += '<a name="t' + key + '" href="#scroll-tab-' + key + '" class="topnav mdl-layout__tab' + actv + '"><div class="navtext">' + val + '</div></a>\n';
      });
      $('#top-list').html(top_groups);

      // generate the pages with cards
      elems = '';
      page_num = 0;
      $.each(sections, function(key1,val1) {
        if (page_num == 0) { actv = 'is-active'; }
        else { actv = ''; }
        elems += '<section class="mdl-layout__tab-panel ' + actv + '" id="scroll-tab-' + page_num + '">';
        elems += '  <div class="mdl-grid">';

        // generate cards in group
        $.each(val1, function(key2,val2) {
          w_conf = cards_conf[val2];
          w_conf['page_num'] = page_num
          w_conf['item_num'] = key2
          w_conf['card_id'] = val2
          elems += cards[w_conf['card']](w_conf);
        });

        elems += '  </div>\n';
        elems += '</section>\n\n';
        page_num++;
      });
      $('#card-elems').html(elems);
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function safe_class(str) {
      return str.replace('.', '__');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////


