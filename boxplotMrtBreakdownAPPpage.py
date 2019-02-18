import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from datetime import timedelta
import urllib.request
import json
import numpy as np

# to fetch api from Here.com
urlBase = 'https://route.api.here.com/routing/7.2/calculateroute.json?app_id=CqnyNhJQRmXS5JggWAos&app_code=qsE9fGn1RRAPNOxzG1OeFA&waypoint0=geo!{}&waypoint1=geo!{}&mode=fastest;car;traffic:disabled'


#Mapbox api
MAPBOX_TOKEN = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



df = pd.read_csv('countLongLatName.csv', sep=',',encoding = 'utf8')
#print(len(df['Postal']))

dfNSL = df[df['Line']=="NSL"]
dfEWL = df[df['Line']=="EWL"]
dfCGL = df[df['Line']=="CGL"]
dfNEL = df[df['Line']=="NEL"]
dfDTL = df[df['Line']=="DTL"]
dfCCL = df[df['Line']=="CCL"]

# append CGL back to NEL since it is part of NEL
dfEWL =dfEWL.append(dfCGL)

# add styles
# define styles
styleCenter={
    'textAlign': 'center',
}

styleCenterAndColor={
    'textAlign': 'center',
    'color': '#ff0000',
    'font-weight': 'bold',
    'font-size': '150%',
}



# the boxplot outline cant change colour even tho the box changed colour.
# hence move the names to suit the colours
x_data = ['DTL', 'CCL',
          'EWL', 'NSL',
          'NEL',]



y_data = [
            dfDTL['Count'].tolist(),
            dfCCL['Count'].tolist(),
            dfEWL['Count'].tolist(),
            dfNSL['Count'].tolist(),
            dfNEL['Count'].tolist(),
            
        ]

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

traces = []

for xd, yd, cls in zip(x_data, y_data, colors):
        traces.append(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker=dict(
                size=2,
            ),
            line=dict(width=1),
        ))

layout = go.Layout(
    title='MRT breakdown Frequencies',
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=True
)
#fig = go.Figure(data=data, layout=layout)

#py.iplot(fig)






applayout = html.Div([
    html.H1('Frequency of MRT breakdowns Sep 2012 - Apr 2018',style = styleCenter),
    html.Div('Api from Twitter @SMRT_Singapore', style = styleCenter),

    html.Div(id='text-content'),
    dcc.Graph(
        id='boxplots',
        #layout=layout,
        figure={
            'data':traces,
            'layout':layout,
        },
    ),

    
])



if __name__ == '__main__':
    app.run_server(debug=True)



