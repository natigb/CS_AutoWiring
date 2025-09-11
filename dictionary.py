
dataloggers = { 
      "img/cr1000x.png": {
        "model": "CR1000Xe",
        "connection": 
            {
            "power": ["12V+", "Ground", "GND-"],
            "interfaces": 
                ["MicroSD", "Ethernet", "RS232", "CSIO", "USB"],
            "ports": 
                ["H_1", "L_1", "GND_1", "H_2","L_2", "GND_2","VX_1","VX_2", "GND_3", "H_3", "L_3", "GND_4", "H_4", "L_4", "GND_5","P_1", "GND_6", "P_2",
                "H_5", "L_5", "GND_7","H_6", "L_6", "GND_8","VX_3","VX_4", "GND_9", "H_7", "L_7", "GND_10","H_8", "L_8", "GND_11",
                "5V_1", "G_1", "SW_1","SW_2", "12V_1", "G_2","C_1","C_2","C_3", "C_4","G_3","C_5","C_6", "RG_1", "C_7", "C_8","RG_2", "G_4"]
            }
        },
        "img/cr350.png": {
        "model": "CR350-WIFI",
        "connection": 
            {
            "power": ["Bat-", "Bat+", "CHG-", "CHG+", "Ground"],
            "interfaces": 
                ["WIFI", "Antenna", "RS232", "USB"],
            "ports": 
                ["12V_1", "G_1", "C_1", "12V_2", "G_2", "C_2", "SW_1", "G", "TX_2", "RX_2","RG_1", "SW_2", "G_4", "TX_3", "RX_3", "PLL_1", "PSW", "GND_1", "VX_1", "H_1", "L_1", "GND_2", "VX_2", "H_2", "L_2", "GND_3" ]
            }
        },
        "img/cr300/cr310.png": {
        "model": "CR310",
        "connection": 
            {
            "power": ["Bat-", "Bat+", "CHG-", "CHG+", "Ground"],
            "interfaces": 
                ["Ethernet", "RS232", "USB"],
            "ports": 
                ["VX_1", "G_1", "VX_2", "G_2", "PSW_1", "G_3", "C_1", "G_4", "C_2", "G_5", "SW_12", "G_6",
                 "GND_1", "PLL_1", "GND_2", "L_3", "H_3", "GND_3", "L_2", "H_2", "GND_4", "L_1", "H_1", "GND_5"]
                }
        },
        "img/cr6.png": {
        "model": "CR6",
        "connection": 
            {
            "power": ["Bat-", "Bat+", "CHG-", "CHG+", "Ground"],
            "interfaces": 
                ["Ethernet", "RS232", "USB", "MicroSD", "CSIO"],
            "ports": 
                ["U_1", "U_2", "GND_1", "U_3", "U_4", "GND_2", "U_5", "U_6", "GND_3", "U_7", "U_8", "GND_4", "U_9", "U_10", "GND_5", "U_11", "U_12", "GND_6",
                 "G_1", "SW_1", "SW_2", "G_2", "12V", "G_3", "C_1", "C_2", "C_3", "C_4", "RG_1", "G_4"]
                }
        }
    }
  
