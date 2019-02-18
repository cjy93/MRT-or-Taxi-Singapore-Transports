import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import taxiDatabase
from datetime import datetime
from datetime import timedelta


MAPBOX_TOKEN = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
print("before")
db = taxiDatabase.TaxiDatabase()
print("after")


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



dfMrt = pd.read_csv('mrt_stations.csv')
#dfMrtA = pd.read_csv('mrt_stations_a.csv')
#dfMrtB = pd.read_csv('mrt_stations_b.csv')

## prepare some data
# get the full table of summary
dfTaxiSummary = db.selectAllFromTaxiSummary() # self not needed to type. to pull out database everything
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

styleMargin = {
    'margin' : '100px',
}

applayout = html.Div([
    html.H1('Number of Taxi within 2km of where you are', style = styleCenter),
    html.Div(id='text-content'),
    dcc.Graph(id='mrtStation_map'),
    
    html.Div(id='mrtStation_debug', children='debug area', style= styleCenterAndColor),
    #html.Div(id='mrtStation_debug2', children='debug area'),
    
    html.Div(id='mrtStation_div-currentViewingTime' , style = styleCenter),
    
    # Note html.Div as a container. Here has RangerSlider and words
    html.Div(id='div-rangeSliderContainer',
        children=['Select range of dates',
        dcc.RangeSlider(
            id='mrtStation_rangeSlider-date',
            min=0,
            max=maxDateId,
            step=1,
            value=[0,min(2, maxDateId)], # default range 0:2 (or min dateId)
                                     # cater to test where there's only 1 date
            marks=datasetDisplayDate,
        )] , style = styleCenter
    ),
    
    html.Br(),
    dcc.Slider(
        id='mrtStation_slider-taxiSummaryId',
        min=taxiSummaryIdMin,         # initialization
        max=taxiSummaryIdMax,         # initialization
        #marks={i: '{}'.format(dfTaxiSummary.ltaTimestamp[i]) 
        #    for i in #range(taxiSummaryIdMin,taxiSummaryIdMax,180)}, # every 3hr
        value=5,
        included=False
    ),


    
], style = styleMargin) # styleMargin makes the margins of box adjusted



@app.callback(
    dash.dependencies.Output('mrtStation_map', 'figure'),
    [dash.dependencies.Input('mrtStation_slider-taxiSummaryId', 'value'),
    dash.dependencies.Input('mrtStation_map', 'hoverData') ])
def update_map(slider_taxiSummaryId, hoverData):
    """ Update map 
    Data to display: 
    0: MRT Station
    1: taxi locations based on current time
    """
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
    datasetId = slider_taxiSummaryId
    #dfAllTaxi = db.selectTaxiDetailsWhereDatasetId(datasetId)
    #dfNearestTaxi = db.selectNearestTaxi(1, )
    # dummy df
    dfNearestTaxi = pd.DataFrame(data = [(0,0,0)], 
            columns=('lat', 'long', 'idtaxidetails'))
    dfNearestTaxiDummy = dfNearestTaxi
    if hoverData is not None:
        if hoverData['points'][0]['curveNumber'] == 0:
        # hover on mrt station 
        # count nearest taxi

            searchRadiusKm = 2
            lat = hoverData['points'][0]['lat']
            lon = hoverData['points'][0]['lon']
            dfNearestTaxi = db.selectNearestTaxi(datasetId,
                    lat, lon, searchRadiusKm)
            if dfNearestTaxi is None:
                dfNearestTaxi = dfNearestTaxiDummy


    # go.figure is dash plot figure
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
                    lat = dfNearestTaxi['lat'],
                    lon = dfNearestTaxi['long'],
                    mode = 'markers',
                    marker = dict(
                        size=8,
                        opacity = 0.6,
                        color='rgb(0,255,0)',
                    ),
                    customdata = dfNearestTaxi['idtaxidetails'],
                    hoverinfo = 'none',
                    hovertext = None,
                    name = 'Nearest Taxi (<=2km)',
                ),
            ],
            layout=layout
    )



@app.callback(
    dash.dependencies.Output('mrtStation_div-currentViewingTime', 'children'),
    [dash.dependencies.Input('mrtStation_slider-taxiSummaryId', 'value')])
