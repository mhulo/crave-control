
commands_conf = {
  "cmd0999" : {
    "description" : "test scene",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_9",
          "set_val": 80,
          "ramp_time": 4              
        }
      },
      {
        "method" : "core@DelayMs",
        "params" : {
          "device_id": "NET1_254_56_0",
          "time_ms": 3000            
        }
      },
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_9",
          "set_val": 20,
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0001" : {
    "description" : "dim master lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_0",
          "set_val": None,
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0002" : {
    "description" : "dim nia lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_3",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0003" : {
    "description" : "dim study lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_5",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0004" : {
    "description" : "dim dining lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_8",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0005" : {
    "description" : "dim lounge lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_9",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0006" : {
    "description" : "dim kitchen lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_15",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0007" : {
    "description" : "dim entrance lights",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_16",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0008" : {
    "description" : "dim downstairs",
    "actions" : [
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_8",
          "ramp_time": 4              
        }
      },
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_9",
          "ramp_time": 4              
        }
      },
      {
        "method" : "cgate@SetBrightness",
        "params" : {
          "device_id": "NET1_254_56_15",
          "ramp_time": 4              
        }
      }
    ]
  },
  "cmd0009" : {
    "description" : "ensuite fan",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_1"          
        }
      }
    ]
  },
  "cmd0023" : {
    "description" : "stairs led strip",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_6"          
        }
      }
    ]
  },
  "cmd0010" : {
    "description" : "wir light",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_7"          
        }
      }
    ]
  },
  "cmd0011" : {
    "description" : "ensuite ceiling heat",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_11"          
        }
      }
    ]
  },
  "cmd0012" : {
    "description" : "bathroom lights",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_12"          
        }
      }
    ]
  },
  "cmd0013" : {
    "description" : "ensuite floor heat",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_13"          
        }
      }
    ]
  },
  "cmd0015" : {
    "description" : "master led strip",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_17"          
        }
      }
    ]
  },
  "cmd0016" : {
    "description" : "bathroom fan",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_18"          
        }
      }
    ]
  },
  "cmd0017" : {
    "description" : "bathroom ceiling heat",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_21"          
        }
      }
    ]
  },
  "cmd0018" : {
    "description" : "bathroom floor heat",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_22"          
        }
      }
    ]
  },
  "cmd0019" : {
    "description" : "garage light",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_23"          
        }
      }
    ]
  },
  "cmd0020" : {
    "description" : "front door light",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_24"          
        }
      }
    ]
  },
  "cmd0021" : {
    "description" : "study lights toggle",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_5"          
        }
      }
    ]
  },
  "cmd0022" : {
    "description" : "ensuite lights",
    "actions" : [
      {
        "method" : "cgate@SetPower",
        "params" : {
          "device_id": "NET1_254_56_2"          
        }
      }
    ]
  },
  "cmd0023" : {
    "description" : "toggle stairs led strip",
    "actions" : [
      {
        "method" : "hue/hueController@levelToggle",
        "params" : {
          "device_id": "2"             
        }
      }
    ]
  },
  "cmd0024" : {
    "description" : "dim stairs led strip",
    "actions" : [
      {
        "method" : "hue/hueController@levelDim",
        "params" : {
          "device_id": "2"             
        }
      }
    ]
  },
  "cmd0025" : {
    "description" : "toggle bedroom led strip",
    "actions" : [
      {
        "method" : "hue/hueController@levelToggle",
        "params" : {
          "device_id": "3"             
        }
      }
    ]
  },
  "cmd0026" : {
    "description" : "dim bedroom led strip",
    "actions" : [
      {
        "method" : "hue/hueController@levelDim",
        "params" : {
          "device_id": "3"             
        }
      }
    ]
  }
}







