import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import MRTbreakdownCalculator 
import base64
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'jupyterPagesPictures/TaxiLocationTimelapse.gif' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Data##################################################
# one for map and another for calculation of percentage
df = pd.read_csv('countLongLatNameNoCGL.csv', sep=',',encoding = 'utf8')


# define styles
styleCenter={
    'textAlign': 'center',
}




# App Layout
applayout = html.Div([    
    html.H1('Density Map done with Ipyleaflet', style = styleCenter),
    html.Div('Contains 21798372 data points over 5 days of collection and put in MySQL', style= styleCenter),
    html.Div('Data api from data.gov.sg', style= styleCenter),
    html.Div([
        html.Img(width=700, src='data:image/png;base64,{}'.format(encoded_image.decode())),
        html.Br(),
        html.A('Link to the Jupyter python code', href='https://raw.githubusercontent.com/cjy93/MRT-or-Taxi-Singapore-Transports/master/DensityMaptaxilatlongColumnOnly.ipynb'),
    
    ], style = styleCenter),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),


  
])




    




if __name__ == '__main__':
    app.run_server(debug=True)    