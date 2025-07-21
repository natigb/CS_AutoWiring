
dataloggers = { 
      "CR100Xe": {
        "model": "CR1000Xe",
        "connection": 
            {
            "power": ["12V_0", "GND_0", "GND_-1"],
            "interfaces": 
                ["MicroSD", "Ethernet", "RS232", "CSIO", "USB"],
            "ports": 
                ["H_1", "L_1", "GND_1", "H_2","L_2", "GND_2","VX_1","VX_2", "GND_3", "H_3", "L_3", "GND_4", "H_4", "L_4", "GND_5","P_1", "GND_6", "P_2",
                "H_5", "L_5", "GND_7","H_6", "L_6", "GND_8","VX_3","VX_4", "GND_9", "H_7", "L_7", "GND_10","H_8", "L_8", "GND_11",
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
                    ("Black", "G"),
                    ("Clear", "G"), 
                    ("Gray", "G")],
            "RS-485": [("Yellow", "C"), 
                    ("Blue", "C"),  
                    ("Brown", "12V"),
                    ("Black", "G"), 
                    ("Gray", "G"), 
                    ("Clear", "GND")]
        
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
                ("Black", "G"),
                ("Green", "U", "C"), 
                ("Red", "12V"), 
                ("Shield", "GND")],
            "Diff-Measurement": [
                ("Blue", "U", "H"), 
                ("Yellow", "U", "L"),  
                ("Black", "G"),
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
        },

        "CS616": {
        "name": "30 cm Water Content Reflectometer",
        "measurement" : "soil",
        "model": "CS616",
        "connection": 
        {
            "Default": [
                    ("Red", "12V"), 
                    ("Green", "H", "L", "U"),  
                    ("Orange", "C"),  
                    ("Black", "GND"),  
                    ("Clear", "G")]
        }
        }

    }



