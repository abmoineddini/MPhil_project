import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import os
import signal
from threading import Timer
import webbrowser
from werkzeug.serving import run_simple
from  multiprocessing import Process
import numpy as np
# from SpatialRec import Spatial_Rec_utils
import Spatial_Rec_utils
import serial
# from ... import utils

def angleSetPluseCalibration(comPort, angle):
    arduino = serial.Serial(comPort, 9600, timeout=1)
    line = arduino.readline()
    print(line)
    try:
        string = line.decode()
    except:
        print("ignored")
    else:
        numS = string.replace("\r\n", '')

        while numS != "ready":
            line = arduino.readline()
            line = line.decode()
            numS = line.replace("\r\n", '')
        while line != "Starting":
            arduino.write(b"rdy")
            line = arduino.readline()
            line = line.decode()
            line = line.replace("\r\n", '')

        print("Starting")
    time.sleep(1)
    angle = str(angle)
    arduino.write(angle.encode())
    line = arduino.readline()
    line = line.decode()
    line = line.replace("\r\n", '')
    while line!="done":
        line = arduino.readline()
        print(line)
        line = line.decode()
        line = line.replace("\r\n", '')

    while not line.isdigit():
        line = arduino.readline()
        print(line)
        line = line.decode()
        line = line.replace("\r\n", '')
    currAng = int(line)
    print("Speaker is at ", currAng, " Degrees now")
    arduino.close()

    return currAng

