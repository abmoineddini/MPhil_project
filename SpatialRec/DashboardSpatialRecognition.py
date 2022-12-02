import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import numpy as np
#from SpatialRec import Spatial_Rec_utils
import Spatial_Rec_utils
import serial
import signal
import webbrowser
from threading import Timer



def DataCollectionDashboard(samples, Increment, RangeRotation, Directory):
    mypath = Directory
    CSVFiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    progress = 0
    Start = True

    df_prog = pd.DataFrame({'names' : [' ', 'Progress'],
                            'values' :  [100 - progress, progress]})

    df_prog_total = pd.DataFrame({'names' : [' ', 'Progress'],
                                'values' :  [100 - 2*progress, 2*progress]})

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    dropDownMen_test = dcc.Dropdown(options=CSVFiles, 
                                placeholder="Select a Test", 
                                clearable=False, 
                                style={"width" : "50%"})

    ## Current Test progress pie chart
    piChart_current = go.Pie(labels=df_prog.loc[:,'names'], 
                                    values=df_prog.loc[:, 'values'], 
                                    hole = 0.5,
                                    marker=dict(colors=["white", "#636EFA"]),
                                    sort=False, name=" Current Test Progress")

    ## Overall Test progress pie chart
    piChart_total = go.Pie(labels=df_prog_total.loc[:,'names'], 
                                    values=df_prog_total.loc[:, 'values'], 
                                    hole = 0.5,
                                    marker=dict(colors=["white", "#636EFA"]),
                                    sort=False, name= "Overall Progress")

    pieFig = make_subplots(rows=2, cols=1, specs=[[{"type": "domain"}],[{"type": "domain"}]])
    pieFig.add_trace(piChart_current, row=1, col=1)
    pieFig.add_trace(piChart_total, row=2, col=1)

    graphView1 = dcc.Graph(figure=pieFig)
    graphView2 = dcc.Graph(figure={})
    CounterVal = dcc.Input(id = "Samples", type="number", min=1, max=samples, step=1, value=1)
    IncrementCounter = dcc.Input(id = "Increments", type="number", min=0, max=RangeRotation, step=Increment, value=0)
    app.layout = html.Div([
            html.Div([CounterVal, IncrementCounter
            ],style={'display': 'none'}),
            html.Div([html.H1('Progress and Data Preview'), 
            dcc.Interval(id='interval-component',interval=10*1000, n_intervals=1, max_intervals=samples),
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
    ############### Plot Progress ##################
    @app.callback([Output(graphView1, 'figure'), 
                    Output(component_id=dropDownMen_test, component_property='options'), 
                    Output('Samples', 'value')], 
                    Input('Samples', 'value'), 
                    Input('Samples', 'max'), 
                    Input('Increments', 'value'), 
                    Input('Increments', 'max'), 
                    Input('Increments', 'step'), 
                    Input('interval-component', 'n_intervals'))   
    def collectData(sample, maxVal, currIncrement, RangeRot, Increment, n):
        progress_curr = 100*(sample/maxVal)
        totalSampleCollected = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        prog_total = 100*(len(totalSampleCollected)/(maxVal*(int(RangeRot/Increment)+1)))
        
        Spatial_Rec_utils.DataCollect("COM4", 4, 2, "testing/temp/90-test-"+str(sample)+".csv")

        df_prog = pd.DataFrame({'names' : [' ', 'Progress'],
                                'values' :  [100 - progress_curr, progress_curr]})

        df_prog_total = pd.DataFrame({'names' : [' ', 'Progress'],
                                    'values' :  [100 - prog_total, prog_total]})

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        dropDownMen_test = dcc.Dropdown(options=CSVFiles, 
                                    placeholder="Select a Test", 
                                    clearable=False, 
                                    style={"width" : "50%"})

        ## Current Test progress pie chart
        piChart_current = go.Pie(labels=df_prog.loc[:,'names'], 
                                        values=df_prog.loc[:, 'values'], 
                                        hole = 0.5,
                                        marker=dict(colors=["white", "#636EFA"]),
                                        sort=False)

        ## Overall Test progress pie chart
        piChart_total = go.Pie(labels=df_prog_total.loc[:,'names'], 
                                        values=df_prog_total.loc[:, 'values'], 
                                        hole = 0.5,
                                        marker=dict(colors=["white", "#636EFA"]),
                                        sort=False)


        pieFig = make_subplots(rows=2, cols=1, specs=[[{"type": "domain"}],[{"type": "domain"}]])
        pieFig.add_trace(piChart_current, row=1, col=1)
        pieFig.add_trace(piChart_total, row=2, col=1)

        graphView1 = pieFig

        options = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        
        sample = sample+1
        return graphView1, options, sample
    

    ############### Plot Figures ################
    @app.callback(Output(component_id=graphView2, component_property='figure'),
                Input(component_id=dropDownMen_test, component_property='value'))   
    def updateGraph(SampleNumber):
        if SampleNumber==None:
            fig = go.FigureWidget(make_subplots(rows=1, cols=1))

        else:
            df = pd.read_csv(os.path.join("testing/temp", str(SampleNumber)))    
            cols, rows = Spatial_Rec_utils.plotSize((len(df.axes[1])-2))
            titles = ()
            for i in range(len(df.axes[1])-2):
                title = "Channel" + str(i)
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

    @app.callback(Output('StatusOfDataCollection', 'children'),
                Input('EndDataCollection', 'n_clicks'))
    def ShutdownApp(n):
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
        app.run(debug=True)

        
DataCollectionDashboard(10, 30, 90)


