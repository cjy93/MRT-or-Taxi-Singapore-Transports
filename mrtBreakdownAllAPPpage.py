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


# one for map and another for calculation of percentage
dfAllMrt = pd.read_csv('countLongLatName.csv', sep=',',encoding = 'utf8')
df = pd.read_csv('countLongLatNameNoCGL.csv', sep=',',encoding = 'utf8')


# list of all lines
listlines = ['NSL','EWL','DTL','NEL','CCL']

# dictionary of total break down per line
dictbreakdownPerline = {}
for lines in listlines:
    dfCheckline = df[df['Line'] == lines]
    sumPerLine = sum(dfCheckline['Count'])
    print(lines, sumPerLine)
    dictbreakdownPerline[lines] = sumPerLine  # new method to do dictionaries
print(dictbreakdownPerline)  # verified against excel is correct

# new column add to df called " Name_Count"
dfcount =[]
listPercent = []
for row in range(0, len(df['Line'])):
    listPercent.append((df['Count'][row]/dictbreakdownPerline[df['Line'][row]])*100)
    #print(listPercent)
    concat = "{}, number of breakdowns:{}".format(df['Station Name'][row], df['Count'][row])
    dfcount.append(concat)
#print(dfcount)
df['Name_Count'] = dfcount
df['Percentage'] = listPercent
print(max(df['Percentage']))


# MRT dataset NSL
dfNSL = df[df['Line']=="NSL"]
# MRT dataset EWL
dfEWL = df[df['Line']=="EWL"]
# MRT dataset DTL
dfDTL = df[df['Line']=="DTL"]
# MRT dataset NEL
dfNEL = df[df['Line']=="NEL"]
# MRT dataset CCL
dfCCL = df[df['Line']=="CCL"]
# MRT dataset CGL 
dfCGL = df[df['Line']=="CGL"]


# max percentage break down
maxBreakdownPercent = int(max(df['Percentage'])+0.5)

# add styles to align center
styleCenter={
    'textAlign': 'center',
}
styleCenterAndColor={
    'textAlign': 'center',
    'color': '#ff0000',
    'font-weight': 'bold',
    'font-size': '120%',
}

# percentage of breakdown
dfPercent = sum(dfAllMrt['Count'])



applayout = html.Div([
    html.H1('MRT breakdown Bubble Chart Overview from Sep 2012 - Apr 2018', style = styleCenter),
    html.Div('Api from Here.com and Mapbox.com and Twitter', style = styleCenter),

    html.Div(id='text-content'),
    dcc.Graph(id='All_map'),   
    
    
    
    html.Div(id='All_debug', children='Frequency of MRT Breakdowns',style= styleCenterAndColor),
    #html.Div(id='debug2', children='debug area'),
 
    html.P('', style= styleCenter),
    html.Div('% is normalised to each MRT line frequency', style= styleCenter),
    html.Br(),
    html.Div(id='div-currentViewingTime' ),
    html.Br(),

# slider

    dcc.Slider(
        id = 'percentageslider',
        min= 0,
        max=maxBreakdownPercent,
        marks={i: '{}%'.format(i) for i in range(maxBreakdownPercent)},
        step=0.05,
        value=0,
    )
    
])

# slider affect debug
@app.callback(
    dash.dependencies.Output('All_debug', 'children'),
    [    dash.dependencies.Input('percentageslider', 'value'), # not used here in callback
    ],
    )
    
    # the following are values from the above id
def updateDebug(percentageSlider):
    return "Please click on the slider. Percentage slider is: {}%".format(percentageSlider)




    

@app.callback(
    dash.dependencies.Output('All_map', 'figure'),
    [   dash.dependencies.Input('All_map', 'hoverData'), # not used here in callback
        dash.dependencies.Input('percentageslider', 'value'),
    ],
    )
    
    # the following are values from the above id
