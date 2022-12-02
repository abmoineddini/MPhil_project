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



def DataCollect(DataCollectionCOM, Channels, Period, SampleName):
    Arduino = serial.Serial(DataCollectionCOM , 2000000, timeout=1)
    time.sleep(5)
    Input = "Time"
    for i in range(Channels):
        ChName = "Ch" + str(i+1)
        Input = np.append(Input, ChName)
    
    stime = time.time_ns()
    difTime = 0
    Period = Period*(10**9)
    while difTime <= Period:
        line = Arduino.readline()
        if line != (''):
            
            try:
                line = line.decode()
            except:
                continue
            else:
                line = line.replace("\r\n", '')
                line = line.split(" ")
                if all(item.isdigit() for item in line) and len(line) == Channels:
                    difTime = time.time_ns() - stime
                    Input = np.vstack((Input, np.append(str(difTime), line)))
    
    pd.DataFrame(np.delete(Input, 0, 0)).to_csv(SampleName, header=Input[0])
    Arduino.close()
    
    pd.DataFrame(np.delete(Input, 0, 0)).to_csv(SampleName, header=Input[0])


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



