import pandas
import os
from datetime import date

def creatDirectorySpatialRec(Increment, RotAngle, Channels):
    today = date.today()
    DIRName = "TrainingData/Spatial_Recognition"
    if os.path.exists(DIRName) == False:
        os.makedirs(DIRName)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    print(int(today.month))
    ExperimentName = str(Channels) +"Ch" + "-" + str(Increment) + "Deg_" + str(RotAngle) + "Deg_" + str(today.day) + "-" + months[int(today.month) - 1] + "-" + str(today.year)
    ExperimentDir = os.path.join(DIRName, ExperimentName)
    if os.path.exists(ExperimentDir) == False:
        os.mkdir(ExperimentDir)
        os.mkdir(os.path.join(ExperimentDir, "Logs"))
        os.mkdir(os.path.join(ExperimentDir, "RawData"))
        os.mkdir(os.path.join(ExperimentDir, "Figures"))

        ## Making the Training, Validation and Testing dase
        os.mkdir(os.path.join(ExperimentDir, "DataBase"))
        os.mkdir(os.path.join(ExperimentDir, "DataBase", "training"))
        os.mkdir(os.path.join(ExperimentDir, "DataBase", "Validation"))
        os.mkdir(os.path.join(ExperimentDir, "DataBase", "Testing"))

    
    print(ExperimentName)
    return ExperimentName, ExperimentDir
