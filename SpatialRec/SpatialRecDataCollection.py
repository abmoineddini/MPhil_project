import utils
import DataManagement
import os
import time
import numpy as np
import serial
import pandas as pd
import random
import math
from SpatialRec import Spatial_Rec_utils
import subprocess
import IoTConnection



def DataCollection(DataCollectionCOM, StageControllerCOM, StageController, currAngle, NumSamples, NumChannels, Period, Increment, RotAngle, Direction, ExperimentName, ExperimentDIR):
    # Fining all the classes in the range of rotation
    print(Increment)
    if Direction == 1:
        Increments = np.linspace(0, RotAngle, int(RotAngle/Increment)+1)
    else:  
        Increments = np.linspace(360-RotAngle, 0, int(RotAngle/Increment)+1)
    print(Increments)
    progressMatrix = ""
    for i in Increments:
        progressMatrix += str(i) + ":" + "0 "
    
    print(progressMatrix)
    CompleteprogressMatrix = "0:0 " + progressMatrix
    IoTConnection.Data_Collection_Pub_IoT(ExperimentDIR, CompleteprogressMatrix)

    # Start the web base dashboard data monitoring
    dashStartCMD = "python SpatialRec/DashboardSpatialRecognition.py -d " + ExperimentDIR +"/RawData"
    DashBoardStart = subprocess.Popen(["start", "cmd", "/k", dashStartCMD], shell = True)
    
    totalSampleProcessed = 0
    InitalInspect = True
    for Angle in Increments:
        # Setting Angle
        if Angle != 0:
            currAngle = utils.AngleSet(Angle, StageController, currAngle)
            time.sleep(1)

        for Sample in range(NumSamples):
            # Finding Suitable name for the sample
            NameTest = True
            RawDataDIR = os.path.join(ExperimentDIR, "RawData")
            testNum = 1
            Files = [f for f in os.listdir(RawDataDIR) if os.path.isfile(os.path.join(RawDataDIR, f))]
            while NameTest:
                CSVName = str(Angle) + '-Test-'+ str(testNum) + '.csv'
                if CSVName in Files:
                    print("File Already exist, Trying another name.")
                    testNum = testNum+1
                else:
                    NameTest = False

            SampleName = os.path.join(RawDataDIR, CSVName)
            Spatial_Rec_utils.DataCollect(DataCollectionCOM, NumChannels, Period, SampleName)
            
            for i in range(len(progressMatrix.split(" "))):
                if progressMatrix.split(" ")[i].split(":")[0] == str(Angle):
                    progressMatrix.split(" ")[i].split(":")[1] = 100 * (Sample/NumSamples)

            try:
                currProgress = str(Angle) + ":" + str(100 * (Sample/NumSamples)) + " "
                CompleteprogressMatrix = currProgress + progressMatrix
                print(CompleteprogressMatrix)
                IoTConnection.Data_Collection_Pub_IoT(ExperimentDIR, progressMatrix)

            except:
                print("Connection busy will update in next run")

            totalSampleProcessed += 1

    if (totalSampleProcessed % (NumSamples*2)) == 0:
        totalSampleProcessed = 0
        currAngle, StageController = utils.Calibrate(StageControllerCOM, StageController)



## Starting the Exepriment Function
def StartSpatialRecogExperiment(self, DialogBoxOutput):
    self.StageStatIndecator.setText("Calibrating...")
      
    ## Calibrating the Stage
    if self.StageCalibStat == False or self.currAngle != 0: 
        
        self.currAngle, self.arduino = utils.Inititialise(self.StageControllerPort)
        # time.sleep(2)
        self.StageStatIndecator.setText("Ready!")
        self.StageCalibStat = True


    
    ## Valifying all experimental params are set correctly
    self.ExperimentStatIndecator.setText("Varifying Parameters")
    try:
        self.NumberOfSamples = int(self.SampleSizeInput.text())

        try:
            self.Period = int(self.PeriodInput.text())
            
            try:
                self.NumberOfChannels = int(self.ChannelNumberInput.text())

                try:
                    self.Increment = int(self.IncrementInput.text())
                    if self.Increment <= 180:
                        try:
                            self.RotAngle = int(self.RotAngleInput.text())
                            if self.RotAngle >= self.Increment*2 and self.RotAngle <= 360:
                                self.Direction = self.DirectionSectionComboBox.currentText()
                                if self.Direction == "Anti-ClockWise":
                                    self.Direction = 0
                                else:
                                    self.Direction = 1

                                print(self.Direction)

                                DialogBoxOutput.setText("Success! \nStarting the Experiment Now... ")
                                
                                ## Creating relavent Directories
                                self.ExperimentStatIndecator.setText("Starting...")
                                print("starting")
                                ExperimentName, ExperimentDIR = DataManagement.creatDirectorySpatialRec(self.Increment, self.RotAngle, self.NumberOfChannels)    
                                print("Relavent Directories Creates")
                                self.ExperimentNameIndecator.setText(ExperimentName)
                                print(self.DataCollectorPort, self.StageControllerPort, 
                                                self.arduino, 0, self.NumberOfSamples, self.NumberOfChannels, 
                                                self.Period, self.Increment, self.RotAngle, self.Direction, 
                                                ExperimentName, ExperimentDIR)
                                try:
                                    DataCollection(self.DataCollectorPort, self.StageControllerPort, 
                                                self.arduino, 0, self.NumberOfSamples, self.NumberOfChannels, 
                                                self.Period, self.Increment, self.RotAngle, self.Direction, 
                                                ExperimentName, ExperimentDIR)
                                except:
                                    print("Error Starting the test!")
                            else:
                                DialogBoxOutput.setText("Rotation angle must be at least over two times the size of the increments") 
                        
                        except:
                            print("Rotation angle must be an integer!")
                            DialogBoxOutput.setText("Rotation angle must be an integer!") 
                    
                    else:
                        DialogBoxOutput.setText("Please Chose a sensible Increments") 
                except:
                    print("Increments must be an integer!")
                    DialogBoxOutput.setText("Increments must be an integer!")               
            except:
                print("Number of Channels must be an integer!")
                DialogBoxOutput.setText("Number of Channels must be an integer!")
        except:
            print("Period must be an integer!")
            DialogBoxOutput.setText("Period must be an integer!")
    except:
        print("Sample number must be an integer!")
        DialogBoxOutput.setText("Sample number must be an integer!")


## Homming the stage to zero
def HomeTheStage(self, StageControllerPort, arduino, DialogBoxOutput):
    try:
        self.StageStatIndecator.setText("Calibrating...")
        self.currAngle, self.arduino = utils.Calibrate(StageControllerPort, arduino)
        self.StageStatIndecator.setText("Ready!")
    except:
        DialogBoxOutput.setText("Calibration failed!\nFirst Initialize the stage by running an experiment.") 
        self.StageStatIndecator.setText("Calibrating failed")
