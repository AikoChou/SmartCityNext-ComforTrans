#! -*- coding:utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dtable
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import sqlite3
import datetime as dt
import random

server = Flask('my app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('comforTrans-app', server=server,
                url_base_pathname='/',
                csrf_protect=False)

mapbox_access_token = 'pk.eyJ1IjoiYWlrb2Nob3UiLCJhIjoiY2o1bWF2emI4M2ZoYjJxbnFmbXFrdHQ0ZCJ9.w0_1-IC0JCPukFL7Bpa92w'
DF_ROUTE_TEXT = pd.read_csv('./routes_car.csv')
DF_ROUTE = pd.read_csv('./map_car.csv')
DF_CROWD = pd.read_csv('./crowd_car.csv')
endpt_size = 20
zoom=13

data = Data([
    Scattermapbox(
        lat=DF_ROUTE.lat,
        lon=DF_ROUTE.lon,
        mode='markers+lines',
        marker=Marker(
            size=[endpt_size] + [4 for j in range(len(DF_ROUTE.lon)-2)] + [endpt_size]
        ),
    )
])
layout = Layout(
    height=300,
    margin=Margin(l=10, r=10, t=10, b=20),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        style='streets',
        center=dict(
            lat=np.mean(DF_ROUTE.lat),
            lon=np.mean(DF_ROUTE.lon),
        ),
        pitch=0,
        zoom=zoom
    ),
)

fig = dict(data=data, layout=layout)

crowd_val = [ 90,160,140,100,120,240,300,860,1110,940,400,450,580,400,320,460,590,990,1230,1330,910,580,410,510 ]

trace0 = Bar(
    x=[i for i in range(24)],
    y=crowd_val,
    marker=Marker(
        color='#7F7F7F'
    ),
    opacity=0.6
)

bar_data = [trace0]
bar_layout = Layout(
	title='市民大道四段',
	height=300,
    autosize=True,

    xaxis=dict(
	    range=[-0.5, 23.5], 
	    nticks=25,
        ticksuffix=":00"
    ),

)

bar = dict(data=bar_data, layout=bar_layout)

app.layout = html.Div([

    html.Div([
        html.H2("ComforTrans ʕ•ᴥ•ʔ"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H3("Try ComforTans!")
        ], className='Title'),
        html.Div([
	        html.Button('搭乘大眾運輸', id='button'),
	        html.Button('自行駕駛', id='button', style={'background-color': '#DDDDDD'}),
        	html.Label('目的地 Destination:'),
            dcc.Input(
			    placeholder='Enter destination',
			    type='text',
			    value='台北101'
			),
        ], className='ten columns wind-speed', style={'position': 'relative', 'top': 10}),
        html.Div([
			html.Label('出發時間 Departure time:'),
            dcc.Input(
			    placeholder='Enter Departure time',
			    type='text',
			    value='2017/10/24 12:00'
			),
			html.Button('Go', id='button', style=dict(float='center')),
        ], className='ten columns wind-speed', style={'position': 'relative', 'top': 10, 'bottom': 10}),
    ], className='row wind-speed-row'),
   
    html.Div([
        html.Div([
            html.H3("推薦路線 Recommdation Routes")
        ], className='Title'),

        html.Div([
            dcc.Graph(id='main-graph', figure=fig),
		    dtable.DataTable(
		        rows=DF_ROUTE_TEXT.to_dict('records'),
		        columns=DF_ROUTE_TEXT.columns,
		        row_selectable=True,
		        selected_row_indices=[0],
		        id='datatable-routes'
		    ),
        ], className='twelve columns wind-speed'),
    ], className='row wind-speed-row'),

    html.Div([
        html.Div([
            html.H3("車流壅塞路段 Congested Roads")
        ], className='Title'),
        html.Div([
	        dcc.Graph(id='crowd-histogram', figure=bar),
		    dtable.DataTable(
		        rows=DF_CROWD.to_dict('records'),
		        columns=DF_CROWD.columns,
		        row_selectable=True,
		        selected_row_indices=[0],
		        id='datatable-routes'
		    ),	     
	    ], className='twelve columns wind-speed')

    ], className='row wind-speed-row')
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
	app.run_server(debug=True) #localhost
	#app.run_server(host='0.0.0.0', port=8080, debug=False)