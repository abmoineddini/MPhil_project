from PyQt5 import QtCore, QtGui, QtWidgets 
import utils
import serial
import time
import os


## Starting the Exepriment Function
def StartSpatialRecogExperiment(self, DialogBoxOutput):
    self.StageStatIndecator.setText("Calibrating...")
    self.StageControllerPort, self.DataCollectorPort = utils.COMFinder(self)
    self.currAngle, self.arduino = utils.Inititialise(self.StageControllerPort)
    time.sleep(1)
    self.StageStatIndecator.setText("Ready!")
    self.ExperimentStatIndecator.setText("Varifying Parameters")
    
    ## Creating relavent Directories


    ## Valifying all experimental params are set correctly
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
                                
                                DialogBoxOutput.setText("Success! \nStarting the Experiment Now... ")
                                self.ExperimentStatIndecator.setText("Starting...")




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