sensors2 = {

    "05103": {
    "name": "WS_WD",
    "measurement" : "wind",
    "model": "05103",
    "type": "analog",
    "connection":
    {
    "SDI-12": [("Red", "U", "P", "PLL"), 
                ("Black", "GND"), 
                ("Green", "U", "H", "L"),
                ("Blue", "U", "EX", "VX"), 
                ("White", "GND"), 
                ("Clear", "GND")]
        }
    },
    "TempVue20": {
    "name": "Pt100 Digital Air Temperature Sensor",
    "measurement" : "temperature",
    "model": "TempVue20",
    "type": "digital",
    "connection": 
    {
        "SDI-12": [("White", "C", "H", "L", "U"), 
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
    "TempVue10": {
    "name": "Pt100 Analog Temperature Sensor",
    "measurement" : "temperature",
    "model": "TempVue10",
    "type": "digital",
    "connection": 
    {
        "4-wire": [("Yellow", "H", "U"),
                    ("Blue", "L", "U"),
                    ("Orange", "H", "U"),
                    ("Purple", "H", "L"),
                    ("Brown", "VX", "EX", "U"),
                    ("Black", "GND"),
                    ("Clear", "GND")

                ],
        "2-wire": [("Orange", "SE", "U"), 
                ("Brown", "VX", "EX", "U"),
                ("Black", "GND"),
                ("Clear", "GND")  
                ]
    
        }
    },
    "109/108/107": {
    "name": "10X Temperature Probe",
    "measurement" : "temperature",
    "model": "109",
    "type": "digital",
    "connection": 
    {
        "Default": [("Black", "VX", "EX", "U"),
                    ("Red", "U", "H", "L"),
                    ("Purple", "GND"),
                    ("Clear", "GND")
                    

                ]
    
        }
    },
    "HygroVue10": {
    "name": "Digital Temperature an Relative Humidity Sensor",
    "measurement" : "temperature",
    "model": "HygroVue10",
    "type": "digital",
    "connection": 
    {
        "SDI-12": [("Brown", "12V"),
                    ("White", "U", "C"),
                    ("Black", "G"),
                    ("Clear", "G")
                ]
    
        }
    },
    "HygroVue5": {
    "name": "Digital Temperature an Relative Humidity Sensor",
    "measurement" : "temperature",
    "model": "HygroVue5",
    "type": "digital",
    "connection": 
    {
        "SDI-12": [("Brown", "12V"),
                    ("White", "U", "C"),
                    ("Black", "G"),
                    ("Clear", "G")
                ]
    
        }
    },
    "EE181-L": {
    "name": "Air Temperature an Relative Humidity Sensor",
    "measurement" : "temperature",
    "model": "EE181-L",
    "type": "analog",
    "connection": 
    {
        "SE-Measurment": [("Yellow", "U", "H", "L"),
                    ("Blue", "U", "H", "L"),
                    ("Black", "GND"),
                    ("Clear", "GND"),
                    ("Red", "12V", "SW")
                ]
    
        }
    },
    "ClimaVue50 G2": {
    "name": "Compact Digital Weather Sensor",
    "measurement" : "basic weather",
    "model": "ClimaVue50 G2",
    "type": "digital",
    "connection": 
    {
        "Modbus": [("White", "U", "C"),
                    ("Clear", "G"),
                    ("Brown", "12V"),
                    ("Black", "G")
                ]
    
        }
    },
    "ClimaVue40": {
    "name": "Compact Digital Weather Sensor",
    "measurement" : "basic weather",
    "model": "ClimaVue40",
    "type": "digital",
    "connection": 
    {
        "RS-485": [("Red", "12V"),
                    ("Black", "G"),
                    ("Green", "C_o"),
                    ("White", "C_e"),
                    ("Clear", "G")
                ]
    
        }
    },
    "MetSENS": {
    "name": "Compact Weather Sensor",
    "measurement" : "basic weather",
    "model": "MetSENS",
    "type": "digital",
    "connection": 
    {
        "RS-485": [("Red", "12V"),
                    ("Black", "G"),
                    ("Green", "C_o"),
                    ("White", "C_e"),
                    ("Clear", "G")
                ],
        "SDI-12": [("Green", "C", "U"),
                    ("Red", "12V"),
                    ("Black", "G"),
                    ("Clear", "G")
                ],
        "RS-232": [("Green", "C_o"),
                    ("White", "C_e"),
                    ("Red", "12V"),
                    ("Black", "G"),
                    ("Clear", "G")
                ],
    
        }
    },
    "CS100": {
    "name": "Barometric Pressure Sensor",
    "measurement" : "barometric pressure",
    "model": "CS100",
    "type": "analog",
    "connection": 
    {
        "SE-Measurement": [
            ("Blue", "U", "H", "L"), 
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
    "BaroVue10": {
    "name": "Barometric Pressure Sensor",
    "measurement" : "barometric pressure",
    "model": "CS100",
    "type": "digital",
    "connection": 
    {
        "SDI-12": [
            ("White", "C", "SDI12", "U"), 
            ("Red", "12V", "Bat+"),  
            ("Black", "G"),
            ("Blue", "Not"), 
            ("Yellow", "Not")],
        "RS-232": [
            ("Yellow", "C_o"), 
            ("Blue", "C_e"),  
            ("Black", "G"),
            ("Red", "12V", "Bat+"), 
            ("White", "Not")]
    
        }
    },
    
    "RainVue-Series": {
    "name": "Rain-Vue Series: SDI-12 Precipitation Sensors",
    "measurement" : "rain",
    "model": "RainVue",
    "type": "digital",
    "connection": 
    {
        "SDI-12": [
            ("White", "C", "U"), 
            ("Clear", "G"),  
            ("Brown", "12V"),
            ("Black", "G")]
        
    }
    },

    "TE525": {
    "name": "Tipping Bucket Rain Gage",
    "measurement" : "rain",
    "model": "TE525",
    "type": "digital",
    "connection": 
    {
        "Pulse": [
                ("Black", "P", "U"), 
                ("White", "GND"),  
                ("Clear", "GND")]
    }
    },
    "CS700": {
    "name": "Tipping Bucket Rain Gage",
    "measurement" : "rain",
    "model": "CS700",
    "type": "digital",
    "connection": 
    {
        "Pulse": [
                ("Black", "P","P_SW", "U"), 
                ("White", "GND"),  
                ("Clear", "GND")],
        "Control": [
                ("Black", "C", "U"), 
                ("White", "5V"),  
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
    },

    "03002": {
        "name": "Wind Sentry Set",
        "measurement": "wind",
        "model": "03002-L",
        "type": "analog",
        "connection": {
            "Default": [
                ("Red", "U", "P", "PLL"),
                ("Black", "GND"),
                ("Green", "U", "H", "L"),
                ("Blue", "U", "EX", "VX"),
                ("White", "GND"),
                ("Clear", "GND"),
            ],
        }
    },
    "Modbus": {
        "name": "Modbus",
        "measurement": "control",
        "model": "Modbus",
        "type": "digital",
        "connection": {
            "COMC1": [
                ("A", "TX"),
                ("B", "RX"),
            ],
        }
    },
    "CH201": {
        "name": "CH201 12V Charging Regulator",
        "measurement": "battery",
        "model": "CH201",
        "type": "power",
        "connection": {
            "RS-232": [
                ("Black", "GND-"),
                ("Red", "12V+"),
                ("TX", "-"),
                ("RX", "-"),
                ("COM G", "-"),
                ("DC In1", "-"),
                ("DC In2", "-"),
                ("g", "-"),
                ("g", "-"),
                ("12V", "-"),
            ],
        }
    },
    "SP10": {
        "name": "Solar Panel SP10",
        "measurement": "battery",
        "model": "SP10",
        "type": "power",
        "connection": {
            "Default": [
                ("Red", "+"),
                ("Black", "-"),
            ],
        }
    },
    "BP7": {
        "name": "7 Ah 12 V Sealed Rechargeable Battery",
        "measurement": "battery",
        "model": "BP7",
        "type": "power",
        "connection": {
            "Default": [
                ("Red", "+"),
                ("Black", "-"),
            ],
        }
    },  
    "CH150": {
        "name": "Charging regulator CH150",
        "measurement": "battery",
        "model": "CH150",
        "type": "power",
        "connection": {
            "Default": [
                ("Red", "12+"),
                ("Black", "GND-"),
                ("G", "-Port 1-"),
                ("CHG", "-Port 1-"),
                ("CHG", "-Port 1-"),
                ("G", "-Port 1-"),
                ("Solar", "-Port 1-"),
            ],
        }
    },
    "Generic Regulator": {
        "name": "Generic Regulator",
        "measurement": "battery",
        "model": "Generic Regulator",
        "type": "power",
        "connection": {
            "Default": [
                ("Red", "12V+"),
                ("Black", "GND-"),
                ("Battery", "Battery"),
                ("Solar Panel", "Solar Panel"),
            ],
        }
    },
}


