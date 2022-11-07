# Dash
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
# Else
from metrics import *
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data
add_data = pd.read_csv(f'datasets/additional_participant_data.csv', sep=',')
top = pd.read_csv(f'datasets/top20.csv', sep=',')
bot = pd.read_csv(f'datasets/bottom20.csv', sep=',')
all = pd.read_csv(f'datasets/groups_metrics.csv', sep=',')
comp = pd.read_csv(f'datasets/groups_comparison.csv', sep=',')
participants = get_participants()

# Vars
participant1 = 'p1'
labels_table = ["ID", "Ontology", "Visualization", "Task Success", "Time on Task (min)"]
info_participant = [
    "ID",
    "Ontologies",
    "Visualization",
    "Task_Success",
    "Time_On_Task",
]

## Tab 1
## TODO: GET A DATAFRAME WITH ALL METRICS FOR ALL PARTICIPANTS EXPORTED TO DATASETS
# CHANGE TABLE TO CARDS AND SHOW METRICS

participant_dropdown = dcc.Dropdown(id='participant1', 
    options=participants, 
    value='p1')

metrics_table = dash_table.DataTable(
    id="metrics_table",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=add_data[add_data["ID"] == participant1].to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

controls_participant = dbc.Card(
    [
        dbc.Form(
            [
                html.Label('Choose data:'), 
                html.Br(), 
                participant_dropdown,
            ]
        ),
    ],
    body=True,
    className='controls'
)


tab1_content = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1("Participant Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls_participant, sm=3),
                            dbc.Col(metrics_table, sm=6)
                        ]
                    )
                ]
            )
        )
    ]
)

## Tab 2 
quantile_dropdown = dcc.Dropdown(
    id='quantile-dropdown', options=['Top 25%','Bottom 25%','All'], value='Top 25%'
)

controls_quantile = dbc.Card(
    [
        dbc.Form(
            [html.Label('Choose data:'), html.Br(), quantile_dropdown,]
        ),
    ],
    body=True,
    className='controls'
)

tab2_content = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1("Quantile Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls_quantile, sm=3),
                            dbc.Col(
                                dcc.Graph(id='time_task')
                            ),
                            dbc.Col(
                                dcc.Graph(id='dist_success')
                            )
                        ]
                    )
                ]
            )
        )
    ]
)

app.layout = html.Div([
    html.H1(children='Eye Gaze Analysis Dashboard'),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Participant Analysis', children=tab1_content),
        dcc.Tab(label='Quantile Analysis', children=tab2_content),
    ]),
],
    style={
        'textAlign':'center'
    })

# Table
@app.callback(
    Output("metrics_table", "data"),
    Input("participant1", "value")
)
def update_table(participant):
    table_updated = add_data[add_data["ID"] == participant].to_dict("records")
    return table_updated

# Time vs Task Graph
@app.callback(
    Output(component_id='time_task', component_property='figure'),
    Input(component_id=quantile_dropdown, component_property='value')
)
def update_graph(quantile):
    if quantile == 'Top 25%':
        data = top
    elif quantile == 'Bottom 25%':
        data = bot
    else:
        data = all

    fig = px.scatter(data, x='Time_On_Task', y='Task_Success',
                       labels={'Task_Success': 'Task Success (%)','Time_On_Task':'Time on task (min)'},
                       title=f'Task Success vs Times on Task for {quantile}', 
                       trendline="ols",trendline_color_override="red")
    return fig

# Success distribution
@app.callback(
    Output(component_id='dist_success', component_property='figure'),
    Input(component_id=quantile_dropdown, component_property='value')
)
def update_graph(quantile):
    if quantile == 'Top 25%':
        data = top
    elif quantile == 'Bottom 25%':
        data = bot
    else:
        data = all

    fig = px.histogram(data, 'Task_Success',
                        title=f'Success distribution for {quantile}')
    return fig



app.run_server(debug=True)