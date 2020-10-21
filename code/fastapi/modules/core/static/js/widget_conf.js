
//Copyright (c) 2011, mhulo @ Crave-Technology Inc. All rights reserved.
//Code licensed under the GNU license http://www.gnu.org/licenses/gpl.html
//version: 2011-06-25
//www.cravetechnology.com.au

widgets_conf = {
  "w0001" : {
    "ui_type" : "dimmer_1",
    "name" : "Master Bedroom Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_0",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_1",
    "groups" : ["Lights", "Upstairs"]
  },
  "w0002" : {
    "ui_type" : "dimmer_1",
    "name" : "Nia's Bedroom Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_3",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_2",
    "groups" : ["Lights", "Upstairs"]
  },
  "w0003" : {
    "ui_type" : "dimmer_1",
    "name" : "Study Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_5",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_3",
    "groups" : ["Lights"]
  }
};

  rest_of_widgets = {
  "w0101" : {
    "ui_type" : "switch_1",
    "name" : "Master LED Strip",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_17",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_15",
    "groups" : ["Lights", "Upstairs"]
  },
    "w0102" : {
    "ui_type" : "switch_1",
    "name" : "Ensuite Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_2",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_22",
    "groups" : ["Lights", "Upstairs"]
  },
    "w0103" : {
    "ui_type" : "switch_1",
    "name" : "Ensuite Fan",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_1",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_9",
    "groups" : ["Devices", "Upstairs"]
  },
    "w0104" : {
    "ui_type" : "switch_1",
    "name" : "Ensuite Ceiling Heat",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_11",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_11",
    "groups" : ["Devices", "Upstairs"]
  },
  "w0105" : {
    "ui_type" : "switch_1",
    "name" : "Stairs LED Strip",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_6",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_23",
    "groups" : ["Lights", "Upstairs"]
  },
  "w0004" : {
    "ui_type" : "dimmer_1",
    "name" : "Dining Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_8",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_4",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0005" : {
    "ui_type" : "dimmer_1",
    "name" : "Lounge Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_9",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_5",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0006" : {
    "ui_type" : "dimmer_1",
    "name" : "Kitchen Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_15",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_6",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0007" : {
    "ui_type" : "dimmer_1",
    "name" : "Entrance Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_16",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "15",
    "fave_percentage_2" : "40",
    "command" : "command_14",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0008" : {
    "ui_type" : "dimmer_1",
    "name" : "Dim Downstairs",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_8",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "20",
    "fave_percentage_2" : "50",
    "command" : "command_8",
    "groups" : ["Lights","Scenes","Downstairs"]
  },
  "w0009" : {
    "ui_type" : "switch_1",
    "name" : "Bathroom Lights",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_12",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_12",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0010" : {
    "ui_type" : "switch_1",
    "name" : "Bathroom Fan",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_18",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_16",
    "groups" : ["Devices", "Downstairs"]
  },
  "w0011" : {
    "ui_type" : "switch_1",
    "name" : "Bathroom Ceiling Heat",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_21",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_17",
    "groups" : ["Devices", "Downstairs"]
  },
  "w0012" : {
    "ui_type" : "switch_1",
    "name" : "Front Door Light",
    "listener_interface" : "cgate",
    "listener_device_id" : "NET1_254_56_24",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_20",
    "groups" : ["Lights", "Downstairs"]
  },
  "w0013" : {
    "ui_type" : "switch_1",
    "name" : "Stairs LED Strip",
    "listener_interface" : "hue",
    "listener_device_id" : "2",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_23",
    "groups" : ["Lights","Hue"]
  },
  "w0014" : {
    "ui_type" : "dimmer_1",
    "name" : "Stairs LED Strip",
    "listener_interface" : "hue",
    "listener_device_id" : "2",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "20",
    "fave_percentage_2" : "50",
    "command" : "command_24",
    "groups" : ["Lights","Hue"]
  },
  "w0015" : {
    "ui_type" : "switch_1",
    "name" : "Bedroom LED Strip",
    "listener_interface" : "hue",
    "listener_device_id" : "3",
    "listener_state_key" : "level",
    "ui_style" : "",
    "command" : "command_25",
    "groups" : ["Lights","Hue"]
  },
  "w0016" : {
    "ui_type" : "dimmer_1",
    "name" : "Bedroom LED Strip",
    "listener_interface" : "hue",
    "listener_device_id" : "3",
    "listener_state_key" : "level",
    "ui_style" : "",
    "fave_percentage_1" : "20",
    "fave_percentage_2" : "50",
    "command" : "command_26",
    "groups" : ["Lights","Hue"]
  }
};

