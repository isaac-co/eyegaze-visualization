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

# Functions
def filter_data(quantile, visualization, domain):
    if quantile == 'Top 25%':
        data = top
    elif quantile == 'Bottom 25%':
        data = bot
    elif quantile == 'Top and Bottom':
        data = both_groups
    else:
        data = all

    if visualization == 'All':
        pass
    elif visualization == 'Tree':
        data = data[data['Visualization'] == 'Tree']
    elif visualization == 'Graph':
        data = data[data['Visualization'] == 'Graph']
    else:
        pass

    if domain == 'All':
        pass
    elif domain == 'Biomedical Domain':
        data = data[data['Ontologies'] == 'Biomedical Domain']
    elif domain == 'Conference Domain':
        data = data[data['Ontologies'] == 'Conference Domain']
    else:
        pass
    return data

# Some additional hard-coded data processing for formatting
all['Task_Success'] = all['Task_Success'] * 100
all['Task_Success'] = all['Task_Success'].round(2)
all['Percentage'] = all['Task_Success'].astype(str) + ' %'
all['mean_fixation_duration'] = all['mean_fixation_duration'].round(2)
all['mean_saccade_length'] = all['mean_saccade_length'].round(2)
all['mean_saccade_duration'] = all['mean_saccade_duration'].round(2)

top['Task_Success'] = top['Task_Success'] * 100
top['Task_Success'] = top['Task_Success'].round(2)
top['Percentage'] = top['Task_Success'].astype(str) + ' %'
top['mean_fixation_duration'] = top['mean_fixation_duration'].round(2)
top['mean_saccade_length'] = top['mean_saccade_length'].round(2)
top['mean_saccade_duration'] = top['mean_saccade_duration'].round(2)

bot['Task_Success'] = bot['Task_Success'] * 100
bot['Task_Success'] = bot['Task_Success'].round(2)
bot['Percentage'] = bot['Task_Success'].astype(str) + ' %'
bot['mean_fixation_duration'] = bot['mean_fixation_duration'].round(2)
bot['mean_saccade_length'] = bot['mean_saccade_length'].round(2)
bot['mean_saccade_duration'] = bot['mean_saccade_duration'].round(2)

both_groups['Task_Success'] = both_groups['Task_Success'] * 100
both_groups['Task_Success'] = both_groups['Task_Success'].round(2)
both_groups['Percentage'] = both_groups['Task_Success'].astype(str) + ' %'
both_groups['mean_fixation_duration'] = both_groups['mean_fixation_duration'].round(2)
both_groups['mean_saccade_length'] = both_groups['mean_saccade_length'].round(2)
both_groups['mean_saccade_duration'] = both_groups['mean_saccade_duration'].round(2)


# Vars
participant1 = 'p1'
visualization1 = "Graph"
participant2 = 'p7'
visualization2 = "Graph"
labels_table = ["ID", "Ontology", "Visualization", "Task Success", "Time on Task (min)","Total Fixations","Mean Fixation Duration",
    "Mean Saccade Length", "Mean Saccade Duration"]
info_participant = [
    "ID",
    "Ontologies",
    "Visualization",
    "Percentage",
    "Time_On_Task",
    "total_fixations",
    "mean_fixation_duration",
    "mean_saccade_length",
    "mean_saccade_duration",
]

## Tab 1

# Participant 1
participant_dropdown1 = dcc.Dropdown(id='participant1', 
    options=participants, 
    value='p1')

visualization_dropdown1 = dcc.Dropdown(id='visualization1', 
    options=['Tree','Graph'], 
    value='Graph')

metrics_table1 = dash_table.DataTable(
    id="metrics_table1",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=all[(all["ID"] == participant1) & (all["Visualization"] == visualization1)].to_dict("records"),
    style_cell={"textAlign": "center", "font_size": "14px"},
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
                visualization_dropdown1,
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

visualization_dropdown2 = dcc.Dropdown(id='visualization2', 
    options=['Tree','Graph'], 
    value='Graph')

metrics_table2 = dash_table.DataTable(
    id="metrics_table2",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=all[(all["ID"] == participant2) & (all["Visualization"] == visualization2)].to_dict("records"),
    style_cell={"textAlign": "center", "font_size": "14px"},
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
                visualization_dropdown2,
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
                    html.H1("Participant Comparison"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls_participant1, sm=3),
                            dbc.Col(metrics_table1, sm=6)
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='heatmap1'), sm=8)
                        ],
                    ),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls_participant2, sm=3),
                            dbc.Col(metrics_table2, sm=6)
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='heatmap2'), sm=8)
                        ],
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

visualization_dropdown = dcc.Dropdown(
    id='visualization-dropdown', options=['Tree','Graph','All'], value='All'
)

