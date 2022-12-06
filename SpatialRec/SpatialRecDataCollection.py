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


def DataCollection(DataCollectionCOM, StageControllerCOM, StageController, currAngle, NumSamples, NumChannels, Period, Increment, RotAngle, Direction, ExperimentName, ExperimentDIR):
    # Fining all the classes in the range of rotation
    if Direction == 1:
        Increments = np.linsapce(0, RotAngle, int(RotAngle/Increment)+1)
    else:  
        Increments = np.linsapce(360-RotAngle, 0, int(RotAngle/Increment)+1)

    # Start the web base dashboard data monitoring
    dashStartCMD = "python SpatialRec/DashboardSpatialRecognition.py -d " + ExperimentDIR +"/RawData"
    DashBoardStart = subprocess.Popen(["start", "cmd", "/k", dashStartCMD], shell = True)
    
    totalSampleProcessed = 0
    InitalInspect = True
    for Angle in Increments:
        # Setting Angle
        currAngle = utils.AngleSet(Angle, StageController, currAngle)

        for Sample in range(NumSamples):
            # Finding Suitable name for the sample
            NameTest = True
            RawDataDIR = os.path.join(ExperimentDIR, "RawData")
            testNum = 1
            while NameTest:
                CSVName = str(Increment) + '-Test-'+ str(testNum) + '.csv'
                if CSVName in RawDataDIR:
                    print("File Already exist, Trying another name.")
                    testNum = testNum+1
                else:
                    NameTest = False

            SampleName = os.path.join(RawDataDIR, CSVName)
            Spatial_Rec_utils.DataCollect(DataCollectionCOM, NumChannels, Period, SampleName)
            if InitalInspect:
                Spatial_Rec_utils.plotPreviewFigures(SampleName, NumChannels)
            else:
                RandInspect = random.randint(0, 70)
                if RandInspect == 7:
                    Spatial_Rec_utils.plotPreviewFigures(SampleName, NumChannels)


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
                                ExperimentName, ExperimentDIR = DataManagement.creatDirectorySpatialRec(self.Increment, self.RotAngle, self.NNumberOfChannels)    
                                self.ExperimentNameIndecator.setText(ExperimentName)


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
