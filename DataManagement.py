import pandas
import os
from datetime import date

def creatDirectory(Increment, RotAngle):
    today = date.today()
    DIRName = "TrainingData"
    if os.path.exists(DIRName) == False:
        os.mkdir(DIRName)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    print(int(today.month))
    ExperimentName =  str(Increment) + "Deg_" + str(RotAngle) + "Deg_" + str(today.day) + "-" + months[int(today.month) - 1] + "-" + str(today.year)
    ExperimentDir = os.path.join(DIRName, ExperimentName)
    if os.path.exists(ExperimentDir) == False:
        os.mkdir(ExperimentDir)
    
    print(ExperimentName)
    return ExperimentName, ExperimentDir

