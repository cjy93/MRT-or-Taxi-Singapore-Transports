import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import MRTbreakdownCalculator 
import base64
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'jupyterPagesPictures/WordCloudOfSingapore.png' # replace with your own image
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
    html.H1('WordCloud using Machine Learning Techniques on Python', style = styleCenter),
    html.Div('To find out what most Singaporeans like to talk about', style= styleCenter),
    html.Div('Data api from twitter (several accounts)', style= styleCenter),
    html.Div([
        html.Img(width=700, src='data:image/png;base64,{}'.format(encoded_image.decode())),
        html.Br(),
        html.A('Link to the Jupyter python code', href='https://raw.githubusercontent.com/cjy93/MRT-or-Taxi-Singapore-Transports/master/GenerateWordCloud.ipynb'),
    
    ], style = styleCenter),
    html.Div('Api: @govsingapore @leehsienloong @PAPSingapore @PeoplesPowerSG @thereformparty @TPPSG @wpsg', 
    style= styleCenter),


  
])




    




if __name__ == '__main__':
    app.run_server(debug=True) 