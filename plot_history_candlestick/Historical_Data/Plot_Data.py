import plotly.graph_objects as go
import pandas as pd
from pprint import pprint
from plotly.subplots import make_subplots
from ta.trend import MACD
import os
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);
#print(os.listdir("./plot_history_candlestick/Historical_Data/Data/BTC"))
# print(os.listdir("./plot_history_candlestick"))
raw_data = pd.read_csv("./plot_history_candlestick/Historical_Data/Data/BTC_USDT_4h.csv")
# print(raw_data)

def plot_image(df):
    print("Image shows!")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
                x= df["Date"],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))
    
    #fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
    # add moving average traces
    # fig.add_trace(go.Scatter(x = X_index, 
    #                      y=df['MA5'], 
    #                      opacity=0.7, 
    #                      line=dict(color='blue', width=2), 
    #                      name='MA 5'))
    # fig.add_trace(go.Scatter(x= X_index, 
    #                      y=df['MA20'], 
    #                      opacity=0.7, 
    #                      line=dict(color='orange', width=2), 
    #                      name='MA 20'))
    # fig.add_trace(go.Scatter(x= X_index, 
    #                      y=df['MA200'], 
    #                      opacity=0.7, 
    #                      line=dict(color='black', width=2), 
    #                      name='MA 200'))
                     
    # Plot volume trace on 2nd row 
    
    # fig.add_trace(go.Bar(x = X_index, 
    #                     y= macd.macd_diff(),
    #                     marker_color=macd_color,
    #                     ), row=3, col=1)
    # fig.add_trace(go.Scatter(x=X_index,
    #                         y=macd.macd(),
    #                         line=dict(color='black', width=2)
    #                         ), row=3, col=1)
    # fig.add_trace(go.Scatter(x=X_index,
    #                         y=macd.macd_signal(),
    #                         line=dict(color='blue', width=1)
    #                         ), row=3, col=1)                                   

    # update y-axis label
    # fig.update_yaxes(title_text="Price", row=1, col=1)
    # fig.update_yaxes(title_text="Volume", row=2, col=1)
    # fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)

    fig.update_layout(
    # title='ETH Price from %s to %s'% ( from_time_str, to_time_str ),
    # remove rangeslider
    xaxis_rangeslider_visible=False,
    yaxis_title='BTC',
    # shapes = [dict(
    #     #x0= from_time_str, x1= to_time_str, y0=0, y1=1, xref='x', yref='paper',
    #     line_width=2)],
    )

    fig.show()

plot_image(raw_data)
# print(raw_data)