domain_dropdown = dcc.Dropdown(
    id='domain-dropdown', options=['Conference Domain','Biomedical Domain','All'], value='All'
)

visualization = 'Graph'
domain = 'Biomedical Domain'

group_table = dash_table.DataTable(
    id="group_table",
    columns=[
        {"name": col, "id": info_participant[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=all[(all["Visualization"] == visualization) & (all["Ontologies"] == domain)].to_dict("records"),
    style_cell={"textAlign": "center", "font_size": "14px"},
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

controls_quantile = dbc.Card(
    [
        dbc.Form(
            [
                html.Label('Choose a grouping:'), 
                html.Br(), 
                quantile_dropdown
            ],
        ),
        dbc.Form(
            [
                html.Label('Choose a visualization:'), 
                html.Br(), 
                visualization_dropdown
            ]
        ),
        dbc.Form(
            [
                html.Label('Choose a domain:'), 
                html.Br(), 
                domain_dropdown
            ]
        )
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
                            dbc.Col(group_table, sm=6)
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id='time_task'), sm=4
                            ),
                            dbc.Col(
                                dcc.Graph(id='dist_success'), sm=4
                            ),
                            dbc.Col(
                                dcc.Graph(id='heatmap_group'), sm=4
                            )
                        ],
                    ),
                ]
            )
        )
    ]
)

app.layout = html.Div([
    html.H1(children='Eye Gaze Analysis Dashboard', id='title'),
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
    [Input("participant1", "value"), Input("visualization1", "value")]
)
def update_table1(participant, visualization):
    table_updated1 = all[(all["ID"] == participant) & (all["Visualization"] == visualization)].to_dict("records")
    return table_updated1

# Heatmap 1
@app.callback(
    Output("heatmap1", "figure"),
    [Input("participant1", "value"), Input("visualization1", "value")]
)
def update_heatmap1(participant, visualization):
    fig = get_heatmap(participant, visualization)
    return fig

# Heatmap 2
@app.callback(
    Output("heatmap2", "figure"),
    [Input("participant2", "value"), Input("visualization2", "value")]
)
def update_heatmap2(participant, visualization):
    fig = get_heatmap(participant, visualization)
    return fig

# Table 2
@app.callback(
    Output("metrics_table2", "data"),
    [Input("participant2", "value"), Input("visualization2", "value")]
)
def update_table2(participant, visualization):
    table_updated2 = all[(all["ID"] == participant) & (all["Visualization"] == visualization)].to_dict("records")
    return table_updated2

# Time vs Task Graph
@app.callback(
    Output(component_id='time_task', component_property='figure'),
    [Input("quantile-dropdown", "value"), Input("visualization-dropdown","value"), Input("domain-dropdown","value")]
)
def update_graph(quantile, visualization, domain):
    data = filter_data(quantile, visualization, domain)

    fig = px.scatter(data, x='Time_On_Task', y='Task_Success',
                       labels={'Task_Success': 'Task Success (%)','Time_On_Task':'Time on task (min)'},
                       title=f'Task Success vs Times on Task for {quantile}', 
                       trendline="ols",trendline_color_override="red")
    return fig

# Success distribution
@app.callback(
    Output(component_id='dist_success', component_property='figure'),
    [Input("quantile-dropdown", "value"), Input("visualization-dropdown","value"), Input("domain-dropdown","value")]
)
def update_graph(quantile, visualization, domain):
    data = filter_data(quantile, visualization, domain)
    
    fig = px.histogram(data, 'Task_Success',
                        title=f'Success distribution for {quantile}')
    fig.update_layout(
    xaxis_title="Task Success",
    yaxis_title="Count")

    return fig

# Heatmap Group
@app.callback(
    Output("heatmap_group", "figure"),
    [Input("quantile-dropdown", "value"), Input("visualization-dropdown","value"), Input("domain-dropdown","value")]
)
def update_heatmap_group(quantile, visualization, domain):
    data = filter_data(quantile, visualization, domain)

    fig = get_heatmap_group(data)
    fig.update_layout(title=f"Fixation Heatmap for {quantile}")
    
    return fig

# Table 1
@app.callback(
    Output("group_table", "data"),
    [Input("quantile-dropdown", "value"), Input("visualization-dropdown","value"), Input("domain-dropdown","value")]
)
def update_table_group(quantile, visualization, domain):
    data = filter_data(quantile, visualization, domain)
    mean_row = data.mean(numeric_only=True).to_frame(name="Mean").T
    mean_row['ID'] = 'Mean'
    mean_row['Task_Success'] = mean_row['Task_Success'].round(2)
    mean_row['Percentage'] = mean_row['Task_Success'].astype(str) + ' %'
    data = pd.concat([data,mean_row])

    table_updated = data.to_dict("records")
    return table_updated


app.run_server(debug=True)