def DataCollectionDashboard(samples, Period, Direction, Increment, RotAngle,  ExperimentDir):
    mypath = "testing/temp"
    CSVFiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    if Direction == 1:
        Increments = np.linspace(Increment, RotAngle, int(RotAngle/Increment))
    else:  
        Increments = np.linspace(360-RotAngle, Increment, int(RotAngle/Increment))
    print(Increments)
    progress = 0

    df_prog = pd.DataFrame({'names' : ['Progress', ' '],
                        'values' :  [progress, 100 - progress]})

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    theme = {'dark': True}

    dropDownMen_test = dcc.Dropdown(options=CSVFiles, 
                                placeholder="Select a Test", 
                                clearable=False, 
                                style={"width" : "50%"})

    ## Setting up figures
    piChart = px.pie(df_prog, values= 'values', names = 'names', hole = 0.5,
                        color_discrete_sequence = ["#636EFA", 'rgba(0,0,0,0)'])
    piChart.data[0].textfont.color = 'white'
    piChart.data[0]["labels"] = ['Progress = '+ ('%.2f' % progress) + "%", ' ']
    graphView1 = dcc.Graph(figure=piChart)
    graphView2 = dcc.Graph(figure={})


    CounterSample_perIncrement = dcc.Input(id = "SamplesUpdate", type="number", min=1, max=samples, step=1, value=1)
    #IncrementCounter = dcc.Input(id = "IncrementCounter", type="number", min=0, max=Increment*len(Increments-1), step=Increment, value=0)
    CounterSample_Total = dcc.Input(id = "TotalSamples", value=1)
    # TimeConst_1 = dcc.Input(id = "Time_interval_AngleSet", value = (Increment * 50)/100 +2)
    # TimeConst_2 = dcc.Input(id = "Time_interval_for_calibration", value = (200 * 50)/100 +2)

    app.layout = html.Div([
            html.Div([CounterSample_perIncrement, CounterSample_Total,
                    #TimeConst_1, TimeConst_2,
                    html.Div(id="WorkingDirectory", children = ExperimentDir),
                    html.Div(id="CollectionPeriod", children = Period),
                    dcc.Input(id="StageAdjustmentStat", value = "False"),
                    html.Div(id="StageCalibrationOrAdjustment", children = ""),
                    html.Div(id="TimeCounter"),
                    html.Div(id= "StageControllerCOM", children = "COM3"),
                    html.Div(id= "CurrentAngle", children = 0),
                    html.Button(id= "Increment" , children = Increment)
                    ],style={'display': 'none'}),
            html.Div([html.H1('Progress and Data Preview'), 
            dcc.Interval(id='interval-component', interval=(Period + 7)*1000, n_intervals=0, max_intervals=samples*len(Increments-1)),
            # dcc.Interval(id='interval-component-stage',  interval=(((Increment * 100)/100)+2)*1000, n_intervals=0, disabled=True),
            html.Div([    
                html.H4("Select the Test"),
                dropDownMen_test], style={"width" : "75%", 'display': 'inline-block'}),
            html.Div([
                html.H3("Progress")], style={"width" : "25%", 'display': 'inline-block'}),
            html.Div([
                graphView2], style={"width" : "75%", 'display': 'inline-block'}),
            html.Div([
                graphView1], style={"width" : "25%", 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Button("End data Collection", id="EndDataCollection", n_clicks=0),
            html.Div(id='StatusOfDataCollection')
            ])
        ])

    ## Adjusting stage to desired angle
    # @app.callback(Output("CurrentAngle", "children"),
    #                 Input("StageAdjustmentStat", "value"),
    #                 Input("StageControllerCOM", "children"),
    #                 Input("IncrementCounter", "value"), 
    #                 Input("interval-component", "disabled"),
    #                 Input("CurrentAngle", "children"))
    # def StageMover(StageMoveStat, COM, Angle, Timer_State, currAngle, Trigger, n):
    #     if StageMoveStat == "True":
    #         currAngle = angleSetPluseCalibration(COM, Angle)
    #         Time_Counter_Disabled = False
    #         Trigger = True
    #     else:
    #         currAngle = currAngle
    #     return currAngle

    ## Data Collection and Determining when to adjust the stage
    @app.callback([Output(graphView1, 'figure'), 
                    Output(dropDownMen_test, 'options'), 
                    Output('SamplesUpdate', 'value'),
                    Output("StageAdjustmentStat", "value"),
                    Output("interval-component", "interval"),
                    Output("CurrentAngle", "children")],
                    [Input('SamplesUpdate', 'value'),           # 1.Sample Number
                    Input('SamplesUpdate', 'max'),              # 2.Max number of Samples
                    Input('interval-component', 'n_intervals'), # 3.interval Number
                    Input("WorkingDirectory", "children"),      # 4.Directory
                    Input("CollectionPeriod", "children"),      # 5.Collection Period
                    Input("StageAdjustmentStat", "value"),      # 6.Whether the stage is moving or not
                    Input("interval-component", "interval"),    # 7.Time Interval delay
                    Input("StageControllerCOM", "children"),    # 8.COM port for stage Controller
                    Input("CurrentAngle", "children"),           # 9.current angle
                    Input("Increment" , "children")])           # 10. Increment
    def collectData(sample, maxVal, n, Direcotry, Period, StageAdjStat, 
                    Time_counter_Interval, COM, Angle, Increment):      
        # if StageAdjStat == "True":
        #     StageAdjStat = "False"
        #     sample = 1
        #     print(Angle)
        #     Angle = angleSetPluseCalibration(COM, Angle)
        #     graphView1  = px.pie(df_prog, values= 'values', names = 'names', hole = 0.5,
        #             color_discrete_sequence = ["#636EFA", 'rgba(0,0,0,0)'])
        #     graphView1 .data[0].textfont.color = 'white'
        #     graphView1 .data[0]["labels"] = ['Progress = '+ ('%.2f' % progress) + "%", ' ']
        #     print(1)
        #     Time_counter_Interval = (Period + 7)*1000
        #     return graphView1, options, sample, StageAdjStat, Time_counter_Interval, Angle
            
        print(sample)
        print(maxVal)
        print("Collecting Data ...")
        progress = 100*(sample/(maxVal))

        Spatial_Rec_utils.DataCollect("COM4", 4, Period, "testing/temp/File-"+ str(Angle)+"-"+str(sample)+".csv")
        print("Data Collect Done!")
        df_prog = pd.DataFrame({'names' : ['Progress', ' '],
            'values' :  [progress, 100 - progress]})

        graphView1 = px.pie(df_prog, values= 'values', names = 'names', hole = 0.5,
                            color_discrete_sequence = ["#636EFA", 'rgba(0,0,0,0)'])
        graphView1.data[0].textfont.color = 'white'
        graphView1.data[0]["labels"] = ['Progress = '+ ('%.2f' % progress) + "%", ' ']
        options = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        # if sample == maxVal:
        #     Time_counter_Interval = (((Increment * 500)/100)+2)*1000
        #     print(Increment)
        #     Angle = Angle + Increment
        #     StageAdjStat = "True"
        # else:
        #     StageAdjStat = "False"
        sample = sample+1
        return graphView1, options, sample, StageAdjStat, Time_counter_Interval, Angle


    ## Plotting figures
    @app.callback(Output(component_id=graphView2, component_property='figure'),
                  Input(component_id=dropDownMen_test, component_property='value'))   
    def updateGraph(SampleNumber):
        if SampleNumber==None:
            fig = {}

        else:
            df = pd.read_csv(os.path.join("testing/temp", str(SampleNumber)))    
            cols, rows = Spatial_Rec_utils.plotSize((len(df.axes[1])-2))
            titles = ()
            for i in range(len(df.axes[1])-2):
                title = "Channel" + str(i+1)
                titles += (title, )
            fig = go.FigureWidget(make_subplots(rows=rows, cols=cols, subplot_titles=titles))        
            for row in range(rows):
                for col in range(cols):
                    Channel = "Ch" + str(row + col + 1)
                    fig.add_trace(go.Scatter(x=df.loc[:, "Time"], y=df.loc[:, Channel]), row=row+1, col=col+1)
                    fig.update_xaxes(title_text="Time (s)", row=row+1, col=col+1)
                    fig.update_yaxes(title_text="Voltage Output (v)", row=row+1, col=col+1)

            fig.update_layout(showlegend=False, height=700, title = {"text":"Plot for the Experiment " + str(SampleNumber), 
                                                                    'y':0.97,
                                                                    'x':0.5,
                                                                    'font_size' : 24,
                                                                    'xanchor': 'center', 
                                                                    'yanchor': 'top'})
        
        graphView2 = fig
        return graphView2


    ## Shutting down data collection
    @app.callback(Output('StatusOfDataCollection', 'children'),
                  Input('EndDataCollection', 'n_clicks'))
    def shutDown(n):
        if n == 1:
            os.kill(os.getpid(), signal.SIGTERM)
            msg = "Shutting Down"
        else:
            msg = "Collecting Data" 
        return msg

    def open_browser():
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://127.0.0.1:8050/')

    if __name__ == '__main__':

        Timer(1, open_browser).start()
        server = Process(target=app.run(debug=True))
        run_simple("localhost", 8050, server)
        server.terminate()


#DataCollectionDashboard(samples, Period, Direction, Increment, RotAngle,  ExperimentDir):
DataCollectionDashboard(10, 2, 1, 15, 60, "Testing")