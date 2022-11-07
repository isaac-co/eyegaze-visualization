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
both_groups = pd.read_csv(f'datasets/groups_metrics.csv', sep=',')
all = pd.read_csv(f'datasets/all_metrics.csv', sep=',')
comp = pd.read_csv(f'datasets/groups_comparison.csv', sep=',')
participants = get_participants()

# Vars
participant1 = 'p1'
ontology1 = 1
participant2 = 'p2'
ontology2 = 1
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

# Participant 1
participant_dropdown1 = dcc.Dropdown(id='participant1', 
    options=participants, 
    value='p1')

ontology_dropdown1 = dcc.Dropdown(id='ontology1', 
    options=[1,2], 
    value=1)

metrics_table1 = dash_table.DataTable(
    id="metrics_table1",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=add_data[(add_data["ID"] == participant1) & (add_data["Visualization"] == ontology1)].to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

controls_participant1 = dbc.Card(
    [
        dbc.Form(
            [
                html.Label('Choose a participant:'), 
                html.Br(), 
                participant_dropdown1,
            ]
        ),
        dbc.Form(
            [
                html.Label('Choose a visualization:'),
                html.Br(), 
                ontology_dropdown1,
            ]
        ),
    ],
    body=True,
    className='controls'
)

# Participant 2
participant_dropdown2 = dcc.Dropdown(id='participant2', 
    options=participants, 
    value='p2')

ontology_dropdown2 = dcc.Dropdown(id='ontology2', 
    options=[1,2], 
    value=1)

metrics_table2 = dash_table.DataTable(
    id="metrics_table2",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=add_data[(add_data["ID"] == participant2) & (add_data["Visualization"] == ontology2)].to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

controls_participant2 = dbc.Card(
    [
        dbc.Form(
            [
                html.Label('Choose a participant:'), 
                html.Br(), 
                participant_dropdown2,
            ]
        ),
        dbc.Form(
            [
                html.Label('Choose a visualization:'),
                html.Br(), 
                ontology_dropdown2,
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
                            dbc.Col(controls_participant1, sm=3),
                            dbc.Col(metrics_table1, sm=6)
                        ]
                    ),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls_participant2, sm=3),
                            dbc.Col(metrics_table2, sm=6)
                        ]
                    ),
                ]
            )
        )
    ]
)

## Tab 2 
quantile_dropdown = dcc.Dropdown(
    id='quantile-dropdown', options=['Top 25%','Bottom 25%','Top and Bottom','All'], value='Top 25%'
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

# Table 1
@app.callback(
    Output("metrics_table1", "data"),
    [Input("participant1", "value"), Input("ontology1", "value")]
)
def update_table1(participant, ontology):
    table_updated1 = add_data[(add_data["ID"] == participant) & (add_data["Visualization"] == ontology)].to_dict("records")
    return table_updated1

# Table 2
@app.callback(
    Output("metrics_table2", "data"),
    [Input("participant2", "value"), Input("ontology2", "value")]
)
def update_table2(participant, ontology):
    table_updated2 = add_data[(add_data["ID"] == participant) & (add_data["Visualization"] == ontology)].to_dict("records")
    return table_updated2

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
    elif quantile == 'Top and Bottom':
        data = both_groups
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
    elif quantile == 'Top and Bottom':
        data = both_groups
    else:
        data = all

    fig = px.histogram(data, 'Task_Success',
                        title=f'Success distribution for {quantile}')
    return fig



app.run_server(debug=True)