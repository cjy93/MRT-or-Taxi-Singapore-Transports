import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import barGraphMRTStationAPPpage
import boxplotMrtBreakdownAPPpage
import CalculatorDelayTimeAPPpage
import densityhistogramAvgRidershipAPPpage
import mrtStationAPPpage
import ScatterplotDashPublicTransportAPPpage
import taxiDistance2ptsDropDownAPPpage
import taxiDistance2ptsAPPpage
import taxiStandCarparkAPPpage
import densityMapIpyWidgetAPPpage
import wordcloudAPPpage
import mrtBreakdownAllAPPpage


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Go to wordcloudAPPpage', href='/wordcloudAPPpage'),
    html.Br(),
    dcc.Link('Go to ScatterplotDashPublicTransportAPPpage', href='/ScatterplotDashPublicTransportAPPpage'),
    html.Br(),
    dcc.Link('Go to boxplotMrtBreakdownAPPpage', href='/boxplotMrtBreakdownAPPpage'),
    html.Br(),
    dcc.Link('Go to barGraphMRTStationAPPpage', href='/barGraphMRTStationAPPpage'),    
    html.Br(),
    dcc.Link('Go to CalculatorDelayTimeAPPpage', href='/CalculatorDelayTimeAPPpage'),
    html.Br(),
    dcc.Link('Go to mrtBreakdownAllAPPpage', href='/mrtBreakdownAllAPPpage'),
    html.Br(),
    dcc.Link('Go to densityhistogramAvgRidershipAPPpage', href='/densityhistogramAvgRidershipAPPpage'),
    html.Br(),
    dcc.Link('Go to densityMapIpyWidgetAPPpage', href='/densityMapIpyWidgetAPPpage'),
    html.Br(),
    dcc.Link('Go to taxi_mrtStationAPPpage', href='/mrtStationAPPpage'),    
    html.Br(),
    dcc.Link('Go to taxiDistance2ptsDropDownAPPpage', href='/taxiDistance2ptsDropDownAPPpage'),
    html.Br(),
    dcc.Link('Go to Alternative-taxiDistance2ptsAPPpage', href='/taxiDistance2ptsAPPpage'),
    html.Br(),
    dcc.Link('Go to taxiStandCarparkAPPpage', href='/taxiStandCarparkAPPpage'),
    
    
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/barGraphMRTStationAPPpage':
         return barGraphMRTStationAPPpage.applayout
    elif pathname == '/boxplotMrtBreakdownAPPpage':
         return boxplotMrtBreakdownAPPpage.applayout
    elif pathname == '/CalculatorDelayTimeAPPpage':
         return CalculatorDelayTimeAPPpage.applayout
    elif pathname == '/densityhistogramAvgRidershipAPPpage':
         return densityhistogramAvgRidershipAPPpage.applayout
    elif pathname == '/mrtStationAPPpage':
         return mrtStationAPPpage.applayout
    elif pathname == '/ScatterplotDashPublicTransportAPPpage':
         return ScatterplotDashPublicTransportAPPpage.applayout
    elif pathname == '/taxiDistance2ptsDropDownAPPpage':
         return taxiDistance2ptsDropDownAPPpage.applayout
    elif pathname == '/taxiDistance2ptsAPPpage':
         return taxiDistance2ptsAPPpage.applayout
    elif pathname == '/taxiStandCarparkAPPpage':
         return taxiStandCarparkAPPpage.applayout
    elif pathname == '/densityMapIpyWidgetAPPpage':
         return densityMapIpyWidgetAPPpage.applayout
    elif pathname == '/wordcloudAPPpage':
         return wordcloudAPPpage.applayout
    elif pathname == '/mrtBreakdownAllAPPpage':
         return mrtBreakdownAllAPPpage.applayout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
