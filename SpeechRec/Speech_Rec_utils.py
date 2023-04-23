import time
import serial
import math
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
from threading import Timer
import webbrowser
import winsound

def playAudioFile(Name):
    # AudioFileName = Name.split('/')
    # AudioFileName = AudioFileName[1].split('.')
    # AudioFileName = "AudioOriginal/"+AudioFileName[0]+'.wav'
    winsound.PlaySound(Name, winsound.SND_ASYNC | winsound.SND_ALIAS )

def collectData_1_Channel(COMPort, Name, AudioFileName):
    Channel1 = []
    Time = []
    dataCollection = False
    dataAvailability = True
    i = 0
    j = 0
    FirstCounter = True
    sR = 4000 / 3.5
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    if FirstCounter:
        for i in range(4000):
            print(line)
        FirstCounter = False
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            # print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 210:
                        dataCollection = False
                    else:
                        dataCollection = True
                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                Channel1.append(int(vals[0]))
                                Time.append(i / sR)
                                i = i + 1
                                j = 5000
                        # print("StartingDataCollection")

        while dataCollection:
            line = arduino.readline()
            print(line)
            if line != (''):
                try:
                    string = line.decode()
                except:
                    print("ignored")
                else:
                    numS = string.replace("\r\n", '')
                    if numS.isdigit():
                        if int(numS) < 210:
                            j = j - 1
                        else:
                            j = 5000

                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                Channel1.append(int(vals[0]))
                                Time.append(i / sR)
                                i = i + 1
                                j = 5000

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Channel1}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return [Channel1, Time]


def collectData_2_Channel(COMPort, Name, AudioFileName):
    Channel1 = []
    Channel2 = []
    Time = []
    dataCollection = False
    dataAvailability = True
    i = 0
    j = 0
    FirstCounter = True
    sR = 4000 / 3.5
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    if FirstCounter:
        for i in range(4000):
            print(line)
        FirstCounter = False
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            # print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 210:
                        dataCollection = False
                    else:
                        dataCollection = True
                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    Channel1.append(int(vals[0]))
                                    Channel2.append(int(vals[1]))
                                    Time.append(i / sR)
                                    i = i + 1
                                    j = 5000
                        # print("StartingDataCollection")

        while dataCollection:
            line = arduino.readline()
            print(line)
            if line != (''):
                try:
                    string = line.decode()
                except:
                    print("ignored")
                else:
                    numS = string.replace("\r\n", '')
                    if numS.isdigit():
                        if int(numS) < 210:
                            j = j - 1
                        else:
                            j = 5000

                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    Channel1.append(int(vals[0]))
                                    Channel2.append(int(vals[1]))
                                    Time.append(i / sR)
                                    i = i + 1
                                    j = 5000

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Channel1,'Channel 2 (V)': Channel2}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return [Channel1, Channel2, Time]



def collectData_3_Channel(COMPort, Name, AudioFileName):
    Channel1 = []
    Channel2 = []
    Channel3 = []
    Time = []
    dataCollection = False
    dataAvailability = True
    i = 0
    j = 0
    FirstCounter = True
    sR = 4000 / 3.5
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    if FirstCounter:
        for i in range(4000):
            print(line)
        FirstCounter = False
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            # print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 210:
                        dataCollection = False
                    else:
                        dataCollection = True
                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        Channel1.append(int(vals[0]))
                                        Channel2.append(int(vals[1]))
                                        Channel3.append(int(vals[2]))
                                        Time.append(i / sR)
                                        i = i + 1
                                        j = 5000
                        # print("StartingDataCollection")

        while dataCollection:
            line = arduino.readline()
            print(line)
            if line != (''):
                try:
                    string = line.decode()
                except:
                    print("ignored")
                else:
                    numS = string.replace("\r\n", '')
                    if numS.isdigit():
                        if int(numS) < 210:
                            j = j - 1
                        else:
                            j = 5000

                        vals = numS.split(" ")
                        if len(vals) > 2:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        Channel1.append(int(vals[0]))
                                        Channel2.append(int(vals[1]))
                                        Channel3.append(int(vals[2]))
                                        Time.append(i / sR)
                                        i = i + 1
                                        j = 5000

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Channel1,'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return [Channel1, Channel2, Channel3, Time]




def collectData_4_Channel(COMPort, Name, AudioFileName):
    Channel1 = []
    Channel2 = []
    Channel3 = []
    Channel4 = []
    Time = []
    dataCollection = False
    dataAvailability = True
    i = 0
    j = 0
    FirstCounter = True
    sR = 4000 / 3.5
    arduino = serial.Serial(COMPort , 2000000, timeout=1)
    line = arduino.readline()
    if FirstCounter:
        for i in range(4000):
            print(line)
        FirstCounter = False
    winsound.PlaySound(AudioFileName, winsound.SND_ASYNC | winsound.SND_ALIAS)
    while dataAvailability:
        line = arduino.readline()
        if line != (''):
            # print(line)
            try:
                string = line.decode()
            except:
                print("ignored")
            else:
                numS = string.replace("\r\n", '')
                if numS.isdigit():
                    print(int(numS))
                    if int(numS) < 210:
                        dataCollection = False
                    else:
                        dataCollection = True
                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        if vals[3].isdigit():
                                            Channel1.append(int(vals[0]))
                                            Channel2.append(int(vals[1]))
                                            Channel3.append(int(vals[2]))
                                            Channel4.append(int(vals[3]))
                                            Time.append(i / sR)
                                            i = i + 1
                                            j = 5000
                        # print("StartingDataCollection")

        while dataCollection:
            line = arduino.readline()
            print(line)
            if line != (''):
                try:
                    string = line.decode()
                except:
                    print("ignored")
                else:
                    numS = string.replace("\r\n", '')
                    if numS.isdigit():
                        if int(numS) < 210:
                            j = j - 1
                        else:
                            j = 5000

                        vals = numS.split(" ")
                        if len(vals) > 3:
                            if vals[0].isdigit():
                                if vals[1].isdigit():
                                    if vals[2].isdigit():
                                        if vals[3].isdigit():
                                            Channel1.append(int(vals[0]))
                                            Channel2.append(int(vals[1]))
                                            Channel3.append(int(vals[2]))
                                            Channel4.append(int(vals[3]))
                                            Time.append(i / sR)
                                            i = i + 1
                                            j = 5000

                        if j < 1:
                            dataCollection = False
                            dataAvailability = False


    arduino.close()
    import pandas as pd
    dict = {'Time (s)': Time, 'Channel 1 (V)': Channel1,'Channel 2 (V)': Channel2, 'Channel 3 (V)': Channel3, 'Channel4 (V)': Channel4}

    df = pd.DataFrame(dict)
    dataBaseName = "TrainingData/" + Name + ".csv"
    df.to_csv(dataBaseName)
    print(dataBaseName)
    return [Channel1, Channel2, Channel3, Channel4, Time]

def plotSize(ChannelNum):
    i = int(math.sqrt(ChannelNum))
    j = i
    if i**2 < ChannelNum:
        if i == j:
            i += 1
    if j*i < ChannelNum:
        if i > j:
            j += 1
    return i, j  ## Number of Columns, number of Rows

def plotPreviewFigures(CSVFileName, NumChannels):
    pass
