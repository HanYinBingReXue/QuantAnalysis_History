import plotly.graph_objects as go
import pandas as pd
import gate_api
import time
from config import *
from pprint import pprint
from datetime import datetime
from plotly.subplots import make_subplots
from ta.trend import MACD
import random

#State Variable
Max_Bar_Num = 1000;
settle = 'usdt' # str | Settle currency
bar_interval = '4h' # str | Interval time between data points. Note that `1w` means natual week(Mon-Sun), while `7d` means every 7d since unix 0 (optional) (default to '5m')
contract = 'BTC_USDT' # str | Futures contract
##2020-01-01 00:00:00 ---- 2022-1-1 00:00:00
##    1577854800 ------------- 1641013200
#to_time_unix = int(time.time());
#在2015年和2021年之间任选一段时间
to_time_unix = random.randint(1577854800,1641013200)
to_time_str = datetime.utcfromtimestamp(to_time_unix).strftime('%Y-%m-%d %H:%M:%S');
if "s" in bar_interval:
    bar_interval_value = int(bar_interval.replace("s",""))
    from_time_unix = to_time_unix - (Max_Bar_Num * bar_interval_value);
    from_time_str = datetime.utcfromtimestamp(to_time_unix - (Max_Bar_Num * bar_interval_value)).strftime('%Y-%m-%d %H:%M:%S');

if "m" in bar_interval:
    bar_interval_value = int(bar_interval.replace("m",""))
    from_time_unix = to_time_unix - (Max_Bar_Num * bar_interval_value * 60);
    from_time_str = datetime.utcfromtimestamp(to_time_unix - ( Max_Bar_Num * bar_interval_value * 60)).strftime('%Y-%m-%d %H:%M:%S');

if "h" in bar_interval:
    bar_interval_value = int(bar_interval.replace("h",""))
    from_time_unix = to_time_unix - (Max_Bar_Num * bar_interval_value * 60 * 60);
    from_time_str = datetime.utcfromtimestamp(to_time_unix - ( Max_Bar_Num * bar_interval_value * 60 * 60)).strftime('%Y-%m-%d %H:%M:%S');

if "d" in bar_interval:
    bar_interval_value = int(bar_interval.replace("d",""))
    from_time_unix = to_time_unix - (Max_Bar_Num * bar_interval_value * 60 * 60 * 24);
    from_time_str = datetime.utcfromtimestamp(to_time_unix - ( Max_Bar_Num * bar_interval_value * 60 * 60 * 24)).strftime('%Y-%m-%d %H:%M:%S');

if "w" in bar_interval:
    bar_interval_value = int(bar_interval.replace("w",""))
    from_time_unix = to_time_unix - (Max_Bar_Num * bar_interval_value * 60 * 60 * 24 * 7);
    from_time_str = datetime.utcfromtimestamp(to_time_unix - ( Max_Bar_Num * bar_interval_value * 60 * 60 * 24 * 7)).strftime('%Y-%m-%d %H:%M:%S');


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

    global from_time_unix,settle,bar_interval,contract,from_time_str,to_time_str;


    abi_instance = logged_in();

    print("Getting history raw future data....")
    history_close_price = [];
    history_high_price = [];
    history_low_price = [];
    history_open_price = [];
    history_timestamp = [];
    history_volume = [];
    
    print("Settle Currency: %s" % settle);
    print("Contract: %s" % contract);
    #limit = 100 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
    print("Interval: %s" % bar_interval);
    print("Time: %s  %s" % (from_time_str , to_time_str ));
    _from = from_time_unix ;# int | Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified (optional)
    to = to_time_unix; # int | End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time (optional)
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
    #均线 Calculate  
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()
    #MACD Calculate
    # MACD
    macd = MACD(close=df['close'], 
            window_slow=26,
            window_fast=12, 
            window_sign=9)
    print("Get Data Successfully!")
    return df,macd;


def plot_image(df,macd):
    print("Image shows!")
    X_index = pd.to_datetime(df['time'],unit='s');
    fig = go.Figure()
    fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
                    vertical_spacing=0.01, 
                    row_heights=[0.5,0.1,0.2,0.2]);
    fig.add_trace(go.Candlestick(
                x= X_index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))
    
    #fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
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
    bar_color = [];
    for each in range(0,Max_Bar_Num):
        if df['open'][each] >= df["close"][each]:
            bar_color.append("green")
        else:
            bar_color.append("red")
    
    fig.add_trace(go.Bar(x = X_index, 
                     y=df['volume'],
                     marker_color = bar_color,
                     name= 'Volume'), 
                     row=2, col=1);   

    #Plot MACD
    # Plot MACD trace on 3rd row
    macd_color = [];
    for val in macd.macd_diff():
        if val >= 0:
            macd_color.append("green")
        else:
            macd_color.append("red")
    fig.add_trace(go.Bar(x = X_index, 
                        y= macd.macd_diff(),
                        marker_color=macd_color,
                        ), row=3, col=1)
    fig.add_trace(go.Scatter(x=X_index,
                            y=macd.macd(),
                            line=dict(color='black', width=2)
                            ), row=3, col=1)
    fig.add_trace(go.Scatter(x=X_index,
                            y=macd.macd_signal(),
                            line=dict(color='blue', width=1)
                            ), row=3, col=1)                                   

    # update y-axis label
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)

    fig.update_layout(
    title='ETH Price from %s to %s'% ( from_time_str, to_time_str ),
    # remove rangeslider
    xaxis_rangeslider_visible=False,
    yaxis_title='ETH',
    shapes = [dict(
        x0= from_time_str, x1= to_time_str, y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    )

    fig.show()