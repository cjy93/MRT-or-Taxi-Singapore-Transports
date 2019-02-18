import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('countLongLatNameNoCGL.csv', sep=',',encoding = 'utf8')
#print(len(df['Postal']))



# to get the count per mrt 
listlines = ['NSL','EWL','DTL','NEL','CCL']
dictbreakdownPerline = {}
for lines in listlines:
    dfCheckline = df[df['Line'] == lines]
    sumPerLine = sum(dfCheckline['Count'])
    print(lines, sumPerLine)
    dictbreakdownPerline[lines] = sumPerLine  # new method to do dictionaries
print(dictbreakdownPerline)  # verified against excel is correct

# to get percentage of breakdown
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

# bar graph NSL
dfNSL = df[df['Line']=="NSL"]
dfEWL = df[df['Line']=="EWL"]
dfNEL = df[df['Line']=="NEL"]
dfDTL = df[df['Line']=="DTL"]
dfCCL = df[df['Line']=="CCL"]

# max percentage break down
maxBreakdownPercent = int(max(df['Percentage'])+0.5)


# change df column to list
x = df.Line.tolist()
y = df.Count.tolist()


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

applayout = html.Div([
    html.H1('MRT breakdown fr Sep 2012 - Apr 2018 Normalised by MRT Line', style= styleCenter),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='North South Line', value='tab-1-example'),
        dcc.Tab(label='East West Line', value='tab-2-example'),
        dcc.Tab(label='North East Line', value='tab-3-example'),
        dcc.Tab(label='Downtown Line', value='tab-4-example'),
        dcc.Tab(label='Circle Line', value='tab-5-example'),
    ]),
    html.Div(id='tabs-content-example'),
    
    dcc.Slider(
        id = 'percentageslider',
        min= 0,
        max=maxBreakdownPercent,
        marks={i: '{}%'.format(i) for i in range(maxBreakdownPercent)},
        step=0.05,
        value= maxBreakdownPercent,
    )
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value'),
               Input('percentageslider', 'value')])
def render_content(tab , sliderpercent):

    # Tab 1: NSL    
    dfNSLsubset = dfNSL[dfNSL['Percentage']<= sliderpercent]
    xNSL = dfNSLsubset['Station Name'].tolist()
    yNSL = dfNSLsubset['Count'].tolist()
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('NSL count of breakdowns'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': xNSL,
                        'y': yNSL,
                        'type': 'bar',
                        'marker':{
                            "color":'rgba(255,0,0,0.5)',
                            "line":{
                                "color":'rgb(153,0,0)',
                                "width":1.5,
                            }
                        }
                    }]
                }
            ),
            html.Div("Count of breakdown for NSL is:", style=styleCenter),
            html.Div("{}".format(dictbreakdownPerline['NSL']), style=styleCenterAndColor),
            html.P("Slider is at {}%".format(sliderpercent), style=styleCenter),
        ])
    # Tab 2 : EWL
    dfEWLsubset = dfEWL[dfEWL['Percentage']<= sliderpercent]
    xEWL = dfEWLsubset['Station Name'].tolist()
    yEWL = dfEWLsubset['Count'].tolist()
    if tab == 'tab-2-example':
        return html.Div([
            html.H3('EWL count of breakdowns'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': xEWL,
                        'y': yEWL,
                        'type': 'bar',
                        'marker':{
                            "color":'rgba(0,153,76,0.5)',
                            "line":{
                                "color":'rgb(0,102,51)',
                                "width":1.5,
                            }
                        }
                    }]
                }
            ),
            html.Div("Count of breakdown for EWL is:", style=styleCenter),
            html.Div("{}".format(dictbreakdownPerline['EWL']), style=styleCenterAndColor),
            html.P("Slider is at {}%".format(sliderpercent), style=styleCenter),
        ])
        
        
    # Tab 3 : NEL
    dfNELsubset = dfNEL[dfNEL['Percentage']<= sliderpercent]
    xNEL = dfNELsubset['Station Name'].tolist()
    yNEL = dfNELsubset['Count'].tolist()
    if tab == 'tab-3-example':
        return html.Div([
            html.H3('NEL count of breakdowns'),
            dcc.Graph(
                id='graph-3-tabs',
                figure={
                    'data': [{
                        'x': xNEL,
                        'y': yNEL,
                        'type': 'bar',
                        'marker':{
                            "color":'rgba(153,51,255,0.5)',
                            "line":{
                                "color":'rgb(76,0,153)',
                                "width":1.5,
                            }
                        }
                    }]
                }
            ),
            html.Div("Count of breakdown for NEL is:", style=styleCenter),
            html.Div("{}".format(dictbreakdownPerline['NEL']), style=styleCenterAndColor),
            html.P("Slider is at {}%".format(sliderpercent), style=styleCenter),
        ])


    # Tab 4 : DTL
    dfDTLsubset = dfDTL[dfDTL['Percentage']<= sliderpercent]
    xDTL = dfDTLsubset['Station Name'].tolist()
    yDTL = dfDTLsubset['Count'].tolist()
    
    if tab == 'tab-4-example':
        return html.Div([
            html.H3('DTL count of breakdowns'),
            dcc.Graph(
                id='graph-4-tabs',
                figure={
                    'data': [{
                        'x': xDTL,
                        'y': yDTL,
                        'type': 'bar',  
                        'marker':{
                            "color":'rgba(0,102,204,0.5)',
                            "line":{
                                "color":'rgba(0,0,204,0.5)',
                                "width":1.5,
                            }
                        }
                        
                    }]
                }
            ),
            html.Div("Count of breakdown for DTL is:", style=styleCenter),
            html.Div("{}".format(dictbreakdownPerline['DTL']), style=styleCenterAndColor),
            html.P("Slider is at {}%".format(sliderpercent), style=styleCenter),
        ])


    # Tab 5 : CCL
    dfCCLsubset = dfCCL[dfCCL['Percentage']<= sliderpercent]
    xCCL = dfCCLsubset['Station Name'].tolist()
    yCCL = dfCCLsubset['Count'].tolist()
    if tab == 'tab-5-example':
        return html.Div([
            html.H3('CCL count of breakdowns'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': xCCL,
                        'y': yCCL,
                        'type': 'bar',
                        'marker':{
                            "color":'rgba(255,255,102,0.5)',
                            "line":{
                                "color":'rgb(255,128,0)',
                                "width":1.5,
                            }
                        }
                    }]
                }
            ),
            html.Div("Count of breakdown for CCL is:", style=styleCenter),
            html.Div("{}".format(dictbreakdownPerline['CCL']), style=styleCenterAndColor),
            html.P("Slider is at {}%".format(sliderpercent), style=styleCenter),
        ])



if __name__ == '__main__':
    app.run_server(debug=True)