def update_map(hoverData,valueofPercentageSlider):
    """ Update map 
    Data to display: 
    0: MRT Station
    1: taxi locations based on current time
    """
    # Colour gradient scale
    sclRed = [ [0,"rgb(255, 0, 0)"],[0.35,"rgb(230, 12, 12)"],[0.5,"rgb(205, 25, 25)"],\
        [0.6,"rgb(180, 37, 37)"],[0.7,"rgb(155, 50, 50)"],[1,"rgb(131, 63, 63)"] ]



    sclGreen = [ [0,"rgb(95, 223, 67)"],[0.35,"rgb(88, 195, 65)"],[0.5,"rgb(81, 167, 63)"],\
        [0.6,"rgb(74, 139, 62)"],[0.7,"rgb(67, 111, 60)"],[1,"rgb(60, 84, 59)"] ]



    sclPurple = [ [0,"rgb(185, 0, 255)"],[0.35,"rgb(164, 11, 222)"],[0.5,"rgb(143, 23, 190)"],\
        [0.6,"rgb(122, 35, 158)"],[0.7,"rgb(101, 47, 126)"],[1,"rgb(80, 59, 94)"] ]
        
        
        
    sclBlue = [ [0,"rgb(39, 122, 255)"],[0.35,"rgb(44, 112, 224)"],[0.5,"rgb(50, 103, 196)"],\
        [0.6,"rgb(55, 93, 168)"],[0.7,"rgb(61, 84, 140)"],[1,"rgb(67, 75, 112)"] ]    
        
        
        
    sclYellow = [ [0,"rgb(246, 252, 39)"],[0.35,"rgb(222, 227, 45)"],[0.5,"rgb(198, 203, 51)"],\
        [0.6,"rgb(175, 178, 57)"],[0.7,"rgb(151, 154, 63)"],[1,"rgb(128, 130, 69)"] ]  
        
    # layout of the map
    layout = go.Layout(
            mapbox= {
                'accesstoken': MAPBOX_TOKEN,
                'center': {'lat': 1.353869, 'lon':103.817780},
                'zoom': 10.5,
                'style': 'light'

            },
            hovermode = 'closest',
            margin = {'l': 0, 'r': 0, 'b': 0, 't': 20}
    )

    # to subset based on MRT line
    # dfNSL is outside variable, not local variable
    dfNSLper = dfNSL[dfNSL['Percentage']<= valueofPercentageSlider]
    dfEWLper = dfEWL[dfEWL['Percentage']<= valueofPercentageSlider]
    dfNELper = dfNEL[dfNEL['Percentage']<= valueofPercentageSlider]
    dfDTLper = dfDTL[dfDTL['Percentage']<= valueofPercentageSlider]
    dfCCLper = dfCCL[dfCCL['Percentage']<= valueofPercentageSlider]
    






    return go.Figure(
            data=[
            #for NSL 
                go.Scattermapbox(
                    lat = dfNSLper['latitude'],
                    lon = dfNSLper['Longtitude'],
                    mode = 'markers+lines',
                    line = dict(
                        width = 2,
                        color = 'rgb(255,0,0)'
                    ),
                    marker = dict(
                        size= dfNSLper['Count']*0.3,
                        opacity = 0.6,
                        reversescale = True,
                        autocolorscale = False,
                        #color='rgb(255,0,0)',
                        colorscale = sclRed,
                        cmin = dfNSLper['Count'].min(),
                        color = dfNSLper['Count'],
                        cmax = dfNSLper['Count'].max(),
                        #colorbar = dict(
                        #    thickness = 10,
                        #    titleside = "top"
                        #),
                    ),
                    customdata = dfNSLper['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfNSLper['Name_Count'],
                    name = 'NSL Mrt Station',
                ),
                
                # for EWL
                go.Scattermapbox(
                    lat = dfEWLper['latitude'],
                    lon = dfEWLper['Longtitude'],
                    mode = 'markers+lines',
                    line = dict(
                        width = 2,
                        color = 'rgb(0,255,0)'
                    ),
                    marker = dict(
                        size= dfEWLper['Count']*0.3,
                        opacity = 0.6,
                        reversescale = True,
                        autocolorscale = False,
                        #color='rgb(255,0,0)',
                        colorscale = sclGreen,
                        cmin = dfEWLper['Count'].min(),
                        color = dfEWLper['Count'],
                        cmax = dfEWLper['Count'].max(),
                        #colorbar = dict(
                        #    thickness = 10,
                        #    titleside = "top"
                        #),
                    ),
                    customdata = dfEWLper['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfEWLper['Name_Count'],
                    name = 'EWL Mrt Station',
                ),
                
                
                
              
                
                
                
                # for DTL
                go.Scattermapbox(
                    lat = dfDTLper['latitude'],
                    lon = dfDTLper['Longtitude'],
                    mode = 'markers+lines',
                    line = dict(
                        width = 2,
                        color = 'rgb(39,122,252)'
                    ),
                    marker = dict(
                        size= dfDTLper['Count']*0.5,
                        opacity = 0.6,
                        reversescale = True,
                        autocolorscale = False,
                        #color='rgb(255,0,0)',
                        colorscale = sclBlue,
                        cmin = dfDTLper['Count'].min(),
                        color = dfDTLper['Count'],
                        cmax = dfDTLper['Count'].max(),
                        #colorbar = dict(
                        #    thickness = 10,
                        #    titleside = "top"
                        #),
                    ),
                    customdata = dfDTLper['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfDTLper['Name_Count'],
                    name = 'DTL Mrt Station',
                ),
                
                
                
                #for NEL
                go.Scattermapbox(
                    lat = dfNELper['latitude'],
                    lon = dfNELper['Longtitude'],
                    mode = 'markers+lines',
                    line = dict(
                        width = 2,
                        color = 'rgb(185,0,255)'
                    ),
                    marker = dict(
                        size= dfNELper['Count']*0.5,
                        opacity = 0.6,
                        reversescale = True,
                        autocolorscale = False,
                        #color='rgb(255,0,0)',
                        colorscale = sclPurple,
                        cmin = dfNELper['Count'].min(),
                        color = dfNELper['Count'],
                        cmax = dfNELper['Count'].max(),
                        #colorbar = dict(
                        #    thickness = 10,
                        #    titleside = "top"
                        #),
                    ),
                    customdata = dfNELper['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfNELper['Name_Count'],
                    name = 'NEL Mrt Station',
                ),
                
                
                
                # For CCL
                go.Scattermapbox(
                    lat = dfCCLper['latitude'],
                    lon = dfCCLper['Longtitude'],
                    mode = 'markers+lines',
                    line = dict(
                        width = 2,
                        color = 'rgb(246,252,39)'
                    ),
                    marker = dict(
                        size= dfCCLper['Count']*0.5,
                        opacity = 0.6,
                        reversescale = True,
                        autocolorscale = False,
                        #color='rgb(255,0,0)',
                        colorscale = sclYellow,
                        cmin = dfCCLper['Count'].min(),
                        color = dfCCLper['Count'],
                        cmax = dfCCLper['Count'].max(),
                        #colorbar = dict(
                        #    thickness = 10,
                        #    titleside = "top"
                        #),
                    ),
                    customdata = dfCCLper['Station Name'],
                    hoverinfo = 'text', 
                    hovertext = dfCCLper['Name_Count'],
                    name = 'CCL Mrt Station',
                ),


            ],
            layout=layout
    )






if __name__ == '__main__':
    app.run_server(debug=True)






