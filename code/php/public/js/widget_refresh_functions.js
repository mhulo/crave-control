
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au

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
    function spawn_listener_interfaces() {        

        // this is where it spawns a listener for each interface needed
        // based on the interfaces that the widgets on the page need

        $.each(listner_addresses_arr, function(i,field) {
            console.log(field+' interface spawned');
            get_live_status(field);
        });
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function get_live_status(interface) {        

        // get a refreshed set of values for the given interface

        //create a new websocket object.
        socket_uri = "ws://"+ws_host_addr+":"+ws_host_ports[interface]+"/code/modules/interfaces/"+interface+"/"+interface+"Daemon.php?"; 
        ws_sockets[interface] = new WebSocket(socket_uri);

        ws_sockets[interface].onopen = function(ev) { // connection is open 
            console.log('socket connected to '+interface+' interface');
        };

        // message received on websocket from server
        ws_sockets[interface].onmessage = function(ev){
            //console.log('got something');
            ws_last_msg_time[interface] = $.now(); // keep track of how recently anything was sent to this interface
            //console.log('last='+ws_last_msg_time[interface]);

            if (ev.data == 'pong') {
                console.log(interface+' '+ev.data+' received');
            }
            else {
                //console.log(interface+' '+ev.data);
                var result = JSON.parse(ev.data); // daemon via websocket sends json data
                $.each(result, function(i,field){
                    if (($('.'+i).length) && ($('.'+i).val() != field)) { // if the value exists and is different to the network
                        console.log(i+' updated to '+field);
                        $('.'+i).val(field); // update it
                        $('.'+i).trigger('change');
                    }
                });
            }
        };

        ws_sockets[interface].onerror   = function(ev){
            console.log('socket error on '+interface+' interface');
        };

        ws_sockets[interface].onclose   = function(ev){
            console.log('socket disconnected from '+interface+' interface');
            //try to reconnect in 5 seconds

            setTimeout(function(){
                if (ws_sockets[interface].readyState != 1) { // if something else hasn't triggered a re-connect already
                    console.log('waited 5 secs.. reconnecting to '+interface);
                    get_live_status(interface);
                }
            }, 5000);

        };
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////

    function check_socket_active(interface) {

        if (ws_sockets[interface].readyState == 1) {

            //console.log('got here');
            if ((($.now() - ws_last_msg_time[interface]) > 2000) && (($.now() - ws_last_msg_time[interface]) < 10000)) { // if update in the last 2 to 10 secs range, send a ping then go again
        
                ws_sockets[listener_interface].send('ping');
                console.log(listener_interface+' ping sent');

                setTimeout(function() {
                    check_socket_active(listener_interface);
                },2000 ); // go again in 2 secs
            }
            else if (($.now() - ws_last_msg_time[interface]) > 10000)  { // if update longer than 10 secs ago, reconnect
	
                ws_sockets[interface].close();
                get_live_status(interface);
            }
        }
        else if (ws_sockets[interface].readyState > 1) {
	        get_live_status(interface);
        }
    }

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_check_action_fired(comp_subtype,comp_div_id) {

        listener_time = $('#'+comp_div_id+' .listener_time').val();
        listener_val = $('#'+comp_div_id+' .listener_value').val();
        if (listener_val == "x") { listener_val = 0; }

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_main').val();
            break;
        }

        if ((($.now() - listener_time) > 6000) && (comp_val != listener_val)) { // no change at all and val still not same as listener, so set the widget back to the listener val
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
    function switch_check_action_fired(comp_subtype,comp_div_id) {

        listener_time = $('#'+comp_div_id+' .listener_time').val();
        listener_val = $('#'+comp_div_id+' .listener_value').val();
        if (listener_val == "x") { listener_val = 0; }

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false
            break;
        }

        if ((($.now() - listener_time) > 6000) && (comp_val != level_to_truefalse(listener_val))) { // no change at all and val still not same as listener, so set the widget back to the listener val
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
    function slider_value_changed(comp_val,comp_subtype,comp_div_id,widget_command,listener_interface) {

	//console.log('got here');

        $('#'+comp_div_id+'_label').html(comp_val+'%');
        if (comp_val == 0) { $('#'+comp_div_id+'_icon').removeClass('is-active'); }
        else { $('#'+comp_div_id+'_icon').addClass('is-active'); }

        listener_val = $('#'+comp_div_id+' .listener_value').val();
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val();

        if ((comp_val != listener_val) && // fire action if its different
            (comp_val != val_by_listener)) { // and it was a user action

            // fire the action and reset the last set by listener
            console.log('widget command: '+widget_command+' --> widget value/s: '+comp_val);
            var surl = '/api/command/run/?z='+get_rand_ext()+'&cmd='+widget_command+'&set_val='+comp_val;
            $.get(surl, function(data, status){
                //console.log(surl);
            });
            $('#'+comp_div_id+' .value_by_listener').val('x');

            setTimeout(function() {
                check_socket_active(listener_interface);
            },2000 ); // send a ping or two to ensure the websocket it working if nothing is moving on its own within 2 secs

            setTimeout(function() {
                slider_check_action_fired(comp_subtype,comp_div_id);
            },6000 ); // worry if 6s after firing the action nothing actually happened

        }

        updated_time_elem = $('#'+comp_div_id+' .updated_time');
        updated_time_elem.val($.now()); // update the timestamp regardless of user or listener related change
        updated_time_elem.trigger('change');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function switch_value_changed(comp_val,comp_subtype,comp_div_id,widget_command) {

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
            console.log('widget command: '+widget_command+' --> widget value/s: '+truefalse_to_level(comp_val));
            var surl = '/api/command/run/?z='+get_rand_ext()+'&cmd='+widget_command+'&set_val='+truefalse_to_level(comp_val);
            $.get(surl, function(data, status){
            });
            $('#'+comp_div_id+' .value_by_listener').val('x');

            setTimeout(function() {
                switch_check_action_fired(comp_subtype,comp_div_id);
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
        $('#'+comp_div_id+'_listener_label').html(listener_val+'%');

        listener_time_elem = $('#'+comp_div_id+' .listener_time');
        listener_time_elem.val($.now());
        listener_time_elem.trigger('change');
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_listener_time_changed(comp_subtype,comp_div_id) {

        listener_val = $('#'+comp_div_id+' .listener_value').val();
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        updated_time = $('#'+comp_div_id+' .updated_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val();

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_main').val();
            break;
        }

        // if the widget was not updated for over 6sec
        // or if the widget val was last set by the listener - still safe to update
        // but dont bother if its already the same
        if (((listener_time - updated_time > 6000) || (comp_val == val_by_listener))     
          && (listener_val != comp_val)) {

            $('#'+comp_div_id+' .value_by_listener').val(listener_val);
            $('#'+comp_div_id+' .value_by_listener').trigger('change');

            // update the actual widget itself
            switch (comp_subtype) {
                case 'mdl1':
                    $('#'+comp_div_id+'_main')[0].MaterialSlider.change(listener_val);
                    $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this

                    //comp_val_elem = document.getElementById(comp_div_elem+"_main");
                    //comp_val_elem.MaterialSlider.change(listener_val);
                    //comp_val_elem.trigger('change'); // the label wont update unless we trigger this
                break;
            }
        }

        if (listener_val != comp_val) { // ie if listener and widget are different for any reason at this point try again soon
            setTimeout(function() {
                listener_time_elem = $('#'+comp_div_id+' .listener_time');
                listener_time_elem.val($.now());
                listener_time_elem.trigger('change');
            },250 ); // worry abt difference until it is the same by faking a chg in 250ms
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function switch_listener_time_changed(comp_subtype,comp_div_id) {       

        listener_val = $('#'+comp_div_id+' .listener_value').val(); // number 0-100
        listener_time = $('#'+comp_div_id+' .listener_time').val();
        updated_time = $('#'+comp_div_id+' .updated_time').val();
        val_by_listener = $('#'+comp_div_id+' .value_by_listener').val(); // logical true or false

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false
            break;
        }

        // if the widget was not updated for over 6sec
        // or if the widget val was last set by the listener - still safe to update
        // but dont bother if its already the same
        if (((listener_time - updated_time > 6000) || (comp_val == txt_to_logical(val_by_listener))) 
          && (level_to_truefalse(listener_val) != comp_val))  {

            // update the widget value by listener
 //           $('#'+comp_div_id+' .value_by_listener').val(level_to_truefalse(listener_val));
 //           $('#'+comp_div_id+' .value_by_listener').trigger('change');

            val_by_listener_elem = $('#'+comp_div_id+' .value_by_listener');
            val_by_listener_elem.val(level_to_truefalse(listener_val));
            val_by_listener_elem.trigger('change');

            // update the actual widget itself
            switch (comp_subtype) {
                case 'mdl1':
                    if (level_to_truefalse(listener_val) == true) {  $('#'+comp_div_id+'_l')[0].MaterialSwitch.on(); }
                    else {  $('#'+comp_div_id+'_l')[0].MaterialSwitch.off(); }
                    $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
                break;
            }

        }

        if (level_to_truefalse(listener_val) != comp_val) { // ie if listener and widget are different for any reason at this point try again soon
            setTimeout(function() {
                listener_time_elem = $('#'+comp_div_id+' .listener_time');
                listener_time_elem.val($.now());
                listener_time_elem.trigger('change');
            },250 ); // worry abt difference until it is the same by faking a chg in 250ms
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function slider_adjust(comp_subtype,comp_div_id,set_to) {

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_main').val();
            break;
        }

        if ((set_to == "plus") && (comp_val < 100)) {
            new_val = parseInt(comp_val)+1;
        }
        else if ((set_to == "minus") && (comp_val > 0)) {
            new_val = parseInt(comp_val)-1;
        }
        else if ((set_to == "toggle") && (comp_val == 0)) {
            new_val = 100;
        }
        else if ((set_to == "toggle") && (comp_val > 0)) {
            new_val = 0;
        }
        else {
            new_val = parseInt(set_to);
        }

        // now update the slider
        switch (comp_subtype) {
            case 'mdl1':
                $('#'+comp_div_id+'_main')[0].MaterialSlider.change(new_val);
                $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
            break;
        }
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    //function adjust_switch(component_div_id,set_to) {
    function switch_adjust(comp_subtype,comp_div_id,set_to) {

        switch (comp_subtype) {
            case 'mdl1':
                comp_val = $('#'+comp_div_id+'_l').is('.is-checked'); // logical true or false
            break;
        }

        new_val = comp_val;

        switch (comp_subtype) {
            case 'mdl1':
                if ((set_to == "toggle") && (comp_val == false)) {
                    $('#'+comp_div_id+'_l')[0].MaterialSwitch.on();
                    $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
                }
                else if ((set_to == "toggle") && (comp_val == true)) {
                    $('#'+comp_div_id+'_l')[0].MaterialSwitch.off();
                    $('#'+comp_div_id+'_main').trigger('change'); // the label wont update unless we trigger this
                }
            break;
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
        if (level >0) { output = true; }
        return output;
    }
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
    function truefalse_to_level(truefalse) {
        output = 0;
        if (truefalse == true) { output = 100; }
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
