import plotly.express as px
import pandas as pd
import math
import os
import re

def load_files(participant = 1):
    
    route = f'datasets/p{participant}/p{participant}'
    
    # Load one of the files to create functions
    baseline_cols = ['number', 'time', 'l_screen_x', 'l_screen_y', 'l_cam_x', 'l_cam_y', 'l_distance', 
                'l_pupil', 'l_code', 'r_screen_x', 'r_screen_y', 'r_cam_x', 'r_cam_y', 'r_distance', 
                'r_pupil', 'r_code']

    baseline = pd.read_csv(f'{route}GZD.txt', sep='\t', names = baseline_cols, on_bad_lines='skip')
    
    # Load FXD graph and tree
    fxd_cols = ['number', 'time', 'duration', 'screen_x', 'screen_y']

    fxd_graph = pd.read_csv(f'{route}.graphFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')
    fxd_tree = pd.read_csv(f'{route}.treeFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')

    # Load EVD graph and tree
    evd_cols = ['time', 'event', 'event_key', 'data1', 'data2', 'description']

    evd_graph = pd.read_csv(f'{route}.graphEVD.txt', sep='\t', names = evd_cols, on_bad_lines='skip')
    evd_tree = pd.read_csv(f'{route}.treeEVD.txt', sep='\t', names = evd_cols, on_bad_lines='skip')
    
    # Load GZD graph and tree
    gzd_cols = ['number', 'time', 'l_screen_x', 'l_screen_y', 'l_cam_x', 'l_cam_y', 'l_distance', 
                'l_pupil', 'l_code', 'r_screen_x', 'r_screen_y', 'r_cam_x', 'r_cam_y', 'r_distance', 
                'r_pupil', 'r_code']

    gzd_graph = pd.read_csv(f'{route}.graphGZD.txt', sep='\t', names = gzd_cols, on_bad_lines='skip')
    gzd_tree = pd.read_csv(f'{route}.treeGZD.txt', sep='\t', names = gzd_cols, on_bad_lines='skip')

    return baseline, fxd_graph, fxd_tree, evd_graph, evd_tree, gzd_graph, gzd_tree

# Helper functions 
def distance(row):
    x1, y1 = row['x'], row['y']
    x2, y2 =  row['next_x'], row['next_y']
    dist = math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))
    row['dist'] = dist
    
    return row

def duration(row):
    
    t1, d1 = row['time'], row['duration']
    t2 = row['next_time']
    duration = t2 - (t1+d1)
    row['duration_between_fixations'] = duration
    
    return row 

# Metric functions

## All metrics
def get_metrics_df(row):
    
    participant = ''.join(filter(str.isdigit, row['ID']))
    print(participant)
    
    visualization = row['Visualization']
    
    # Load data for participant
    baseline, fxd_graph, fxd_tree, evd_graph, evd_tree, gzd_graph, gzd_tree = load_files(participant)
    
    # Baseline gaze data
    base_avg_size_left, base_avg_size_right, base_avg_size_both = get_gaze_metrics(baseline)
    # Graph data
    if visualization == 1:
        # Fixations data
        total_fixations, sum_fixation_duration, mean_fixation_duration, std_fixation_duration = get_fixation_metrics(fxd_graph)
        # Saccade length data
        total_saccades, sum_saccade_length, mean_saccade_length, std_saccade_length = get_saccade_length_metrics(fxd_graph)
        # Saccade duration data
        sum_saccade_duration, mean_saccade_duration, std_saccade_duration = get_saccade_durations_metrics(fxd_graph)
        # Event data
        total_left_clicks, mean_time_between_clicks, std_time_between_clicks = get_event_metrics(evd_graph)
        # Gaze data
        avg_size_left, avg_size_right, avg_size_both = get_gaze_metrics(gzd_graph)
    # Tree data
    else:
        # Fixations data
        total_fixations, sum_fixation_duration, mean_fixation_duration, std_fixation_duration = get_fixation_metrics(fxd_tree)
        # Saccade length data
        total_saccades, sum_saccade_length, mean_saccade_length, std_saccade_length = get_saccade_length_metrics(fxd_tree)
        # Saccade duration data
        sum_saccade_duration, mean_saccade_duration, std_saccade_duration = get_saccade_durations_metrics(fxd_tree)
        # Event data
        total_left_clicks, mean_time_between_clicks, std_time_between_clicks = get_event_metrics(evd_tree)
        # Gaze data
        avg_size_left, avg_size_right, avg_size_both = get_gaze_metrics(gzd_tree)
    
    cols = ['base_avg_size_left', 'base_avg_size_right', 
            'base_avg_size_both', 'total_fixations', 'sum_fixation_duration', 
            'mean_fixation_duration', 'std_fixation_duration', 'total_saccades', 
            'sum_saccade_length', 'mean_saccade_length', 'std_saccade_length', 
            'sum_saccade_duration', 'mean_saccade_duration', 'std_saccade_duration', 
            'total_left_clicks', 'mean_time_between_clicks', 'std_time_between_clicks', 
            'avg_size_left', 'avg_size_right', 'avg_size_both']
    
    data = [base_avg_size_left, base_avg_size_right, 
            base_avg_size_both, total_fixations, sum_fixation_duration, 
            mean_fixation_duration, std_fixation_duration, total_saccades, 
            sum_saccade_length, mean_saccade_length, std_saccade_length, sum_saccade_duration, 
            mean_saccade_duration, std_saccade_duration, total_left_clicks, 
            mean_time_between_clicks, std_time_between_clicks, 
            avg_size_left, avg_size_right, avg_size_both]
    
    for i in range(len(cols)):
        row[cols[i]] = data[i]
    
    return row

