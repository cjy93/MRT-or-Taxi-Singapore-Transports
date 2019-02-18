import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import MRTbreakdownCalculator 
import base64
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'MRT_picture.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Data##################################################
# one for map and another for calculation of percentage
df = pd.read_csv('countLongLatNameNoCGL.csv', sep=',',encoding = 'utf8')


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

# make the Percentage column
# list of all lines
listlines = ['NSL','EWL','DTL','NEL','CCL']

# Count total number of breakdowns across all the stations in our dataframe
totalCount =  sum(df.Count)

# new column add to df called " Name_Count"
dfcount =[]
listPercent = []
for row in range(0, len(df['Line'])):
    listPercent.append((df['Count'][row]/totalCount)*100)
    #print(listPercent)
    concat = "{}, number of breakdowns:{}".format(df['Station Name'][row], df['Count'][row])
    dfcount.append(concat)
#print(dfcount)
df['Name_Count'] = dfcount
df['Percentage'] = listPercent  # percentage of breakdown per station over all breakdowns possible
print(max(df['Percentage']))
########################################################


# App Layout
applayout = html.Div([    
    html.H1('Percentage of MRT delay occurence based on Sep 2012 - Apr 2018 data', style = styleCenter),
    html.Div([
        html.Img(width=500, src='data:image/png;base64,{}'.format(encoded_image.decode())),
    ], style = styleCenter),
    html.Div('Choose MRT Track Line', style= styleCenter),
    dcc.Dropdown(
        id='chooseMRTline',
        options=[
            {'label': 'North South Line', 'value': 'NSL'},
            {'label': 'East West Line', 'value': 'EWL'},
            {'label': 'North East Line', 'value': 'NEL'},
            {'label': 'Downtown Line', 'value': 'DTL'},
            {'label': 'Circle Line', 'value': 'CCL'},
        ],
        value='NSL' # initial value
    ),
    
    html.Div('Choose MRT Station_from', style= styleCenter),
    dcc.Dropdown(
        id='station-from',
       
        value=''
    ),
    
    html.Div('Choose MRT Station_to', style= styleCenter),
    dcc.Dropdown(
        id='station-to',
       
        value=''
    ),
    html.Div(id='output-container', style= styleCenterAndColor)
])




    

@app.callback(
    dash.dependencies.Output('station-from', 'options'),
    [dash.dependencies.Input('chooseMRTline', 'value'),
    ])
def update_optionFrom(chooseMRTline):
    #print(df[df['Line']==chooseMRTline])
    outputOptions = [ {'label':row['Station Name'], 'value':row['Station Name']}  \
                        for index, row in df[df['Line']==chooseMRTline].iterrows()]
    return outputOptions # will replace 'options'
    
@app.callback(
    dash.dependencies.Output('station-to', 'options'),
    [dash.dependencies.Input('chooseMRTline', 'value'), # this is only affected by MRT Line anyway
    ])
def update_optionTo(chooseMRTline):
    #print(df[df['Line']==chooseMRTline])
    outputOptions = [ {'label':row['Station Name'], 'value':row['Station Name']}  \
                        for index, row in df[df['Line']==chooseMRTline].iterrows()]
    return outputOptions # will replace 'options'
    



@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('chooseMRTline', 'value'),
    dash.dependencies.Input('station-from', 'value'),
    dash.dependencies.Input('station-to', 'value')])
def update_output(chooseMRTline, stationFrom, stationTo):
    print('You have selected "{} {} {} "'.format(chooseMRTline, stationFrom, stationTo))
    breakdownPercentage = ''
    try:
        breakdownPercentage = MRTbreakdownCalculator.breakdowncalculator(df, chooseMRTline, stationFrom, stationTo)
    except ValueError:
        print('value error')
    return 'You have selected "MRT Line:{}, From:{}, To:{}" \n Chance of delay: {}%'.format(chooseMRTline, stationFrom, stationTo , breakdownPercentage)



if __name__ == '__main__':
    app.run_server(debug=True)    