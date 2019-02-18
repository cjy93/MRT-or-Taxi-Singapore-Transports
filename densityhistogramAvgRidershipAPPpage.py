import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import taxiDatabase
from datetime import datetime
from datetime import timedelta
import plotly.plotly as py
from dash.dependencies import Input, Output
import numpy as np


# define styles
styleCenter={
    'textAlign': 'center',
}

MAPBOX_TOKEN = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

print("before")
db = taxiDatabase.TaxiDatabase()
print("after")

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

applayout = html.Div([
    html.H1('Density and Histogram plot of Location of Taxi across time', style = styleCenter),
    html.Div(id='text-content'),
    dcc.Graph(id='map'),
    
    
    
    html.Div(id='div-currentViewingTime'),
    
    html.Div(id='div-rangeSliderContainer',
        children=['Select range of dates',
        dcc.RangeSlider(
            id='rangeSlider-date',
            min=0,
            max=maxDateId,
            step=1,
            value=[0,min(2, maxDateId)], # default range 0:2 (or min dateId)
                                     # cater to test where there's only 1 date
            marks=datasetDisplayDate,
        )]
    ),
    
    html.Br(),
    
    dcc.Slider(
        id='slider-taxiSummaryId',
        min=taxiSummaryIdMin,         # initialization
        max=taxiSummaryIdMax,         # initialization
        #marks={i: '{}'.format(dfTaxiSummary.ltaTimestamp[i]) 
        #    for i in #range(taxiSummaryIdMin,taxiSummaryIdMax,180)}, # every 3hr
        value=5,
        included=False
    ),
    html.Br(),


    
])


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('slider-taxiSummaryId', 'value'),
    dash.dependencies.Input('map', 'hoverData') ])
def update_map(slider_taxiSummaryId, hoverData):
    """ Update map 
    Data to display: 
    0: MRT Station
    1: taxi locations based on current time
    """
    #print(figure.keys())
    #layout = go.Layout(
    #        mapbox= {
    #            'accesstoken': MAPBOX_TOKEN,
    #            'center': {'lat': 1.353869, 'lon':103.817780},
    #            'zoom': 10.5,
    #
    #        },
    #       hovermode = 'closest',
    #       margin = {'l': 0, 'r': 0, 'b': 0, 't': 0}
    #)
    datasetId = slider_taxiSummaryId
    dfAllTaxi = db.selectTaxiDetailsWhereDatasetId(datasetId)
    
    # plot using 2D histogram contour
    x = dfAllTaxi['long']
    y = dfAllTaxi['lat']
    data = [
        go.Histogram2dContour(
            x = x,
            y = y,
            colorscale = 'Blues',
            reversescale = True,
            xaxis = 'x',
            yaxis = 'y'
        ),
        go.Scatter(
            x = x,
            y = y,
            xaxis = 'x',
            yaxis = 'y',
            mode = 'markers',
            marker = dict(
                color = 'rgba(0,0,0,0.3)',
                size = 3
            )
        ),
        go.Histogram(
            y = y,
            xaxis = 'x2',
            marker = dict(
                color = 'rgba(0,0,0,1)'
            )
        ),
        go.Histogram(
            x = x,
            yaxis = 'y2',
            marker = dict(
                color = 'rgba(0,0,0,1)'
            )
        )
    ]

    layout = go.Layout(
        autosize = False,
        xaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        yaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        xaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False
        ),
        yaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False
        ),
        height = 600,
        width = 1200,
        bargap = 0,
        hovermode = 'closest',
        showlegend = False
    )
    #dfNearestTaxi = db.selectNearestTaxi(1, )
    # dummy df
    
   
    #colorscale = #['rgb(255,0,0)','rgb(255,128,0)','rgb(255,255,0)','rgb(128,255,0)','rgb(0,255,0)','rgb(0,255,255)','rgb(0,128,255)',
    #                'rgb(0,0,255)', 'rgb(127,0,255)','rgb(255,0,255)','rgb(255,255,255)'   ]

    #fig = ff.create_2d_density(
    #    dfAllTaxi['long'], dfAllTaxi['lat'], colorscale=colorscale,
    #    hist_color='rgb(255, 237, 222)', point_size=3
    #)
    # go.figure is dash plot figure
    #return fig
    return go.Figure(
            data=data,
            layout=layout
            )



@app.callback(
    dash.dependencies.Output('div-currentViewingTime', 'children'),
    [dash.dependencies.Input('slider-taxiSummaryId', 'value')])
def update_currentViewingTime(slider_taxiSummaryId):
    #print('update_currentViewingTime {}'.format(slider_taxiSummaryId,))
    # slider_taxiSummaryId starts from 1 (same as mysql table id)
    # but as a list, it starts from 0
    # @TODO: more robust way is to use pandas to match the id 
    # rather than using indexing
    return 'Current viewing time: {} (id:{})'.format(str(
        dfTaxiSummary.ltaTimestamp[slider_taxiSummaryId-1]),
        slider_taxiSummaryId)
        
        




@app.callback(
    dash.dependencies.Output('slider-taxiSummaryId', 'max'),
    [dash.dependencies.Input('rangeSlider-date', 'value')])
def update_sliderBasedOnDate_max(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    maxIdTaxiSummary = max(rangeLtaTime.idtaxisummary)
    return maxIdTaxiSummary # this replaces 'max'
        
        
 
@app.callback(
    dash.dependencies.Output('slider-taxiSummaryId', 'min'),
    [dash.dependencies.Input('rangeSlider-date', 'value')])
def update_sliderBasedOnDate_min(basedOnRangeDate):
    startDate = datasetInternalDate[basedOnRangeDate[0]]
    endDate = datasetInternalDate[basedOnRangeDate[1]]
    startDateLta= datetime.strptime(startDate, '%Y-%m-%d')
    endDateLta = datetime.strptime(endDate, '%Y-%m-%d')
    rangeLtaTime = dfTaxiSummary[(dfTaxiSummary.ltaTimestamp> startDateLta) & (dfTaxiSummary.ltaTimestamp <= endDateLta + timedelta(days=1))]
    
    minIdTaxiSummary = min(rangeLtaTime.idtaxisummary)
    return minIdTaxiSummary # this replaces 'min'
        

@app.callback(
    dash.dependencies.Output('slider-taxiSummaryId', 'marks'),
    [dash.dependencies.Input('rangeSlider-date', 'value')])
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








if __name__ == '__main__':
    app.run_server(debug=True)