def update_currentViewingTime(slider_taxiSummaryId):
    #print('update_currentViewingTime {}'.format(slider_taxiSummaryId,))
    # slider_taxiSummaryId starts from 1 (same as mysql table id)
    # but as a list, it starts from 0
    # @TODO: more robust way is to use pandas to match the id 
    # rather than using indexing
    return 'Current viewing time: {} (id:{})'.format(str(
        dfTaxiSummary.ltaTimestamp[slider_taxiSummaryId-1]),
        slider_taxiSummaryId)
        
"""        
@app.callback(
    dash.dependencies.Output('mrtStation_debug2', 'children'),
    [dash.dependencies.Input('mrtStation_rangeSlider-date', 'value')])
def update_sliderBasedOnDate(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    # Min and Max of the range index    
    minIdTaxiSummary = min(rangeLtaTime.idtaxisummary)
    maxIdTaxiSummary = max(rangeLtaTime.idtaxisummary)

    
    #print(rangeLtaTime)
    return "basedOnrangeDATE{}, startDate {} ,endDate {}, ltaTimeStamp {}".\
        format(basedOnRangeDate, startDate ,endDate, rangeLtaTime.ltaTimestamp)
"""


@app.callback(
    dash.dependencies.Output('mrtStation_slider-taxiSummaryId', 'max'),
    [dash.dependencies.Input('mrtStation_rangeSlider-date', 'value')])
def update_sliderBasedOnDate_max(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    maxIdTaxiSummary = max(rangeLtaTime.idtaxisummary)
    return maxIdTaxiSummary # this replaces 'max'
        
        
 
@app.callback(
    dash.dependencies.Output('mrtStation_slider-taxiSummaryId', 'min'),
    [dash.dependencies.Input('mrtStation_rangeSlider-date', 'value')])
def update_sliderBasedOnDate_min(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    minIdTaxiSummary = min(rangeLtaTime.idtaxisummary)
    return minIdTaxiSummary # this replaces 'min'
        

@app.callback(
    dash.dependencies.Output('mrtStation_slider-taxiSummaryId', 'marks'),
    [dash.dependencies.Input('mrtStation_rangeSlider-date', 'value')])
def update_sliderBasedOnDate_marks(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    minIdTaxiSummary = min(rangeLtaTime.idtaxisummary)
    maxIdTaxiSummary = max(rangeLtaTime.idtaxisummary)
    marksTaxiSummary ={i: '{}'.format(dfTaxiSummary.ltaTimestamp[i].strftime('%m-%d %H-%M') ) 
            for i in range(minIdTaxiSummary,maxIdTaxiSummary+1,180)}, # every 3hr
    print("marksTaxiSummary", marksTaxiSummary[0])
    
    return marksTaxiSummary[0] # this replaces 'marks' and also make away tuples





@app.callback(
    dash.dependencies.Output('mrtStation_debug', 'children'),
    [dash.dependencies.Input('mrtStation_map', 'hoverData'),
    dash.dependencies.Input('mrtStation_slider-taxiSummaryId', 'value'),
    dash.dependencies.Input('mrtStation_rangeSlider-date', 'value')])
def update_text(hoverData, slider_taxiSummaryId, sliderDateIdList):
    if hoverData is None:
        print('update_text NONE')
        return
    print('update_text: {}'.format(str(hoverData)))
    #s = df[df['station'] == hoverData['points'][0]['customdata']]
    #print(hoverData)

    
    # to test mrtStation_rangeSlider-date
    #if True:
    #    sliderDateTxt = [datasetInternalDate[x] for x in sliderDateIdList]
    #    return 'sliderId: {}'.format(sliderDateTxt,)


    # by inspecting the console, when hover over mrt the curvenumber is 0, taxi is 1
    if hoverData['points'][0]['curveNumber'] == 0:  
        # hover on mrt station 
        # count nearest taxi
        datasetId = slider_taxiSummaryId

        stnName = hoverData['points'][0]['customdata']
        searchRadiusKm = 2
        lat = hoverData['points'][0]['lat']
        lon = hoverData['points'][0]['lon']
        df = db.selectNearestTaxi(datasetId, lat, lon, searchRadiusKm)
        countNearbyTaxi = df.shape[0]
        #return "Taxi withinlat:{}, long:{}, nearbyTaxi (2km):{}". \
        #      format(lat, lon, 
        #    countNearbyTaxi)
        return "{}. {} taxis with {}km. lat:{:.3f}, long:{:.3f}".format(stnName, 
            countNearbyTaxi, searchRadiusKm, lat, lon)


if __name__ == '__main__':
    app.run_server(debug=True)






