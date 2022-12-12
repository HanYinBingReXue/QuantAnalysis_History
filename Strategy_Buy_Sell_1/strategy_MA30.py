import pandas as pd;
import plotly.graph_objects as go
import plotly.express as px
import os
from plotly.subplots import make_subplots
from sklearn import preprocessing
import numpy as np
from Function_Set import *
from scipy import signal
from datetime import datetime
from pprint import pprint
#Modify Path
os.chdir("/Users/han/Crypto/QuantAnalysis_History_ETH/Strategy_Buy_Sell_1")
current_directory = os.getcwd()
#print(current_directory) 
# get all relevant historical data
#sheet name
#ETH_USDT_2022_06_1m
#ETH_USDT_2022_06_5m
#ETH_USDT_2022_06_1h
#ETH_USDT_2022_06_4h
#ETH_USDT_2022_06_1d
raw_data_eth = pd.read_csv("ETH-USD-2021.csv");
raw_data_dow = pd.read_csv("Dow-2021.csv");
raw_data_nas = pd.read_csv("nasdaq-2021.csv");
raw_data_vix = pd.read_csv("VIX_History.csv");
raw_data_fed = pd.read_csv("FEDFUNDS.csv");
#------------------------------------------------------------------


#data preprocessing
#------------------------------------------------------------------
#格式统一 
#日期格式 2021-01-01 %Y-%M-%D to 2021-12-31
# Column Date Open High Low Close
#drop columns we dont need
for each in range(0,len(raw_data_eth)):
    raw_data_eth.loc[each,"Date"] = datetime.strptime(raw_data_eth.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
Index = raw_data_eth["Date"];
raw_data_eth = raw_data_eth.set_index(Index)
raw_data_eth = raw_data_eth.drop(["Close","Volume","Date"], axis = 1);
raw_data_eth = raw_data_eth.rename(columns={"Adj Close" : "Close"});
#ETH Format Done

for each in range(0,len(raw_data_dow)):
    raw_data_dow.loc[each,"Date"] = datetime.strptime(raw_data_dow.loc[each,"Date"],"%m/%d/%y").strftime("%Y-%m-%d %H:%M:%S");
raw_data_dow = raw_data_dow.loc[::-1].reset_index(drop=True);
#change object type to datetime type
raw_data_dow["Date"] = pd.to_datetime(raw_data_dow["Date"]);
Index = raw_data_dow["Date"];
raw_data_dow = raw_data_dow.set_index(Index)
raw_data_dow = raw_data_dow.drop(["Date"], axis = 1);
raw_data_dow = raw_data_dow.rename(columns= {' Open': "Open", ' High': "High", ' Low' : "Low", ' Close':"Close"});
#Dow Format Done

for each in range(0,len(raw_data_nas)):
    raw_data_nas.loc[each,"Date"] = datetime.strptime(raw_data_nas.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
#change object type to datetime type
raw_data_nas["Date"] = pd.to_datetime(raw_data_nas["Date"]);
Index = raw_data_nas["Date"];
raw_data_nas = raw_data_nas.set_index(Index)
raw_data_nas = raw_data_nas.drop(["Close","Volume","Date"], axis = 1);
raw_data_nas = raw_data_nas.rename(columns={"Adj Close" : "Close"});
#Nas Format Done

for each in range(0,len(raw_data_vix)):
    raw_data_vix.loc[each, "DATE"] = ((datetime.strptime(raw_data_vix.loc[each, "DATE"],"%m/%d/%Y")).strftime("%Y-%m-%d %H:%M:%S"))
raw_data_vix = raw_data_vix.rename(columns={"DATE" : "Date"});
raw_data_vix = raw_data_vix[7808:8060];
#change object type to datetime type
raw_data_vix["Date"] = pd.to_datetime(raw_data_vix["Date"]);
Index = raw_data_vix["Date"];
raw_data_vix = raw_data_vix.set_index(Index)
raw_data_vix = raw_data_vix.drop(["Date"], axis = 1); 
#Vix Format Done


for each in range(0,len(raw_data_fed)):
    raw_data_fed.loc[each,"DATE"] = datetime.strptime(raw_data_fed.loc[each,"DATE"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
#change object type to datetime type
raw_data_fed["DATE"] = pd.to_datetime(raw_data_fed["DATE"]);
Index = raw_data_fed["DATE"];
raw_data_fed = raw_data_fed.set_index(Index)
raw_data_fed = raw_data_fed.drop(["DATE"], axis = 1);
raw_data_fed = raw_data_fed.rename(columns={"FEDFUNDS" : "Interest"});
raw_data_fed = raw_data_fed[0:12]

#补齐所有日期 
from_date = "2021-01-01";
end_date = "2021-12-31";
raw_data_dow = add_missing_date(from_date,end_date,raw_data_dow);
raw_data_nas = add_missing_date(from_date,end_date,raw_data_nas);
raw_data_vix = add_missing_date(from_date,end_date,raw_data_vix);
raw_data_fed = add_missing_date(from_date,end_date,raw_data_fed);


#data Processing
#------------------------------------------------------------------
#使用average price = (open + close) / 2;
raw_data_eth["Ave_Price"] = (raw_data_eth["Open"] + raw_data_eth["Close"])/2;
raw_data_dow["Ave_Price"] = (raw_data_dow["Open"] + raw_data_dow["Close"])/2;
raw_data_nas["Ave_Price"] = (raw_data_nas["Open"] + raw_data_nas["Close"])/2;
raw_data_vix["Ave_Price"] = (raw_data_vix["Open"] + raw_data_vix["Close"])/2;
raw_data_fed["Ave_Price"] = (raw_data_fed["Interest"]);


# Normalized Average Price Calculate
normalized_price_eth = normalized(raw_data_eth["Ave_Price"]); #2021-01-01 -- 2021-12-31
normalized_price_dow = normalized(raw_data_dow["Ave_Price"]); #2021-01-01 -- 2021-12-31
normalized_price_nas = normalized(raw_data_nas["Ave_Price"]); #2021-01-01 -- 2021-12-31
normalized_price_vix = normalized(raw_data_vix["Ave_Price"]); #2021-01-01 -- 2021-12-31
normalized_price_fed = normalized(raw_data_fed["Ave_Price"]); #2022-01-01 -- 2022-12-31

raw_data_eth["Nor_Ave_Price"] = normalized_price_eth;
raw_data_dow["Nor_Ave_Price"] = normalized_price_dow;
raw_data_nas["Nor_Ave_Price"] = normalized_price_nas;
raw_data_vix["Nor_Ave_Price"] = normalized_price_vix;
raw_data_fed["Nor_Ave_Price"] = normalized_price_fed;
#print(raw_data_dow)
#将normalized函数化为1和0的函数（称为step_normalized)，如果前值比后值大，则为1；如果前值比后值小则为0；EX data(59) < data(60); 则取1
step_normalized_eth = step_normalized(raw_data_eth["Nor_Ave_Price"]);
#----------------------------------------------------------
# 以多少日线来判断
MA_num_list = [7,15,30,60];
for MA_Num in MA_num_list:
    print(MA_Num)
    step_normalized_eth = step_normalized_eth[MA_Num-1:]
    #构造一条曲线以判断 通过5条直线的斜率判断
    # 计算ma30 然后以当前的最新数据计算与ma30的斜率
    # 计算ma30
    MA60_eth = moving_average(raw_data_eth["Nor_Ave_Price"],MA_Num)
    MA60_dow = moving_average(raw_data_dow["Nor_Ave_Price"],MA_Num)
    MA60_nas = moving_average(raw_data_nas["Nor_Ave_Price"],MA_Num)
    MA60_vix = moving_average(raw_data_vix["Nor_Ave_Price"],MA_Num)
    MA60_fed = moving_average(raw_data_fed["Nor_Ave_Price"],MA_Num)

    #以后一天的数据计算斜率 length = 306
    slope_eth = slope_cal(raw_data_eth["Nor_Ave_Price"],MA60_eth,MA_Num);
    slope_dow = slope_cal(raw_data_dow["Nor_Ave_Price"],MA60_dow,MA_Num);
    slope_nas = slope_cal(raw_data_nas["Nor_Ave_Price"],MA60_nas,MA_Num);
    slope_vix = slope_cal(raw_data_vix["Nor_Ave_Price"],MA60_vix,MA_Num);
    slope_fed = slope_cal(raw_data_fed["Nor_Ave_Price"],MA60_fed,MA_Num);

    #print(Judgement_Line)

    #----------------------------------------------------
    #测试系数
    #将normalized函数化为1和0的函数（称为step_normalized)，如果前值比后值大，则为1；如果前值比后值小则为0；EX data(59) < data(60); 则取1
    #测试函数是已知值去判断是否正确
    #将函数与Judgement 判断 数函数1 且 Judgement也为1 或者函数0 Judgement也为0的个数
    #取最多个数的系数
    store = [];
    coeffient_eth_range = np.arange(0.2,0.3,0.01);
    coeffient_dow_range = np.arange(0,0.15,0.01);
    coeffient_nas_range = np.arange(0,0.15,0.01);
    coeffient_vix_range = np.arange(0.2,0.4,0.01);
    coeffient_fed_range = np.arange(0.4,0.6,0.01);
    Judgement_up_range = np.arange(0,0.15,0.01);
    Judgement_down_range = np.arange(0,0.15,0.01);
    for coeffient_eth in coeffient_eth_range:
        print(coeffient_eth);
        for coeffient_dow in coeffient_dow_range:
            for coeffient_nas in coeffient_nas_range:
                for coeffient_vix in coeffient_vix_range:
                    for coeffient_fed in coeffient_fed_range:
                        for Judgement_up in Judgement_up_range:
                            for Judgement_down in Judgement_down_range:
                                if(coeffient_eth+coeffient_dow+coeffient_nas+coeffient_vix+coeffient_fed == 1):
                                    Judgement_Line = []
                                    for i in range(0,len(slope_eth)):
                                        Judgement = (slope_eth[i]*coeffient_eth) + (slope_dow[i]*coeffient_dow) + (slope_nas[i]*coeffient_nas) - (slope_vix[i]*coeffient_vix) - (slope_fed[i]*coeffient_fed);
                                        if Judgement >= Judgement_up:
                                            Judgement = 1;
                                        elif Judgement <= -Judgement_down:
                                            Judgement = 0;
                                        else:
                                            Judgement = 0.5;
                                        Judgement_Line.append(Judgement);
                                    count = 0;
                                    for j in range(0,len(step_normalized_eth)):
                                        if step_normalized_eth[j] == Judgement_Line[j]:
                                            count = count + 1;
                                    store.append(["MA_Num:",MA_Num,"coeffient_eth:",coeffient_eth,"coeffient_dow:",coeffient_dow,"coeffient_nas:",coeffient_nas,"coeffient_vix:",coeffient_vix,"coeffient_fed:",coeffient_fed,"Judgement_up:",Judgement_up,"Judgement_down:",Judgement_down,"count:",count])
                                else:
                                    break;
    coincide = [];                        
    for each in store:
        coincide.append(each[-1])
    print(coincide.index(max(coincide)))
    print(store[coincide.index(max(coincide))])
#------------------------------------------------------------------------------------------------\
#经测试 'coeffient_eth:', 0.2, 'coeffient_dow:', 0.0, 'coeffient_nas:', 0.05, 
# 'coeffient_vix:', 0.25000000000000006, 'coeffient_fed:', 0.5000000000000001, 'count:', 151, 
# 'Judgement_up:', 0.0, 'Judgement_down:', 0.14
# #重合最多
# # 以nas--10% dow--10% coin--20% fed--40% vix--20% 的分布计算 
# coeffient_eth = 0.2;
# coeffient_dow= 0.0;
# coeffient_nas = 0.05;
# coeffient_vix = 0.25;
# coeffient_fed = 0.5;
# Judgement_up = 0;
# Judgement_down = 0.14;
# # Judgement_Line
# Judgement_Line = []
# for i in range(0,len(slope_eth)):
#     Judgement = (slope_eth[i]*coeffient_eth) + (slope_dow[i]*coeffient_dow) + (slope_nas[i]*coeffient_nas) - (slope_vix[i]*coeffient_vix) - (slope_fed[i]*coeffient_fed);
#     if Judgement >= Judgement_up:
#         Judgement = 1;
#     elif Judgement <= -Judgement_down:
#         Judgement = 0;
#     else:
#         Judgement = 0.5;
#     Judgement_Line.append(Judgement);                   
#数据可视化
#----------------------------------------------------
# fig = go.Figure();
# fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
#                 vertical_spacing=0.01, 
#                 row_heights=[0.5,0.1,0.2,0.2]);
# fig.add_trace(go.Scatter(x= raw_data_eth.index, y=raw_data_eth["Nor_Ave_Price"],mode='lines',
#                     name='ETH'))
# fig.add_trace(go.Scatter(x= raw_data_eth.index[59:], y= Judgement_Line,mode='lines',
#                     name='Judgement'))
# fig.add_trace(go.Scatter(x= NAS_index, y=nor_data_nas_trendline,mode='lines',
#                     name='NAS'))
# fig.add_trace(go.Scatter(x= VIX_index, y=nor_data_vix_trendline,mode='lines',
#                     name='VIX'))
# fig.add_trace(go.Scatter(x= FED_index, y=nor_data_fed_trendline,mode='lines',
#                     name='FED')) 
# fig.add_trace(go.Scatter(x= DOW_index, y= nor_judgement,mode='lines',
#                     name='Judgement')) 
# fig.show()



## 策略
#买入或做空
#策略1 由美国联邦利率，市场恐慌指数，纳斯达克指数，道琼斯指数(分别计算当时的值和斜率）和货币
# 本身ATR和历史位置判断 是做多或是做空 判断BTC ETH

















def plot_image(df):
    ## 使用MA200作为入场标志，当bar穿过MA200买入，从最高点回撤百分之2卖出。
    ##
    #df['MA200'] = df['Close'].rolling(window=200).mean()
    X_index = pd.to_datetime(df['Timestamp'],unit='s')
    #print(df);
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
                x=  X_index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))


    # fig.add_trace(go.Scatter(x= X_index, 
    #                         y=df['MA200'], 
    #                         opacity=0.7, 
    #                         line=dict(color='black', width=2), 
    #                         name='MA 200'))
    fig.update_layout(
    # title='ETH Price',
    # # remove rangeslider
    xaxis_rangeslider_visible=False,
    # yaxis_title='ETH',
    )
    fig.show()

