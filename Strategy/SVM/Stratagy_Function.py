import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd;
from datetime import datetime
from pprint import pprint
import os
import numpy as np
import plotly.express as px
from typing import Optional
import matplotlib.pyplot as plt
from scipy import signal
from sklearn import svm,preprocessing
from statsmodels.graphics.tsaplots import plot_acf
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

def average_cal(data,n):
    average_value = (sum(data) / n)
    return average_value;

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

def moving_standard_deviation_cal(df,Num):
    standard_deviation = [];
    for i in range(0,len(df) - Num):
        standard_deviation.append(np.std(df[i:i+Num]))
    return standard_deviation;

def standard_deviation_cal(df):
    standard_deviation_value = np.std(df)
    return standard_deviation_value;

def num_more_than_const(df,const): #此功能是为了数1个list中有多少个值比一个数大
    count = 0;
    for each in df:
        if each > const:
            count += 1;
    return count;

def num_less_than_const(df,const): #此功能是为了数1个list中有多少个值比一个数小
    count = 0;
    for each in df:
        if each < const:
            count += 1;
    return count;


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
    expectation_for_each_short = 0;
    expectation_for_each_long = 0;
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
    print("总共交易次数: %s 胜率: %s \n做多交易次数: %s 做多获利次数: %s \n做空交易次数: %s 做空获利次数: %s" 
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
    if short_time == 0:
        expectation_for_each_short = 0;
    else:
        expectation_for_each_short = (sum(short_profit)+sum(short_loss)/short_time);
    if long_time == 0:
        expectation_for_each_long = 0;
    else:
        expectation_for_each_long = (sum(long_profit)+sum(long_loss))/long_time;    
    print("收益率: %s 最后金额: %s \n做多收益: %s 做多亏损: %s 做多单次期望: %s\n做空收益: %s 做空亏损: %s 做空单次期望: %s" 
    %(profit_loss_ratio_show["profit_loss_ratio"][-1],money_change_store[-1],\
    sum(long_profit),sum(long_loss),expectation_for_each_long,\
    sum(short_profit),sum(short_loss),expectation_for_each_short))
    
    return profit_loss_ratio_show;


fig = go.Figure()
def stratagy_test(df,switch,imageflag): #本function时为了测试买卖时的结果
    #switch 是指只开多，只开空，双开，双不开。
    #switch = 1 --> 只开多
    #switch = -1 --> 只开空
    #switch = 0 --> 双不开
    #switch = 2 --> 双开
    if switch == 1:
        long_state = 1;
        short_state = 0;
    elif switch == -1:
        long_state = 0;
        short_state = 1;
    elif switch == 0:
        long_state = 0;
        short_state = 0;
    elif switch == 2:
        long_state = 1;
        short_state = 1;
    price = (df["Open"] + df["Close"])/2;
# price = raw_eth_price_data["Open"]
    df["Price"] = price;
    transaction_state = { 0 : "Waiting",
                        1  :  "Start",
                        -1  :  "End"};                       
    transaction_type = {1 : "Long",
                        2 : "Close Long",
                        0 : "Waiting",
                        -1 : "Short",
                        -2 : "Close Short"};     # "1": Buy; "2": 平多 "-1": Short; “-2”：平空 "0": 空仓
    #初始化
    transaction_state_value = 0;   
    transaction_type_value = 0;
    transaction_store = [];

    df["Diff"] = df["Close"] - df["Close"].shift(1)
    df["Diff"].fillna(0,inplace=True)

    df["Up"] = df["Diff"]
    df["Up"][df["Diff"]>0] = 1;
    df["Up"][df["Diff"]<0] = 0;
    #预测值暂且初始化为0
    df['predictForUp'] = 0
    #目标值是真实的涨跌情况
    target = df['Up']
    length=len(df)
    trainNum=int(length*0.8)
    predictNum=length-trainNum
    #选择指定列作为特征列
    feature=df[['Open', 'High', 'Low','Close' ,'Volume']]
    #标准化处理特征值
    feature=preprocessing.scale(feature)

    #训练集的特征值和目标值
    featureTrain=feature[1:trainNum-1]
    targetTrain=target[1:trainNum-1]
    svmTool = svm.SVC(C = 100000.0,cache_size=200,class_weight=None,
        coef0=0.0,degree=3,gamma=0.0001,kernel="rbf",
        max_iter= -1,probability=False,random_state=None,
        shrinking=True,tol= 0.001,verbose=False)
    svmTool.fit(featureTrain,targetTrain)



    predictedIndex=trainNum
    predict_list = [];
    #逐行预测测试集
    while predictedIndex<length:
        # print(predictedIndex,"/",length)
        testFeature=feature[predictedIndex:predictedIndex+1]           
        predictForUp=svmTool.predict(testFeature)  
        predict_list.append(predictForUp[0])
        if predictForUp[0] == 1 and transaction_state_value == 0 and long_state == 1: #开多: #
            transaction_state_value = 1;
            transaction_type_value = 1;
            transaction_store.append([df.iloc[predictedIndex].name,
                                    transaction_type[transaction_type_value],
                                        transaction_state[transaction_state_value],
                                        df.iloc[predictedIndex]["Close"]])
        if predictForUp[0] == 0 and transaction_state_value == 1 and transaction_type_value == 1: # 平多
            transaction_state_value = -1;
            transaction_type_value = 2;
            transaction_store.append([df.iloc[predictedIndex].name,
                                        transaction_type[transaction_type_value],
                                                transaction_state[transaction_state_value],
                                                df.iloc[predictedIndex]["Close"]])

            transaction_state_value = 0;   
            transaction_type_value = 0;
        if predictForUp[0] == 0 and transaction_state_value == 0 and short_state == 1: #开空
                transaction_state_value = 1;
                transaction_type_value = -1;
                transaction_store.append([df.iloc[predictedIndex].name,
                                        transaction_type[transaction_type_value],
                                                transaction_state[transaction_state_value],
                                                df.iloc[predictedIndex]["Close"]])
        if predictForUp[0] == 1 and transaction_state_value == 1 and transaction_type_value == -1 : #平空
                transaction_state_value = -1;
                transaction_type_value = -2;
                transaction_store.append([df.iloc[predictedIndex].name,
                                        transaction_type[transaction_type_value],
                                                transaction_state[transaction_state_value],
                                                df.iloc[predictedIndex]["Close"]])   
                transaction_state_value = 0;   
                transaction_type_value = 0;  
    
        predictedIndex = predictedIndex+1
    predict_list = [0.0] * trainNum + predict_list;
    df['predictForUp']=predict_list 
             
    # 策略
    #-------------------------------------
    # 策略回测

    if imageflag == 1:
        fig = make_subplots(rows=2, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights=[0.7,0.3]);
        fig.add_trace(go.Candlestick(
                x= df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'),row=1,col=1)
        
        fig.add_trace(go.Scatter(x = df.index, y=price,mode='lines',line_color = "#000000",
                    name='average price'),row=1,col=1)
        # fig.show()
    transaction_store = pd.DataFrame(transaction_store,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
    if(imageflag):
        profit_loss_ratio = test_result(transaction_store,imageflag,fig);
    else:
        profit_loss_ratio = test_result(transaction_store,imageflag,None);
    return profit_loss_ratio;




def test_result(transaction_store,imageflag,fig):
    transaction_store = pd.DataFrame(transaction_store,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
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
    expectation_for_each_short = 0;
    expectation_for_each_long = 0;
#-----------------------------------------
    total_transaction_number = len(transaction_store)/2;
    for each in range(0, len(transaction_store)):
        if money > 0:
            if transaction_store["Transaction Type"][each] == "Long":
                money = (1 - 0.0004) * money;
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
                money = (1 - 0.0004) * money;
                money_change_store.append(money);
                start_long_price = 0;
                close_long_price = 0;

            if transaction_store["Transaction Type"][each] == "Short":
                money = (1 - 0.0004) * money;
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
                money = (1 - 0.0004)* money;
                money_change_store.append(money);
                start_short_price = 0;
                close_short_price = 0;
        elif money <= 0:
            print("亏完啦！")
            break;
    if total_transaction_number == 0:
        transaction_success_ratio = 0;
        expectation_for_each_long = 0;
        expectation_for_each_short = 0;
        print("无交易！");
        return 0;
    else:
        transaction_success_ratio = (long_success + short_sucess) / total_transaction_number;
        print("总共交易次数: %s 胜率: %s \n做多交易次数: %s 做多获利次数: %s \n做空交易次数: %s 做空获利次数: %s" 
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
        # profit_loss_ratio_show = add_missing_date(strategy_start_time,strategy_end_time,strategy_freq,profit_loss_ratio_show);
        if short_time == 0:
            expectation_for_each_short = 0;
        else:
            expectation_for_each_short = (sum(short_profit)+sum(short_loss))/short_time;
        if long_time == 0:
            expectation_for_each_long = 0;
        else:
            expectation_for_each_long = (sum(long_profit)+sum(long_loss))/long_time;    
        print("收益率: %s 最后金额: %s 单次交易期望: %s\n做多收益: %s 做多亏损: %s 做多单次期望: %s\n做空收益: %s 做空亏损: %s 做空单次期望: %s\n" 
        %(profit_loss_ratio_show["profit_loss_ratio"][-1],money_change_store[-1],(money_change_store[-1] - Initial_Money) / total_transaction_number, \
        sum(long_profit),sum(long_loss),expectation_for_each_long,\
        sum(short_profit),sum(short_loss),expectation_for_each_short))

    if imageflag == 1:
        fig.add_trace(go.Scatter(x = profit_loss_ratio_show.index, y=profit_loss_ratio_show["profit_loss_ratio"],mode='lines',
                    name='profit_loss_ratio_show'),row=2,col=1)


        for i in range(0,len(transaction_store)):
            if transaction_store.iloc[i]["Transaction Type"] == "Long" or transaction_store.iloc[i]["Transaction Type"] == "Close Long":
                arrowcolor = "red"
                ay = 40
            else:
                arrowcolor = "green"
                ay = -40

            fig.add_annotation(x=transaction_store.iloc[i].name, y=transaction_store.iloc[i]["Transaction Price"],
                        text=transaction_store.iloc[i]["Transaction Type"],
                        arrowhead = 3,
                        arrowsize = 2,
                        arrowcolor= arrowcolor,
                        showarrow=True,
                        ay = ay,
                        )
        fig.update_layout(
            # title='ETH Price from %s to %s'% ( from_time_str, to_time_str ),
            # remove rangeslider
            xaxis_rangeslider_visible=False,
            # yaxis_title='ETH',
            # shapes = [dict(
            #     x0= from_time_str, x1= to_time_str, y0=0, y1=1, xref='x', yref='paper',
            #     line_width=2)],
            )  
        fig.show()

    

    return profit_loss_ratio_show["profit_loss_ratio"][-1];


def check_bar_interval(bar_interval):
    if "_" in bar_interval:
        bar_interval = bar_interval.replace("_","");
    return bar_interval;

def check_bar_interval_value(bar_interval):
    barintervalvalue  = 0;
    if "_" in bar_interval:
        bar_interval = bar_interval.replace("_","")
    if "m" in bar_interval:
        barintervalvalue = bar_interval.replace("m","")
    if "h" in bar_interval:
        barintervalvalue = bar_interval.replace("h","")
    if "d" in bar_interval:
        barintervalvalue = bar_interval.replace("d","")
    if "w" in bar_interval:
        barintervalvalue = bar_interval.replace("w","")
    return int(barintervalvalue)

def check_bar_interval_unit(bar_interval):
    unit = bar_interval[-1]
    return unit;

def check_max_sd(sd,df): #这个function是用来检查sd是否在df中是最大的
    if sd >=  max(df):
        return 1;
    else:
        return 0;

def bar_is_downward(df): 
    if df["Open"] > df["Close"]:
        return 1;
    else:
        return 0;

def bar_is_upward(df): 
    if df["Open"] < df["Close"]:
        return 1;
    else:
        return 0;

def SVM_Prediction(raw_data):

    # diff列表示本日和上日收盘价的差
    raw_data["Diff"] = raw_data["Close"] - raw_data["Close"].shift(1)
    raw_data["Diff"].fillna(0,inplace=True)

    raw_data["Up"] = raw_data["Diff"]
    raw_data["Up"][raw_data["Diff"]>0] = 1;
    raw_data["Up"][raw_data["Diff"]<0] = 0;
    #预测值暂且初始化为0
    raw_data['predictForUp'] = 0
    #目标值是真实的涨跌情况
    target = raw_data['Up']
    length=len(raw_data)
    trainNum=int(length*0.8)
    predictNum=length-trainNum
    #选择指定列作为特征列
    feature=raw_data[['Open', 'High', 'Low','Close' ,'Volume']]
    #标准化处理特征值
    feature=preprocessing.scale(feature)

    #训练集的特征值和目标值
    featureTrain=feature[1:trainNum-1]
    targetTrain=target[1:trainNum-1]
    svmTool = svm.SVC(kernel='linear')
    svmTool.fit(featureTrain,targetTrain)



    predictedIndex=trainNum
    predict_list = [];
    #逐行预测测试集
    while predictedIndex<length:
        print(predictedIndex,"/",length)
        testFeature=feature[predictedIndex:predictedIndex+1]           
        predictForUp=svmTool.predict(testFeature)  
        # print(predictForUp) 
        predict_list.append(predictForUp[0])  
        predictedIndex = predictedIndex+1
    predict_list = [0.0] * trainNum + predict_list;
    raw_data['predictForUp']=predict_list 


