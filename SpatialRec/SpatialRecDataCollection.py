import utils
import DataManagement
import time


def DataCollection(DataCollectionCOM, StageControllerCOM):
    pass

## Starting the Exepriment Function
def StartSpatialRecogExperiment(self, DialogBoxOutput):
    self.StageStatIndecator.setText("Calibrating...")

    ## Calibrating the Stage
    if self.StageCalibStat == False or self.currAngle != 0:  
        self.currAngle = utils.Inititialise(self.StageControllerPort)
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
                                ExperimentName, ExperimentDIR = DataManagement.creatDirectorySpatialRec(self.Increment, self.RotAngle)    
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
