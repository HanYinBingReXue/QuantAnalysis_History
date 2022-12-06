import plotly.graph_objects as go
import pandas as pd
import gate_api
import time
from config import *
from pprint import pprint
from datetime import datetime
from plotly.subplots import make_subplots

df = []


def logged_in():

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.
    configuration = gate_api.Configuration(
        host = "https://api.gateio.ws/api/v4",
        key = Gate_API1_Public_Key,
        secret = Gate_API1_Private_Key,
    )
# Configure APIv4 key authorization
    api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
    api_instance = gate_api.FuturesApi(api_client)
    print("Logged in Successfully!")
    return api_instance;


def get_history_data():

    #State Variables
    global df;

    abi_instance = logged_in();

    print("Getting history raw future data....")
    history_close_price = [];
    history_high_price = [];
    history_low_price = [];
    history_open_price = [];
    history_timestamp = [];
    history_volume = [];
    settle = 'usdt' # str | Settle currency
    print("Settle Currency: %s" % settle);
    contract = 'BTC_USDT' # str | Futures contract
    print("Contract: %s" % contract);
    #limit = 100 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
    bar_interval = '1m' # str | Interval time between data points. Note that `1w` means natual week(Mon-Sun), while `7d` means every 7d since unix 0 (optional) (default to '5m')
    print("Interval: %s" % bar_interval);
    
    #get past 1 day raw data = 60 * 60 * 24 
    now_time = datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'); 
    first_time = datetime.utcfromtimestamp(int(time.time()) - (60*60*24)).strftime('%Y-%m-%d %H:%M:%S');
    print("Time: %s  %s" % (first_time , now_time ));
    _from =  int(time.time()) - (60*60*24);# int | Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified (optional)
    to = int(time.time()); # int | End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time (optional)
    api_response = abi_instance.list_futures_candlesticks(settle, contract, _from=_from, to=to, interval=bar_interval);
    #pprint(type(api_response))
    for each in api_response:
        history_close_price.append(each._c);
        history_high_price.append(each._h);
        history_low_price.append(each._l);
        history_open_price.append(each._o);
        history_timestamp.append(each._t);
        history_volume.append(each._v);    
    #pprint(history_close_price)
    d = {'time': history_timestamp,'open': history_open_price,'high': history_high_price,'low': history_low_price,'close': history_close_price,'volume':history_volume}
    df = pd.DataFrame(data=d)
    #MACD Calculate
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()
    print("Get Data Successfully!")
    return df;



def plot_image(df):
    print("Image shows!")
    Initial_Time = datetime.utcfromtimestamp(df.iloc[0,0]).strftime('%Y-%m-%d %H:%M:%S');
    End_Time = datetime.utcfromtimestamp(df.iloc[-1,0]).strftime('%Y-%m-%d %H:%M:%S');
    X_index = pd.to_datetime(df['time'],unit='s');
    
    fig = go.Figure(data=go.Candlestick(
                x= X_index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']))

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
    # add moving average traces
    fig.add_trace(go.Scatter(x = X_index, 
                         y=df['MA5'], 
                         opacity=0.7, 
                         line=dict(color='blue', width=2), 
                         name='MA 5'))
    fig.add_trace(go.Scatter(x= X_index, 
                         y=df['MA20'], 
                         opacity=0.7, 
                         line=dict(color='orange', width=2), 
                         name='MA 20'))
    fig.add_trace(go.Scatter(x= X_index, 
                         y=df['MA200'], 
                         opacity=0.7, 
                         line=dict(color='black', width=2), 
                         name='MA 200'))
                         
    
    # Plot volume trace on 2nd row 
    fig.add_trace(go.Bar(x= X_index, 
                     y=df['volume']
                    ), row=2, col=1)                     

    fig.update_layout(
    title='ETH Price from %s to %s'% ( Initial_Time,End_Time ),
    # remove rangeslider
    xaxis_rangeslider_visible=False,
    yaxis_title='ETH',
    shapes = [dict(
        x0= Initial_Time, x1= End_Time, y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    # annotations=[dict(
    #     x=now_time, y=0.05, xref='x', yref='paper',
    #     showarrow=False, xanchor='left', text='Increase Period Begins')]
    )

    fig.show()