## Gaze data
def get_gaze_metrics(df):
    
    # A code with 0 indicates the eye tracker was confdident with this data
    # Filtering only records where both pupil sizes are valid
    df = df[(df['l_code'] == 0) & (df['r_code'] == 0)]
    avg_size_left = df["l_pupil"].mean()
    avg_size_right = df["r_pupil"].mean()
    avg_size_both = pd.concat([df["r_pupil"],df["l_pupil"]]).mean()
    
    return avg_size_left, avg_size_right, avg_size_both

## Fixation data
def get_fixation_metrics(df):
    
    total_fixations = len(df)
    sum_fixation_duration_sec = df["duration"].sum() / 1000
    mean_fixation_duration = df["duration"].mean()
    std_fixation_duration = df["duration"].std()
    
    return total_fixations, sum_fixation_duration_sec, mean_fixation_duration, std_fixation_duration
    
def get_saccade_length_metrics(df):
    
    # Get distances of all points
    coords = df[['screen_x','screen_y']].copy()
    coords = coords.rename({'screen_x':'x','screen_y':'y'}, axis='columns')
    coords['next_x'] = coords['x'].shift(-1)
    coords['next_y'] = coords['y'].shift(-1)
    coords = coords.apply(distance, axis=1)
    coords.dropna(inplace=True)
    
    total_saccades = len(coords)
    sum_saccade_length = coords['dist'].sum()
    mean_saccade_length = coords['dist'].mean()
    std_saccade_length = coords['dist'].std()
        
    return total_saccades, sum_saccade_length, mean_saccade_length, std_saccade_length

def get_saccade_durations_metrics(df):
    
    # Get duration of all saccades
    saccadeDetails = df[['time','duration']].copy()
    saccadeDetails['next_time'] = saccadeDetails['time'].shift(-1)
    saccadeDetails['next_duration'] = saccadeDetails['duration'].shift(-1)
    saccadeDetails = saccadeDetails.apply(duration, axis=1)
    saccadeDetails.dropna(inplace=True)
    
    sum_saccade_duration_sec = saccadeDetails['duration_between_fixations'].sum() / 1000
    mean_saccade_duration = saccadeDetails['duration_between_fixations'].mean()
    std_saccade_duration = saccadeDetails['duration_between_fixations'].std()
    
    return sum_saccade_duration_sec, mean_saccade_duration, std_saccade_duration

## Event data
def get_event_metrics(df):
    
    lclicks = df[df['event'] == 'LMouseButton']
    lclicks = lclicks[['time','data1','data2']]
    lclicks['next_time'] = lclicks['time'].shift(-1)
    lclicks['time_between'] = lclicks['next_time'] - lclicks['time']
    lclicks.dropna(inplace=True)

    total_L_clicks = len(lclicks)
    avg_time_between_clicks_sec = lclicks['time_between'].mean() / 1000
    std_time_between_clicks_sec = lclicks['time_between'].std() / 1000
    
    return total_L_clicks, avg_time_between_clicks_sec, std_time_between_clicks_sec

# Extra

def get_participants():
    # Creating the unique list of directories for participants
    subfolders = [f.path for f in os.scandir('./datasets') if f.is_dir()]
    participants = []
    orders = []
    for folder in subfolders:
        participant = re.search(r'(p\d*)', folder).group(1)
        order = re.search(r'p(\d*)', folder).group(1)
        participants.append(participant)
        orders.append(int(order))
        
    # Ordering by participant number
    df = pd.DataFrame({'participant':participants,'order':orders})
    df.sort_values(by="order", inplace=True)
    return df['participant'].tolist()

def get_heatmap(participant, visualization):

    route = f'datasets/{participant}/{participant}'

    fxd_cols = ['number', 'time', 'duration', 'screen_x', 'screen_y']

    if visualization == 'Tree':
        fxd = pd.read_csv(f'{route}.treeFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')
    else:
        fxd = pd.read_csv(f'{route}.graphFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')

    fig = px.density_heatmap(fxd, x="screen_x", y="screen_y", color_continuous_scale="Sunset")
    fig.update_layout(
    title=f"Fixation Heatmap for participant {participant}",
    xaxis_title="X Coordinates",
    yaxis_title="Y Coordinates")

    return fig

def get_heatmap_group(df):

    fxd_cols = ['number', 'time', 'duration', 'screen_x', 'screen_y']

    res = pd.DataFrame(columns=fxd_cols)

    for _, row in df[['ID','Ontologies','Visualization']].iterrows():
        
        route = f'datasets/{row["ID"]}/{row["ID"]}'
        
        if row['Visualization'] == 'Tree':
            fxd = pd.read_csv(f'{route}.treeFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')
        else:
            fxd = pd.read_csv(f'{route}.graphFXD.txt', sep='\t', names = fxd_cols, on_bad_lines='skip')
        
        res = pd.concat([res,fxd])
        
    fig = px.density_heatmap(res, x="screen_x", y="screen_y", color_continuous_scale="Sunset")
    fig.update_layout(
    title=f"Fixation Heatmap for ",
    xaxis_title="X Coordinates",
    yaxis_title="Y Coordinates")

    return fig