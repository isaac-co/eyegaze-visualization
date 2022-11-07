from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
from metrics import *
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

# Variables and global dataframes
add_data = pd.read_csv(f'datasets/additional_participant_data.csv', sep=',')
top = pd.read_csv(f'datasets/top20.csv', sep=',')
bot = pd.read_csv(f'datasets/bottom20.csv', sep=',')
all = pd.read_csv(f'datasets/groups_metrics.csv', sep=',')
comp = pd.read_csv(f'datasets/groups_comparison.csv', sep=',')
participants = get_participants()


# Set up the app layout
quantile_dropdown = dcc.Dropdown(options=['Top 25%','Bottom 25%'], value='Top 25%')

app.layout = html.Div(children=[
    html.H1(children='Eye Gaze Analysis Dashboard'),
    quantile_dropdown,
    dcc.Graph(id='time_task')
],
    style={
        'textAlign':'center'
    })

# Time vs Task Graph
@app.callback(
    Output(component_id='time_task', component_property='figure'),
    Input(component_id=quantile_dropdown, component_property='value')
)
def update_graph(quantile):
    if quantile == 'Top 25%':
        data = top
    else:
        data = bot

    scatter_fig = px.scatter(data, x='Time_On_Task', y='Task_Success',
                       labels={'Task_Success': 'Task Success (%)','Time_On_Task':'Time on task (min)'},
                       title=f'Task Success per times on task for {quantile}', 
                       trendline="ols",trendline_color_override="red")
    return scatter_fig


app.run_server(debug=True)