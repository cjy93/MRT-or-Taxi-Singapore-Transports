import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import pymongo
from pymongo import MongoClient
import numpy as np

# define styles
styleCenter={
    'textAlign': 'center',
}

styleCenterAndColor={
    'textAlign': 'center',
    'color': '#ff0000',
    'font-weight': 'bold',
    'font-size': '250%',
}


# call out dataset from MongoDB
client = MongoClient()
db = client.publicTransportAvgDist # client.database_name
collection = db.publicAvgDist #db.collection_name

cursor = collection.find({})
# Expand the cursor and construct the DataFrame
df =  pd.DataFrame(list(cursor))
print(df)
#cursorList = list(cursor)  # when you list(cursor), cursor has changed also




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



applayout = html.Div([
    html.H1('ScatterPlot of Average Trip distance by Public Transports', style = styleCenter),
    html.P('Taxi and MRT are 2 top competitors'),
    dcc.Graph(
        id='avg-dist-transport-type',
        figure={
            'data': [
                go.Scatter( #list comprehension method where scatter() is like a method
                    x=df[df['mode'] == i]['year'],
                    y=df[df['mode'] == i]['ave_distance_per_trip'],
                    text=df[df['mode'] == i]['mode'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in ['MRT','LRT','Bus','Taxi']
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Average Trip Distance (Km)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)