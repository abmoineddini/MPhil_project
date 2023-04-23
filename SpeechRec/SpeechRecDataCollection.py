import utils
import DataManagement
import os
import time
import numpy as np
import serial
import pandas as pd
import random
import math
from SpeechRec import Speech_Rec_utils
import subprocess
import IoTConnection



def DataCollection(DataCollectionCOM, NumSamples, NumChannels, ExperimentDIR):
    # Fining all the classes in the range of rotation

    # print(progressMatrix)
    # CompleteprogressMatrix = "0:0 " + progressMatrix
    # print("sending {}".format(CompleteprogressMatrix))
    # IoTConnection.Data_Collection_Pub_IoT(ExperimentDIR, CompleteprogressMatrix)

    # # Start the web base dashboard data monitoring
    # dashStartCMD = "python SpatialRec/DashboardSpatialRecognition.py -d " + ExperimentDIR +"/RawData"
    # DashBoardStart = subprocess.Popen(["start", "cmd", "/k", dashStartCMD], shell = True)
    Audio_path_dir = "SpeechRec/AudioFiles/"
    AudioFiles = os.listdir(Audio_path_dir)
    
    print(AudioFiles)
    totalSampleProcessed = 0
    InitalInspect = True
    for Audio in AudioFiles:
        # Setting Angle
        Audio_path = Audio_path_dir + Audio
        print(Audio_path)
        for Sample in range(NumSamples):
            # Finding Suitable name for the sample
            NameTest = True
            RawDataDIR = os.path.join(ExperimentDIR, "RawData")
            testNum = 1
            Files = [f for f in os.listdir(RawDataDIR) if os.path.isfile(os.path.join(RawDataDIR, f))]
            while NameTest:
                CSVName = str(Audio.replace(".wav", "")) + '-Test-'+ str(testNum) + '.csv'
                if CSVName in Files:
                    print("File Already exist, Trying another name.")
                    testNum = testNum+1
                else:
                    NameTest = False

            print("Test name is : {}".format(CSVName))

            SampleName = os.path.join(RawDataDIR, CSVName)

            if NumChannels == 1:
                Speech_Rec_utils.collectData_1_Channel(DataCollectionCOM, SampleName, Audio_path)
            elif NumChannels == 2:
                Speech_Rec_utils.collectData_1_Channel(DataCollectionCOM, SampleName, Audio_path)
            elif NumChannels == 3:
                Speech_Rec_utils.collectData_3_Channel(DataCollectionCOM, SampleName, Audio_path)
            elif NumChannels == 4:
                Speech_Rec_utils.collectData_4_Channel(DataCollectionCOM, SampleName, Audio_path)


## Starting the Exepriment Function
def StartSpeechRecogExperiment(self):
    
    ## Valifying all experimental params are set correctly
    self.ExperimentStatIndecator.setText("Varifying Parameters")
    # try:
    self.NumberOfSamples = int(self.SampleSizeInput_speech.text())
        # try:
    self.NumberOfChannels = int(self.ChannelNumber_speech.text())
        
        ## Creating relavent Directories
    self.ExperimentStatIndecator.setText("Starting...")
    print("starting")
    ExperimentName, ExperimentDIR = DataManagement.creatDirectorySpeechRec(self.NumberOfChannels)    
    print("Relavent Directories Creates")
    print(self.DataCollectorPort_speech, self.NumberOfSamples, self.NumberOfChannels, ExperimentName, ExperimentDIR)
    # try:
    DataCollection(self.DataCollectorPort_speech, self.NumberOfSamples, self.NumberOfChannels, ExperimentDIR)
    #         except:
    #             print("Error Starting the test!")            
    #     except:
    #         print("Number of Channels must be an integer!")
    # except:
    #     print("Sample number must be an integer!")

