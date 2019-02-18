import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import taxiDatabase
from datetime import datetime
from datetime import timedelta
import urllib.request
import json

# to fetch api from Here.com
urlBase = 'https://route.api.here.com/routing/7.2/calculateroute.json?app_id=CqnyNhJQRmXS5JggWAos&app_code=qsE9fGn1RRAPNOxzG1OeFA&waypoint0=geo!{}&waypoint1=geo!{}&mode=fastest;car;traffic:disabled'


#Mapbox api
MAPBOX_TOKEN = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# define styles
styleCenter={
    'textAlign': 'center',
}
styleCenterAndColor={
    'textAlign': 'center',
    'color': '#ff0000',
    'font-weight': 'bold',
    'font-size': '120%',
}


from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
print("before")
db = taxiDatabase.TaxiDatabase()  # assign the taxiDatabase file with db
print("after")

dfMrt = pd.read_csv('mrt_stations.csv')
#dfMrtA = pd.read_csv('mrt_stations_a.csv')
#dfMrtB = pd.read_csv('mrt_stations_b.csv')

## prepare some data
# get the full table of summary
dfTaxiSummary = db.selectAllFromTaxiSummary()
taxiSummaryIdMin = min(dfTaxiSummary.idtaxisummary)
taxiSummaryIdMax = max(dfTaxiSummary.idtaxisummary)

"""
https://www.peterbe.com/plog/fastest-way-to-uniquify-a-list-in-python-3.6
https://twitter.com/raymondh/status/944125570534621185
A fast way to sort list and maintain its order.
For python >= 3.7 
"""
def sortOrderedList(inputList):
    return list(dict.fromkeys(inputList))
    
def getUniqueDates():
    displayDate = [x.strftime('%a %d-%b') for x in dfTaxiSummary.ltaTimestamp]
    internalDate = [x.strftime('%Y-%m-%d') for x in dfTaxiSummary.ltaTimestamp]
    
    uniDisplayDate = sortOrderedList(displayDate)
    uniInternalDate = sortOrderedList(internalDate)

    internalId = list(range(0, len(uniDisplayDate)))
    
    return internalId, uniDisplayDate, uniInternalDate

datasetDateId, datasetDisplayDate, datasetInternalDate = getUniqueDates()
print(datasetDateId ,datasetDisplayDate,datasetInternalDate)
maxDateId = max(datasetDateId)

applayout = html.Div([
    html.H1('Shortest travelling distance between any 2 locations', style= styleCenter),
    html.Div('Api from Here.com and Mapbox.com'),

    html.Div(id='text-content'),
    dcc.Graph(id='taxi2pts_map'),
    
    
    
    html.Div(id='taxi2pts_debug', children='debug area', style = styleCenterAndColor),
    html.Div(id='taxi2pts_debug2', children='debug area'),
    html.Div([
        html.Div([
            html.Label('From:'),
            dcc.Input(id='input-from', type='text'),
        ], className='six columns'),
        html.Div([
            html.Label('To:'),
            dcc.Input(id='input-to', type='text'),
        ], className='six columns'),
        
    ]),
    html.Div(id='output-container-button',
                 children='Enter a value and press submit'),
    html.Button('Submit', id='button'),   
 
    html.Div(id='div-currentViewingTime'),


    
])


@app.callback(
    dash.dependencies.Output('taxi2pts_debug', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-from', 'value'),
     dash.dependencies.State('input-to', 'value')])
