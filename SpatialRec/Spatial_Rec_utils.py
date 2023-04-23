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


## Data collection using python
def DataCollect_old(DataCollectionCOM, Channels, Period, SampleName):
    Arduino = serial.Serial(DataCollectionCOM , 2000000, timeout=1)
    time.sleep(5)
    Input = "Time"
    print("Time")
    for i in range(Channels):
        ChName = "Ch" + str(i+1)
        Input = np.append(Input, ChName)
    
    stime = time.time_ns()
    difTime = 0
    Period = Period*(10**9)
    while difTime <= Period:
        line = Arduino.readline()
        # print(line)
        if line != (''):
            try:
                line = line.decode()
                line = line.replace("\r\n", '')
                line = line.split(",")
                if all(item.isdigit() for item in line) and len(line) == Channels:
                    difTime = time.time_ns() - stime
                    Input = np.vstack((Input, np.append(str(difTime), line)))
                    print(line)
            except:
                continue
    
    pd.DataFrame(np.delete(Input, 0, 0)).to_csv(SampleName, header=Input[0])
    Arduino.close()
    
    pd.DataFrame(np.delete(Input, 0, 0)).to_csv(SampleName, header=Input[0])
    Arduino.close()


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



import subprocess
## Data collection using c++ for faster
def DataCollect(DataCollectionCOM, Channels, Period, SampleName):
    subprocess.run(["../SerialCommunication/serialCOM/x64/Debug/serialCOM.exe", DataCollectionCOM, Channels, Period])
    file1 = open('temp.txt', 'r')
    countlines = 0
    Channels = 4 
    while True:
        countlines += 1
        line = file1.readline()
        if not line:
            break
        prevline = line
    file1.close()
    print("time : {} us".format(prevline))
    time = int(prevline)
    t = np.linspace(start=0, stop=time, num=countlines, dtype=int)
    print(t)
    file1 = open('temp.txt', 'r')

    Input = "T (s)"
    for i in range(Channels):
        ChName = "Ch" + str(i+1)
        Input = np.append(Input, ChName)


    for i in range(0, countlines):
        line = file1.readline()
        line = line.split("\n")
        line = line[0].split(",")
        try:
            if len(line) == Channels:
                data = np.empty(shape=(1, 5))
                for j in range(Channels):
                    line[j] = int(line[j], 16)
                tempArr = np.array(line)
                data = np.concatenate((t[i], tempArr), axis=None)
                Input = np.vstack((Input, data))
        except:
            print("Invalid Data")

    print(tempArr)
    print(data)
    print(Input)

    file1.close()
    pd.DataFrame(np.delete(Input, 0, 0)).to_csv(SampleName, header=Input[0])
    os.remove("temp.txt")