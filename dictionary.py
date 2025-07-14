
dataloggers = { 
      "CR100Xe": {
        "model": "CR1000Xe",
        "connection": 
            {
            "power": ["12V_0", "GND_0", "GND_-1"],
            "interfaces": 
                ["MicroSD", "Ethernet", "RS232", "CSIO", "USB"],
            "ports": 
                ["SE_1-H_1", "SE_2-L_1", "GND_1", "SE_3-H_2","SE_4-L_2", "GND_2","VX_1","VX_2", "GND_3", "SE_5-H_3", "SE_6-L_3", "GND_4", "SE_7-H_4", "SE_8-L_4", "GND_5","P_1", "GND_6", "P_2",
                "SE_9-H_5", "SE_10-L_5", "GND_7","SE_11-H_6", "SE_12-L_6", "GND_8","VX_3","VX_4", "GND_9", "SE_13-H_7", "SE_14-L_7", "GND_10","SE_15-H_8", "SE_16-L_8", "GND_11",
                "5V_1", "G_1", "SW_1","SW_2", "12V_1", "G_2","C_1","C_2","C_3", "C_4","G_3","C_5","C_6", "RG_1", "C_7", "C_8","RG_2", "G_4"]
            }
        }
    }
  
sensors = {
        "05103": {
        "name": "WS_WD",
        "measurement" : "wind",
        "model": "05103",
        "connection":
        {
        "SDI-12": [("Red", "U", "P", "PLL"), 
                    ("Black", "GND"), 
                    ("Green", "U", "SE"),
                    ("Blue", "U", "EX", "VX"), 
                    ("White", "GND"), 
                    ("Clear", "GND")]
            }
        },
        "TempVue20": {
        "name": "Pt100 Digital Air Temperature Sensor",
        "measurement" : "temperature",
        "model": "TempVue20",
        "connection": 
        {
            "SDI-12": [("White", "C", "SDI12", "U"), 
                    ("Brown", "12V"),  
                    ("Black", "GND"),
                    ("Clear", "GND"), 
                    ("Gray", "GND")]
        
            }
        },
        "CS100": {
        "name": "Barometric Pressure Sensor",
        "measurement" : "baro_pressure",
        "model": "CS100",
        "connection": 
        {
            "SE-Measurement": [
                    ("Blue", "U", "SE"), 
                    ("Yellow", "GND"),  
                    ("Black", "GND"),
                    ("Green", "U", "C"), 
                    ("Red", "12V"), 
                    ("Shield", "GND")],
            "Diff-Measurement": [
                ("Blue", "U", "DiffH"), 
                ("Yellow", "U", "DiffL"),  
                ("Black", "GND"),
                ("Green", "U", "C"), 
                ("Red", "12V"), 
                ("Shield", "GND")]
        
            }
        },

        "TE525": {
        "name": "Tipping Bucket Rain Gage",
        "measurement" : "rain",
        "model": "TE525",
        "connection": 
        {
            "Pulse": [
                    ("Black", "P", "U"), 
                    ("White", "GND"),  
                    ("Clear", "GND")]
        }
        }
    }



