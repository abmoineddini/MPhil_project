import serial.tools.list_ports
from PyQt5 import QtCore, QtGui, QtWidgets


## Finiding the Data collector and stage controller ports for Interface
def COMFinder(self):
    ports = list(serial.tools.list_ports.comports())
    StageControllerPort = ''
    DataCollectorPort = ''
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

## Initializing arduino
def Inititialise(comPort):
    arduino = serial.Serial(comPort, 9600, timeout=1)
    line = arduino.readline()
    print(line)
    try:
        string = line.decode()
    except:
        print("ignored")
    else:
        numS = string.replace("\r\n", '')

        while numS != "ready":
            line = arduino.readline()
            line = line.decode()
            numS = line.replace("\r\n", '')
        while line != "Starting":
            arduino.write(b"rdy")
            line = arduino.readline()
            line = line.decode()
            line = line.replace("\r\n", '')

        print("Starting")
    return 0, arduino

## Homming Sequence
def Calibrate(comPort, arduino):
    ### 
    # The motor controller is setup so that if you 
    # connect to arduino it will run the calibration sequence
    ###
    arduino = serial.Serial(comPort, 9600, timeout=1)
    line = arduino.readline()
    print(line)
    try:
        string = line.decode()
    except:
        print("ignored")
    else:
        numS = string.replace("\r\n", '')

        while numS != "ready":
            line = arduino.readline()
            line = line.decode()
            numS = line.replace("\r\n", '')
        while line != "Starting":
            arduino.write(b"rdy")
            line = arduino.readline()
            line = line.decode()
            line = line.replace("\r\n", '')

        print("Starting")
    return 0, arduino

## Set Angles
def AngleSet(angle, arduino, currAngle):
    if angle==0:
        if currAngle>180:
            angle = 360
        else:
            angle = -360
    angle = str(angle)
    arduino.write(angle.encode())
    line = arduino.readline()
    line = line.decode()
    line = line.replace("\r\n", '')
    while line!="done":
        line = arduino.readline()
        print(line)
        line = line.decode()
        line = line.replace("\r\n", '')

    while not line.isdigit():
        line = arduino.readline()
        print(line)
        line = line.decode()
        line = line.replace("\r\n", '')
    currAng = int(line)
    print("Speaker is at ", currAng, " Degrees now")
    return currAng
    
# ## Enabling and Disabling Window
# def Enable_Disable_Window(s, Condition):
#     if Condition:
#         print("Window Enabled")
#         self.centralwidget.setEnabled(True)
#     else:
#         print("Window Disables")
#         self.centralwidget.setEnabled(False)