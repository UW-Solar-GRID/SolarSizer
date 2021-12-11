"""

Creates GUI with functionality to input latitude, longitude, and a csv file.

These user inputted values are run through the PySAM model.

"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#import datetime

import dash
from dash.dependencies import Input, Output, State
from dash import callback_context, dcc, html
#import plotly.express as px
import pandas as pd

import urllib.request
import os

from pysam import pysam_model
from utils import parse_load_profile as plp
from utils import pull_irradiance
from utils import convert_load_profile

global_lat = None
global_lon = None
global_list_of_contents = None

app = dash.Dash(__name__)

colors = {
    'background': '#777777',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello, welcome to solarGRID',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='A web application for assisting with solar projects', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Br(),

    html.Label('Enter latitude and longitude below:', style={'color': colors['text']

    }),

    html.Br(),

    html.Br(),

    html.Label('Latitude (in degrees):', style={'color': colors['text']

    }),

    dcc.Input(id='lat', type='number'),

    html.Br(),

    html.Label('Longitude (in degrees):', style={'color': colors['text']

    }),

    dcc.Input(id='lon', type='number'),

    html.Br(),

    html.Br(),

    html.Div(id="output"),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    
    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),

    html.Div(id='container-button-timestamp')

#    html.Label('Upload a load profile below:', style={'color': colors['text']
#
#    }),
#
#
#    dcc.Upload(
#        id='upload-csv',
#        children=html.Div([
#            'Drag and Drop or ',
#            html.A('Select csv Files')
#        ]),
#        style={
#            'width': '100%',
#            'height': '60px',
#            'lineHeight': '60px',
#            'borderWidth': '1px',
#            'borderStyle': 'dashed',
#            'borderRadius': '5px',
#            'textAlign': 'center',
#            'margin': '10px'
#        },
#        # Allow multiple files to be uploaded
#        multiple=True
#    ),
#    html.Div(id='output-csv-upload'),
])

#def parse_contents(contents, filename, date):
#    return html.Div([
#        html.H5(filename),
#        html.H6(datetime.datetime.fromtimestamp(date)),
#        html.Hr(),
#        html.Div('Raw Content'),
#        html.Pre(contents[0:200] + '...', style={
#            'whiteSpace': 'pre-wrap',
#            'wordBreak': 'break-all'
#        })
#    ])
#
#@app.callback(Output('output-csv-upload', 'children'),
#              Input('upload-csv', 'contents'),
#              State('upload-csv', 'filename'),
#              State('upload-csv', 'last_modified'))
#def update_output(list_of_contents, list_of_names, list_of_dates):
#    if list_of_contents is not None:
#        children = [
#            parse_contents(c, n, d) for c, n, d in
#            zip(list_of_contents, list_of_names, list_of_dates)]
#        return children


@app.callback(Output('output', 'children'),
              Input('lat', 'value'),
              Input('lon', 'value'))

def update_output(lat, lon):
    """
    Updates output with input values run through FakeSAM model.
    """

    if lat is not None and lon is not None:
        global_lat = lat
        global_lon = lon
        print('global_lat', global_lat)
        print('global_lon', global_lon)
        
        pull_irradiance.create_irradiance_file(lat,lon,2000) # may want to turn this off when testing because will max out request from API rate. Also might want to see about using average irradiance from NREL instead of from a set year.

    else:
        pass


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def load_profile_update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        
        global_list_of_contents = list_of_contents
#        children = [
#            plp.parse_contents(c, n, d) for c, n, d in
#            zip(list_of_contents, list_of_names, list_of_dates)]
        
        [convert_load_profile.create_load_txt(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
#        return children


@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        print('button clicked')
        msg = 'Button 1 was most recently clicked'
        
        model_output = pysam_model.pysam_model()
        print(model_output)

# Tried to write this so the button only calls the model when the inputs are entered but it doesn't work, will at some point replace call to model above
#        print('global_lat', global_lat)
#        print('global_lon', global_lon)
#        print('global_list_of_contents', global_list_of_contents)
#        if global_lat is not None and global_lon is not None and global_list_of_contents is not None:
#            
#            model_output = pysam_model.pysam_model()
#            print(model_output)
#        else:
#            print('You need to input lat, lon, and a load profile first')
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg)
                
if __name__ == '__main__':
    app.run_server(debug=True)
