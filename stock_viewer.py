import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
import pendulum as pen
from datetime import datetime


df = pd.read_csv('NASDAQcompanylist.csv')

app = dash.Dash()

app.title = "Stock Ticker NASDAQ"

server = app.server

app.layout = html.Div([

            html.Div([

                html.H3('An stock viewer made with Dash',
                        style={
                           'font-size': '2.65em',
                           'margin-left': '0px',
                           'font-weight': 'bolder',
                           'font-family': 'Product Sans',
                           'color': "rgba(117, 117, 117, 0.95)",
                           })

            ]),

            html.Div([

                html.H3('Select your favourate stocks:'),
                dcc.Dropdown(id='ticker',

                    options=[{'label':i[1],'value':str(i[0])}
                            for i in zip(df['Symbol'],df['Name'])],
                    value=['AMZN','BIDU'],
                    multi=True)

            ],style={'width':'49%','display':'inline-block','verticalAlign':'top'}),

            html.Div([
                html.H3('Select the start and end dates:'),
                dcc.DatePickerRange(id='date-picker',
                            min_date_allowed= pen.datetime(2017,1,1),
                            max_date_allowed= pen.today(),
                            start_date=pen.datetime(2018, 1, 1),
                            end_date=pen.today(),)

            ],style={'width':'49%','display':'inline-block','marginLeft':10}),


            dcc.Graph(id='stock-graph'),


])

@app.callback(Output('stock-graph','figure'),
            [Input('ticker','value'),
            Input('date-picker','start_date'),
            Input('date-picker','end_date')])

def update_graph(tickers,start,end):
    start = datetime.strptime(start[:10], '%Y-%m-%d')
    # start = start.to_date_string()
    # end = end.to_date_string()
    end = datetime.strptime(end[:10], '%Y-%m-%d')
    traces = []
    for tic in tickers:
        df = web.DataReader(tic,'iex',start,end)
        traces.append(go.Candlestick(
                        x = df.index,
                        open = df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'],
                        name=tic,
                        legendgroup=tic,
                        increasing=dict(line=dict(color= '#17BECF')),
                        decreasing=dict(line=dict(color= '#7F7F7F'))))

    return {
        'data':traces

        }


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':

    app.run_server(debug=True)
#    app.run_server
