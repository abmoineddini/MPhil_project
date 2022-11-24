import serial.tools.list_ports
from PyQt5 import QtCore, QtGui, QtWidgets


## Finiding the Data collector and stage controller ports for Interface
def COMFinder(self):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:

        if "Arduino Uno" in p.description:
            StageControllerPort = p.name
        
        elif "Arduino Mega" in p.description:
            DataCollectorPort = p.name
        
    print("Stage Contoller port is : {}".format(StageControllerPort))
    print("Data Collector port is : {}".format(DataCollectorPort))
    try:
        self.StageCOMIndecatorLabel.setText(StageControllerPort)
        self.DCCOMIndecatorLabel.setText(DataCollectorPort)
    except Exception as e:
        print(e)

    return StageControllerPort, DataCollectorPort