def update_output(n_clicks, inputFrom, inputTo):
    dfPostalFr = db.selectBuildingDetailsFrPostal(inputFrom)
    dfPostalTo = db.selectBuildingDetailsFrPostal(inputTo)
    
    if len(dfPostalFr) > 0 and len(dfPostalTo)>0:
        latlong1 = str(dfPostalFr.lat[0])+ "," + str(dfPostalFr.long[0]) # [0] since there may be multiple records for same PC
        latlong2 = str(dfPostalTo.lat[0])+ "," + str(dfPostalTo.long[0])
        url = urlBase.format(latlong1, latlong2)

        req = urllib.request.Request(url)

        ##parsing response
        r = urllib.request.urlopen(req).read()  # download
        cont = json.loads(r.decode('utf-8'))  # parse as json so can use dictionaries to access data
        
        # shortest travelling time
        dist = cont['response']['route'][0]['summary']['distance']
        timeWTrafficSec = cont['response']['route'][0]['summary']['trafficTime']
        timeWTrafficMins = timeWTrafficSec / 60.0
        # pretty print json
        print(json.dumps(cont, indent=4, sort_keys=True))
        
        # list of lat and long across all the routes we take in 2 points
        listLatitude = []
        listLongitude = []
        for segment in cont['response']['route'][0]['leg'][0]['maneuver']:
            lat = segment['position']['latitude']
            long = segment['position']['longitude']
            listLatitude.append(lat)
            listLongitude.append(long)
        
    else :
        return("Please enter a valid postal code")
        
        
    
    #print(dfPostalFr, dfPostalTo)
    return """
    Distance travelled is {}km. Time Taken (with traffic) is {:.2f}mins """.format(
        dist/1000,
        timeWTrafficMins
    )
    

@app.callback(
    dash.dependencies.Output('taxi2pts_map', 'figure'),
    [    dash.dependencies.Input('taxi2pts_map', 'hoverData'),
    dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-from', 'value'),
     dash.dependencies.State('input-to', 'value')])
    
def update_map(hoverData, n_clicks, inputFrom, inputTo):
    """ Update map 
    Data to display: 
    0: MRT Station
    1: taxi locations based on current time
    """
    # copy from top. Change lat long should also change map
    dfPostalFr = db.selectBuildingDetailsFrPostal(inputFrom)
    dfPostalTo = db.selectBuildingDetailsFrPostal(inputTo)
    
    
    listLatitude = []
    listLongitude = []
    
    if len(dfPostalFr) > 0 and len(dfPostalTo)>0:
        latlong1 = str(dfPostalFr.lat[0])+ "," + str(dfPostalFr.long[0]) # [0] since there may be multiple records for same PC
        latlong2 = str(dfPostalTo.lat[0])+ "," + str(dfPostalTo.long[0])
        url = urlBase.format(latlong1, latlong2)

        req = urllib.request.Request(url)

        ##parsing response
        r = urllib.request.urlopen(req).read()  # download
        cont = json.loads(r.decode('utf-8'))  # parse as json so can use dictionaries to access data
        
        # shortest travelling time
        dist = cont['response']['route'][0]['summary']['distance']
        timeWTrafficSec = cont['response']['route'][0]['summary']['trafficTime']
        timeWTrafficMins = timeWTrafficSec / 60.0
        # pretty print json
        print(json.dumps(cont, indent=4, sort_keys=True))
        
        # list of lat and long across all the routes we take in 2 points
        
        for segment in cont['response']['route'][0]['leg'][0]['maneuver']:
            lat = segment['position']['latitude']
            long = segment['position']['longitude']
            listLatitude.append(lat)
            listLongitude.append(long)
    #print(figure.keys())
    layout = go.Layout(
            mapbox= {
                'accesstoken': MAPBOX_TOKEN,
                'center': {'lat': 1.353869, 'lon':103.817780},
                'zoom': 10.5,

            },
            hovermode = 'closest',
            margin = {'l': 0, 'r': 0, 'b': 0, 't': 0}
    )




    return go.Figure(
            data=[
                go.Scattermapbox(
                    lat = dfMrt['latitude'],
                    lon = dfMrt['Longtitude'],
                    mode = 'markers',
                    marker = dict(
                        size=8,
                        opacity = 0.6,
                        color='rgb(255,0,0)',
                    ),
                    customdata = dfMrt['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfMrt['Station Name'],
                    name = 'Mrt Station',
                ),
                go.Scattermapbox(
                    lat = listLatitude,
                    lon = listLongitude,
                    mode = 'markers+lines',
                    marker = dict(
                        size=8,
                        opacity = 0.6,
                        color='rgb(0,255,0)',
                    ),
                    
                    hoverinfo = 'none', 
                    #hovertext = dfMrt['Station Name'],
                    name = 'Shortest Travelling Time Route',
                ),


            ],
            layout=layout
    )






 








if __name__ == '__main__':
    app.run_server(debug=True)






