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
    'font-size': '150%',
}


from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
print("before")
db = taxiDatabase.TaxiDatabase()  # assign the taxiDatabase file with db
print("after")

dfMrt = pd.read_csv('mrt_stations.csv')
dfAddress = pd.read_csv('Concat_Add_PostalCode_distbtw2PtsSubsetted.csv',encoding ='utf8')
# for full range of building details, please use 'Concat_Add_PostalCode_distbtw2Pts.csv' instead


#dfMrtA = pd.read_csv('mrt_stations_a.csv')
#dfMrtB = pd.read_csv('mrt_stations_b.csv')

#print(dfAddress)

# dictionary for options
addressoptions = [{'label':'input location', 'value': 'default'}] # default to be shown 
for index, row in dfAddress.iterrows():
    #print(row)
    optionsdict = {'label': row['address_postalCode'] , 'value' : row ['LongitudeLatitude']}  # lat and long already inside this df. Autocomplete direct from the data file, no need to go thr MYSql
    addressoptions.append(optionsdict)




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

# box margin
styleMargin = {
    'margin' : '100px',
}


applayout = html.Div([
    html.H1('Shortest travelling distance between any 2 locations',style = styleCenter),
    html.Div('Api from Here.com and Mapbox.com'),

    html.Div(id='text-content'),
    dcc.Graph(id='dist2pts_map'),
    
    
    
    html.Div(id='2ptsdropdown_debug', children='debugjhvhjghj area', style = styleCenterAndColor), # the children is initial value
    html.Div(id='2ptsdropdown_debug2', children='debug area'),
    html.Div([
        html.Div([
            html.Label('From:'),
            
            dcc.Dropdown(
                id= 'input-from',
                options= addressoptions,
                value='default'  # value must match so input will come out
            )
            
            
            
        ], className='six columns'),
        html.Div([
            html.Label('To:'),
            
            
            dcc.Dropdown(
                id= 'input-to',
                options= addressoptions,
                value='default'  # value must match so input will come out
            )
            
            
            
        ], className='six columns'),
        
    ]),
    html.Div(id='output-container-button',
                 children='Enter a value and press submit'),
    html.Button('Submit', id='button'),   
 
    html.Div(id='div-currentViewingTime'),


    
] )


# children is like a attribute. there are other arg like "style"
@app.callback(
    dash.dependencies.Output('2ptsdropdown_debug', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-from', 'value'),
     dash.dependencies.State('input-to', 'value')])
     # 2nd to 4th lines are input
def update_output(n_clicks, inputFrom, inputTo):

    
    if inputFrom != 'default' and inputTo != 'default':
        latlong1 = inputFrom.split("_")[1] + "," + inputFrom.split("_")[0] # [0] since there may be multiple records for same PC
        latlong2 = inputTo.split("_")[1] + "," + inputTo.split("_")[0]
        #print(latlong1,latlong2)
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
        return "Distance Travelled is {:.1f}km  \n Time Taken (with traffic) is {:.2f} mins".format(dist/1000,timeWTrafficMins)
        
    else :
        return("Please enter a location")
        
        
    
    #print(inputFrom, inputTo)
    
    #"""
    #The input-from value was "{}", input-to value was "{}" 
    #and the button has been clicked {} times \n
    #distance travelled is {} \n Time Taken (with traffic) is {:.2f} mins """.format(
        #inputFrom,
        #inputTo,
        #n_clicks,
        
    

@app.callback(
    dash.dependencies.Output('dist2pts_map', 'figure'),
    [    dash.dependencies.Input('dist2pts_map', 'hoverData'), # not used here in callback
    dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-from', 'value'),
     dash.dependencies.State('input-to', 'value')])
    
    # the following are values from the above id
def update_map(hoverData, n_clicks, inputFrom, inputTo):
    """ Update map 
    Data to display: 
    0: MRT Station
    1: taxi locations based on current time
    """
    # copy from top. Change lat long should also change map
    
    
    
    listLatitude = []
    listLongitude = []
    
    if inputFrom != 'default' and inputTo != 'default':
        latlong1 = inputFrom.split("_")[1] + "," + inputFrom.split("_")[0] # [0] since there may be multiple records for same PC
        latlong2 = inputTo.split("_")[1] + "," + inputTo.split("_")[0]
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
                        color='rgb(0,0,0)',
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






