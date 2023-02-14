from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash


layout = html.Div([

    html.H1('exemplo', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H1(children="Payment type", style={"fontSize":"150%"}),

        ], className='six columns'),


    ], className='banner'),

])