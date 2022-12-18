import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd;
from datetime import datetime
from pprint import pprint
import os
import numpy as np



def normalized(Price): #归一到 【0 1】
    Price = (Price - min(Price)) / (max(Price) - min(Price));
    return Price

def normalized_minus1_to_1(Price):
    Price = Price - np.mean(Price);
    Price = Price / np.max(np.abs(Price))
    return Price;



def add_missing_date(_from,to,freq,df):
    date_range = pd.date_range(start = _from, end = to,freq=freq);
    # Use the 'reindex()' function to add the missing dates to the data frame
    df = df.reindex(date_range)
    # Fill missing values with the previous value
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    #print(df)
    return df;

def moving_average(data, n):
    moving_average_values = []
    for i in range(0,len(data) - n):
        moving_average_values.append(sum(data[i:i+n]) / n)
    return moving_average_values
#斜率计算
def slope_cal(date, MA_data, MA_NUM):
    slope = []
    for n in range(0, len(MA_data) -1):
        slope.append(date[n + MA_NUM] - MA_data[n]);
    return slope;
#
def step_normalized(df):
    step_normalized = [];
    for i in range(0,len(df)):
        if df[i-1] <= df[i]:
            step_normalized.append(1);
        elif df[i-1] > df[i]:
            step_normalized.append(0);
    return step_normalized;

#计算振幅率
def amplitude_ratio(df):
    amplitude_ratio = []
    for i in range(0,len(df)):
        if i == 0:
            amplitude_value = (df.iloc[i]["High"] - df.iloc[i]["Low"]) / df.iloc[i]["Close"];
        else:
            amplitude_value = (df.iloc[i]["High"] - df.iloc[i]["Low"]) / df.iloc[i-1]["Close"];
        amplitude_value = float("{:.5f}".format(amplitude_value * 100));    
        amplitude_ratio.append(amplitude_value);
    return amplitude_ratio;

def standard_deviation_cal(df,Num):
    standard_deviation = [];
    for i in range(0,len(df) - Num):
        standard_deviation.append(np.std(df[i:i+Num]))
    return standard_deviation;



def plot_candlestick_image(df):
    print("Image shows!")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
                x= df.index,
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



def strategy_test(transaction_store,strategy_start_time,strategy_end_time,strategy_freq):
    # 计算策略效率（盈亏比，最大回撤等）
# 假设 原始资金（1000）
    Initial_Money = 1000;
#------------------------------
    money_change_store = []
    number_of_eth = 0;
    start_long_price = 0;
    close_long_price = 0;
    start_short_price = 0;
    close_short_price = 0;
    #-----------------------
    money = Initial_Money;
    transaction_money = 0;
    profit_loss_ratio = []
    #-------------------------
    long_success = 0;
    long_time = 0;
    short_sucess = 0;
    short_time = 0;
    long_profit = [];
    short_profit = [];
    long_loss = [];
    short_loss = [];
    number_of_eth = 0;
#-----------------------------------------
    total_transaction_number = len(transaction_store)/2;
    for each in range(0, len(transaction_store)):
        if money > 0:
            if transaction_store["Transaction Type"][each] == "Long":
                start_long_price = float(transaction_store["Transaction Price"][each]);
                number_of_eth =  abs(money / start_long_price) ;
                money_change_store.append(money);
                long_time += 1;

            if transaction_store["Transaction Type"][each] == "Close Long":
                close_long_price = float(transaction_store["Transaction Price"][each]);  
                if(start_long_price < close_long_price):
                    long_success += 1;
                    transaction_money = number_of_eth * (close_long_price - start_long_price)
                    long_profit.append(transaction_money);
                    money = money + transaction_money;
                elif(start_long_price >= close_long_price):
                    transaction_money = number_of_eth * (close_long_price - start_long_price)
                    long_loss.append(transaction_money);
                    money =  transaction_money + money;
                money_change_store.append(money);
                start_long_price = 0;
                close_long_price = 0;

            if transaction_store["Transaction Type"][each] == "Short":
                start_short_price = float(transaction_store["Transaction Price"][each]);
                number_of_eth =  abs(money / start_short_price);
                money_change_store.append(money);
                short_time += 1;

            if transaction_store["Transaction Type"][each] == "Close Short":
                close_short_price = float(transaction_store["Transaction Price"][each])
                if(start_short_price > close_short_price):
                    short_sucess += 1;
                    transaction_money = number_of_eth * (start_short_price - close_short_price)
                    short_profit.append(transaction_money);
                    money = money + transaction_money;
                elif(start_short_price <= close_short_price):
                    transaction_money = number_of_eth * (start_short_price - close_short_price);
                    short_loss.append(transaction_money);
                    money = transaction_money + money;
                money_change_store.append(money);
                start_short_price = 0;
                close_short_price = 0;
        elif money <= 0:
            print("亏完啦！")
            break;
    transaction_success_ratio = (long_success + short_sucess) / total_transaction_number;
    print("总共交易次数: %s 胜率: %s \n 做多交易次数: %s 做多获利次数: %s \n 做空交易次数: %s 做空获利次数: %s" 
    %(total_transaction_number,transaction_success_ratio,long_time,long_success,short_time,short_sucess));
    #transaction_store["money_change"] = money_change_store;
    for each in money_change_store:
        profit_loss_ratio.append(each/1000)
    transaction_store["profit_loss_ratio"] = profit_loss_ratio;
    transaction_store["Transaction Time"] = pd.to_datetime(transaction_store["Transaction Time"])
    Index = transaction_store["Transaction Time"];
    transaction_store = transaction_store.set_index(Index);
    transaction_store = transaction_store.drop("Transaction Time",axis = 1);
    profit_loss_ratio_show = transaction_store;
    profit_loss_ratio_show = profit_loss_ratio_show[~profit_loss_ratio_show.index.duplicated(keep="first")]
    profit_loss_ratio_show = add_missing_date(strategy_start_time,strategy_end_time,strategy_freq,profit_loss_ratio_show);
    print("收益率： %s 最后金额; %s \n 做多收益: %s 做多亏损: %s \n 做空收益: %s 做空亏损: %s" 
    %(profit_loss_ratio_show["profit_loss_ratio"][-1],money_change_store[-1],sum(long_profit),sum(long_loss),sum(short_profit),sum(short_loss)))
    
    
    # long_start_record = pd.DataFrame(long_start_record,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
    # long_end_record = pd.DataFrame(long_end_record,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
    # short_start_record = pd.DataFrame(short_start_record,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
    # short_end_record = pd.DataFrame(short_end_record,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
    
    return profit_loss_ratio_show;