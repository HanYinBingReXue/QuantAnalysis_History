# Author: Qi
# Time : 2022 Dec 12
# Goal : 本代码针对2021年ETH，DOW，NAS，VIX，FED Interest进行分析判断ETH买卖点
# Process : 
# 本代码先将数据进行清理（格式归一，补齐缺的数据）
# 然后对数据进行了归一化
# 接着通过斜率构造了判断线条，并计算了在当前值与MA 7 15 30 60的情况下，权重的最优解
# 并将最后的结果用图像进行了可视化
#

from Function_Set import *
from Setting import *
from Raw_Data_Process import *
#print(current_directory) 
# get all relevant historical data
#sheet name
#ETH_USDT_2022_06_1m
#ETH_USDT_2022_06_5m
#ETH_USDT_2022_06_1h
#ETH_USDT_2022_06_4h
#ETH_USDT_2022_06_1d
# raw_data_eth = pd.read_csv("ETH-USD-2021.csv");
# raw_data_dow = pd.read_csv("Dow-2021.csv");
# raw_data_nas = pd.read_csv("nasdaq-2021.csv");
# raw_data_vix = pd.read_csv("VIX_History.csv");
# raw_data_fed = pd.read_csv("FEDFUNDS.csv");
#------------------------------------------------------------------


#data preprocessing
#------------------------------------------------------------------
#格式统一 
#日期格式 2021-01-01 %Y-%M-%D to 2021-12-31
# Column Date Open High Low Close
#drop columns we dont need
# for each in range(0,len(raw_data_eth)):
#     raw_data_eth.loc[each,"Date"] = datetime.strptime(raw_data_eth.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
# Index = raw_data_eth["Date"];
# raw_data_eth = raw_data_eth.set_index(Index)
# raw_data_eth = raw_data_eth.drop(["Close","Volume","Date"], axis = 1);
# raw_data_eth = raw_data_eth.rename(columns={"Adj Close" : "Close"});
# #ETH Format Done

# for each in range(0,len(raw_data_dow)):
#     raw_data_dow.loc[each,"Date"] = datetime.strptime(raw_data_dow.loc[each,"Date"],"%m/%d/%y").strftime("%Y-%m-%d %H:%M:%S");
# raw_data_dow = raw_data_dow.loc[::-1].reset_index(drop=True);
# #change object type to datetime type
# raw_data_dow["Date"] = pd.to_datetime(raw_data_dow["Date"]);
# Index = raw_data_dow["Date"];
# raw_data_dow = raw_data_dow.set_index(Index)
# raw_data_dow = raw_data_dow.drop(["Date"], axis = 1);
# raw_data_dow = raw_data_dow.rename(columns= {' Open': "Open", ' High': "High", ' Low' : "Low", ' Close':"Close"});
# #Dow Format Done

# for each in range(0,len(raw_data_nas)):
#     raw_data_nas.loc[each,"Date"] = datetime.strptime(raw_data_nas.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
# #change object type to datetime type
# raw_data_nas["Date"] = pd.to_datetime(raw_data_nas["Date"]);
# Index = raw_data_nas["Date"];
# raw_data_nas = raw_data_nas.set_index(Index)
# raw_data_nas = raw_data_nas.drop(["Close","Volume","Date"], axis = 1);
# raw_data_nas = raw_data_nas.rename(columns={"Adj Close" : "Close"});
# #Nas Format Done

# for each in range(0,len(raw_data_vix)):
#     raw_data_vix.loc[each, "DATE"] = ((datetime.strptime(raw_data_vix.loc[each, "DATE"],"%m/%d/%Y")).strftime("%Y-%m-%d %H:%M:%S"))
# raw_data_vix = raw_data_vix.rename(columns={"DATE" : "Date"});
# raw_data_vix = raw_data_vix[7808:8060];
# #change object type to datetime type
# raw_data_vix["Date"] = pd.to_datetime(raw_data_vix["Date"]);
# Index = raw_data_vix["Date"];
# raw_data_vix = raw_data_vix.set_index(Index)
# raw_data_vix = raw_data_vix.drop(["Date"], axis = 1); 
# #Vix Format Done


# for each in range(0,len(raw_data_fed)):
#     raw_data_fed.loc[each,"DATE"] = datetime.strptime(raw_data_fed.loc[each,"DATE"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
# #change object type to datetime type
# raw_data_fed["DATE"] = pd.to_datetime(raw_data_fed["DATE"]);
# Index = raw_data_fed["DATE"];
# raw_data_fed = raw_data_fed.set_index(Index)
# raw_data_fed = raw_data_fed.drop(["DATE"], axis = 1);
# raw_data_fed = raw_data_fed.rename(columns={"FEDFUNDS" : "Interest"});
# raw_data_fed = raw_data_fed[0:12]

# #补齐所有日期 
# from_date = "2021-01-01";
# end_date = "2021-12-31";
# # print(raw_data_dow);
# raw_data_dow = add_missing_date(from_date,end_date,raw_data_dow);
# raw_data_nas = add_missing_date(from_date,end_date,raw_data_nas);
# raw_data_vix = add_missing_date(from_date,end_date,raw_data_vix);
# raw_data_fed = add_missing_date(from_date,end_date,raw_data_fed);


# #data Processing
# #------------------------------------------------------------------
# #使用average price = (open + close) / 2;
# raw_data_eth["Ave_Price"] = (raw_data_eth["Open"] + raw_data_eth["Close"])/2;
# raw_data_dow["Ave_Price"] = (raw_data_dow["Open"] + raw_data_dow["Close"])/2;
# raw_data_nas["Ave_Price"] = (raw_data_nas["Open"] + raw_data_nas["Close"])/2;
# raw_data_vix["Ave_Price"] = (raw_data_vix["Open"] + raw_data_vix["Close"])/2;
# raw_data_fed["Ave_Price"] = (raw_data_fed["Interest"]);


# # Normalized Average Price Calculate
# normalized_price_eth = normalized(raw_data_eth["Ave_Price"]); #2021-01-01 -- 2021-12-31
# normalized_price_dow = normalized(raw_data_dow["Ave_Price"]); #2021-01-01 -- 2021-12-31
# normalized_price_nas = normalized(raw_data_nas["Ave_Price"]); #2021-01-01 -- 2021-12-31
# normalized_price_vix = normalized(raw_data_vix["Ave_Price"]); #2021-01-01 -- 2021-12-31
# normalized_price_fed = normalized(raw_data_fed["Ave_Price"]); #2022-01-01 -- 2022-12-31

# raw_data_eth["Nor_Ave_Price"] = normalized_price_eth;
# raw_data_dow["Nor_Ave_Price"] = normalized_price_dow;
# raw_data_nas["Nor_Ave_Price"] = normalized_price_nas;
# raw_data_vix["Nor_Ave_Price"] = normalized_price_vix;
# raw_data_fed["Nor_Ave_Price"] = normalized_price_fed;
#print(raw_data_dow)
#将normalized函数化为1和0的函数（称为step_normalized)，如果前值比后值大，则为1；如果前值比后值小则为0；EX data(59) < data(60); 则取1
step_normalized_eth = step_normalized(raw_data_eth["Nor_Ave_Price"]);
#----------------------------------------------------------
# 构造一条曲线以判断 通过5条直线的斜率判断
MA_num_list = [7,15,30,60];
# 计算ma 然后以当前的最新数据计算与ma的斜率
# 计算ma
MA_Num = MA_num_list[0];
step_normalized_eth = step_normalized_eth[MA_Num-1:];
MA60_eth = moving_average(raw_data_eth["Nor_Ave_Price"],MA_Num)
MA60_dow = moving_average(raw_data_dow["Nor_Ave_Price"],MA_Num)
MA60_nas = moving_average(raw_data_nas["Nor_Ave_Price"],MA_Num)
MA60_vix = moving_average(raw_data_vix["Nor_Ave_Price"],MA_Num)
MA60_fed = moving_average(raw_data_fed["Nor_Ave_Price"],MA_Num)
pprint(MA60_fed)
#以后一天的数据计算斜率 
slope_eth = slope_cal(raw_data_eth["Nor_Ave_Price"],MA60_eth,MA_Num);
slope_dow = slope_cal(raw_data_dow["Nor_Ave_Price"],MA60_dow,MA_Num);
slope_nas = slope_cal(raw_data_nas["Nor_Ave_Price"],MA60_nas,MA_Num);
slope_vix = slope_cal(raw_data_vix["Nor_Ave_Price"],MA60_vix,MA_Num);
slope_fed = slope_cal(raw_data_fed["Nor_Ave_Price"],MA60_fed,MA_Num);
pprint(slope_fed)
#经测试 
# ['MA_Num:', 7, 'coeffient_eth:', 0.2800000000000001, 'coeffient_dow:', 0.09, 
# 'coeffient_nas:', 0.02, 'coeffient_vix:', 0.2, 'coeffient_fed:', 0.41000000000000003, 
# 'Judgement_up:', 0.0, 'Judgement_down:', 0.0, 'count:', 242]
# 
# ['MA_Num:', 15, 'coeffient_eth:', 0.2, 'coeffient_dow:', 0.01, 
# 'coeffient_nas:', 0.08, 'coeffient_vix:', 0.22000000000000003, 'coeffient_fed:', 0.4900000000000001, 
# 'Judgement_up:', 0.0, 'Judgement_down:', 0.0, 'count:', 196]

# ['MA_Num:', 30, 'coeffient_eth:', 0.24000000000000005, 'coeffient_dow:', 0.01, 
# 'coeffient_nas:', 0.13, 'coeffient_vix:', 0.22000000000000003, 'coeffient_fed:', 0.4, 
# 'Judgement_up:', 0.0, 'Judgement_down:', 0.0, 'count:', 158]
#
#['MA_Num:', 60, 'coeffient_eth:', 0.2, 'coeffient_dow:', 0.0, 
# 'coeffient_nas:', 0.09, 'coeffient_vix:', 0.24000000000000005, 'coeffient_fed:', 0.4700000000000001, 
# 'Judgement_up:', 0.0, 'Judgement_down:', 0.0, 'count:', 123]
# # 以nas--10% dow--10% coin--20% fed--40% vix--20% 的分布计算 
coeffient_eth = 0.28;
coeffient_dow= 0.09;
coeffient_nas = 0.02;
coeffient_vix = 0.22;
coeffient_fed = 0.41;
Judgement_up = 0.01;
Judgement_down = 0.01;
# Judgement_Line
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
# Judgement_Line = px.data.tips();
# Judgement_Line = moving_average(Judgement_Line,3);
#print(Judgement_Line)
#----------------------------------------------------
#测试系数
#将normalized函数化为1和0的函数（称为step_normalized)，如果前值比后值大，则为1；如果前值比后值小则为0；EX data(59) < data(60); 则取1
#测试函数是已知值去判断是否正确
#将函数与Judgement 判断 数函数1 且 Judgement也为1 或者函数0 Judgement也为0的个数
#取最多个数的系数
# store = [];
# coeffient_eth_range = np.arange(0.2,0.3,0.01);
# coeffient_dow_range = np.arange(0,0.15,0.01);
# coeffient_nas_range = np.arange(0,0.15,0.01);
# coeffient_vix_range = np.arange(0.2,0.4,0.01);
# coeffient_fed_range = np.arange(0.4,0.6,0.01);
# Judgement_up_range = np.arange(0,0.15,0.01);
# Judgement_down_range = np.arange(0,0.15,0.01);
# for coeffient_eth in coeffient_eth_range:
#     print(coeffient_eth);
#     for coeffient_dow in coeffient_dow_range:
#         for coeffient_nas in coeffient_nas_range:
#             for coeffient_vix in coeffient_vix_range:
#                 for coeffient_fed in coeffient_fed_range:
#                     for Judgement_up in Judgement_up_range:
#                         for Judgement_down in Judgement_down_range:
#                             if(coeffient_eth+coeffient_dow+coeffient_nas+coeffient_vix+coeffient_fed == 1):
#                                 Judgement_Line = []
#                                 for i in range(0,len(slope_eth)):
#                                     Judgement = (slope_eth[i]*coeffient_eth) + (slope_dow[i]*coeffient_dow) + (slope_nas[i]*coeffient_nas) - (slope_vix[i]*coeffient_vix) - (slope_fed[i]*coeffient_fed);
#                                     if Judgement >= Judgement_up:
#                                         Judgement = 1;
#                                     elif Judgement <= -Judgement_down:
#                                         Judgement = 0;
#                                     else:
#                                         Judgement = 0.5;
#                                     Judgement_Line.append(Judgement);
#                                 count = 0;
#                                 for j in range(0,len(step_normalized_eth)):
#                                     if step_normalized_eth[j] == Judgement_Line[j]:
#                                         count = count + 1;
#                                 store.append(["coeffient_eth:",coeffient_eth,"coeffient_dow:",coeffient_dow,"coeffient_nas:",coeffient_nas,"coeffient_vix:",coeffient_vix,"coeffient_fed:",coeffient_fed,"count:",count,"Judgement_up:",Judgement_up,"Judgement_down:",Judgement_down])
#                             else:
#                                 break;
# coincide = [];                        
# for each in store:
#     coincide.append(each[-1])
# print(coincide.index(max(coincide)))
# print(store[coincide.index(max(coincide))])
#------------------------------------------------------------------------------------------------\
# #重合最多


# 策略
# ————————————————————————————————————————————————————————————————————————————————
# 买入或做空
# 策略1 
# 当Judgement 为1时买入，转为0.5或者0时卖出
# 当Judgement 为0时卖出，转为0.5或者1时卖出
# 都以Open Value为依据
# 评判依据 盈亏比 最大回撤
#
# 由于Judgement 只有359个
# 所以要补齐MA_Num个0.5
makeup_judgement = [0.5] * (MA_Num);
Judgement_Line = makeup_judgement + Judgement_Line;
raw_data_eth["Judgement"] = Judgement_Line
# print(Judgement_Line[1])
# print(raw_data_eth.iloc[1].name)

# 算法实现
# 从Judgement 变化记录变化时的日期和价格
temprarystore_judgement_value =  Judgement_Line[0];
# "1": Start    "-1": End  "0":Waitng
transaction_state = { 0 : "Waiting",
                      1  :  "Start",
                      -1  :  "End"};                       
transaction_type = {1 : "Long",
                    2 : "Close Long",
                    0 : "Waiting",
                    -1 : "Short",
                    -2 : "Close Short"};     # "1": Buy; "2": 平多 "-1": Short; “-2”：平空 "0": 空仓

# 初始化
transaction_state_value = 0.5;   
transaction_type_value = 0;
transaction_store = [];
temprarystore_judgement_value = Judgement_Line[0];
#--------------------------------------
for i in range(0, len(Judgement_Line)):
    if Judgement_Line[i] != temprarystore_judgement_value:
        if Judgement_Line[i] > temprarystore_judgement_value:
            if temprarystore_judgement_value == 0.5: #Judgement_Line[i] 则为1 开多
                transaction_state_value = 1;
                transaction_type_value = 1;
                transaction_store.append([raw_data_eth.iloc[i].name,
                                         transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         raw_data_eth.iloc[i]["Open"]]);
                temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
            elif temprarystore_judgement_value == 0:
                if Judgement_Line[i] == 0.5: # 平空 + 等待
                    transaction_state_value = -1;
                    transaction_type_value = -2;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                         transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         raw_data_eth.iloc[i]["Open"]]);
                    # 以上是平空
                    # 以下是等待
                    transaction_state_value = 0;
                    transaction_type_value = 0;
                    temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
                elif Judgement_Line[i] == 1: # 平空 + 开多
                    transaction_state_value = -1;
                    transaction_type_value = -2;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                            transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_data_eth.iloc[i]["Open"]]);
                    #以上是平空
                    #以下是开多
                    transaction_state_value = 1;
                    transaction_type_value = 1;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                            transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_data_eth.iloc[i]["Open"]]);                        
                    temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
        elif Judgement_Line[i] < temprarystore_judgement_value:
            if temprarystore_judgement_value == 0.5: # 现值为0 开空
                transaction_state_value = 1;
                transaction_type_value = -1;
                transaction_store.append([raw_data_eth.iloc[i].name,
                                        transaction_type[transaction_type_value],
                                        transaction_state[transaction_state_value],
                                        raw_data_eth.iloc[i]["Open"]]);                        
                temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
            elif temprarystore_judgement_value == 1:
                if Judgement_Line[i] == 0.5: #平多 + 等待
                    transaction_state_value = -1;
                    transaction_type_value = 2;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                            transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_data_eth.iloc[i]["Open"]]);
                    # 以上是平仓
                    # 以下是等待
                    transaction_state_value = 0;
                    transaction_type_value = 0;
                    temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
                if Judgement_Line[i] == 1: #平多 + 开空
                    transaction_state_value = -1;
                    transaction_type_value = 2;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                            transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_data_eth.iloc[i]["Open"]]);
                    #以上是平多
                    #以下是开空
                    transaction_state_value = 1;
                    transaction_type_value = -1;
                    transaction_store.append([raw_data_eth.iloc[i].name,
                                            transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_data_eth.iloc[i]["Open"]]);                        
                    temprarystore_judgement_value = Judgement_Line[i]; #交易完成变更存储值
transaction_store = pd.DataFrame(transaction_store,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])
# 策略结束

# 计算策略效率（盈亏比，最大回撤等）
# 假设 原始资金（1000）
Initial_Money = 1000;
money_change_store = []
number_of_eth = 0;
start_long_price = 0;
close_long_price = 0;
start_short_price = 0;
close_short_price = 0;
money = Initial_Money;
profit_loss_ratio = []
for each in range(0, len(transaction_store)):
    if transaction_store["Transaction Type"][each] == "Long":
        start_long_price = float(transaction_store["Transaction Price"][each]);
        number_of_eth =  money / start_long_price ;
        money_change_store.append(money);
    if transaction_store["Transaction Type"][each] == "Close Long":
        close_long_price = float(transaction_store["Transaction Price"][each]);
        money = number_of_eth * close_long_price;
        money_change_store.append(money);
        start_long_price = 0;
        close_long_price = 0;
    if transaction_store["Transaction Type"][each] == "Short":
        start_short_price = float(transaction_store["Transaction Price"][each]);
        number_of_eth =  money / start_short_price;
        money_change_store.append(money);
    if transaction_store["Transaction Type"][each] == "Close Short":
        close_short_price = float(transaction_store["Transaction Price"][each]);
        money = number_of_eth *  close_short_price;
        money_change_store.append(money);
        start_short_price = 0;
        close_short_price = 0;
transaction_store["money_change"] = money_change_store;
for each in money_change_store:
    profit_loss_ratio.append(each/1000)
transaction_store["profit_loss_ratio"] = profit_loss_ratio;
transaction_store["Transaction Time"] = pd.to_datetime(transaction_store["Transaction Time"])
Index = transaction_store["Transaction Time"];
transaction_store = transaction_store.set_index(Index);
transaction_store = transaction_store.drop("Transaction Time",axis = 1);
profit_loss_ratio_show = transaction_store;
profit_loss_ratio_show = profit_loss_ratio_show[~profit_loss_ratio_show.index.duplicated(keep="first")]
profit_loss_ratio_show = add_missing_date(from_date,end_date,profit_loss_ratio_show);

# print(profit_loss_ratio_show)
#计算最大收益
max_profit_ratio = profit_loss_ratio_show.max()["profit_loss_ratio"]
max_loss_ratio = profit_loss_ratio_show.min()["profit_loss_ratio"]
strategy_rate = {"最大收益:" : max_profit_ratio,
                 "最大亏损:" : max_loss_ratio}

#数据可视化
#----------------------------------------------------
fig = go.Figure();
fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights=[0.5,0.1,0.2,0.2]);
fig.add_trace(go.Candlestick(
                x= raw_data_eth.index,
                open=raw_data_eth["Open"],
                high=raw_data_eth['High'],
                low=raw_data_eth['Low'],
                close=raw_data_eth['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))
fig.add_trace(go.Scatter(x = raw_data_eth.index, y=raw_data_eth["Nor_Ave_Price"],mode='lines',
                    name='ETH'),
                    row=2,col=1)
fig.add_trace(go.Scatter(x= raw_data_eth.index, y= Judgement_Line,mode='lines',
                    name='Judgement'),
                    row=2,col=1)
fig.add_trace(go.Scatter(x= profit_loss_ratio_show.index, y= profit_loss_ratio_show["profit_loss_ratio"],mode='lines',
                    name='profit_loss_ratio'),row=3,col=1)
# fig.add_trace(go.Scatter(x= FED_index, y=nor_data_fed_trendline,mode='lines',
#                     name='FED')) 
# fig.add_trace(go.Scatter(x= DOW_index, y= nor_judgement,mode='lines',
#                     name='Judgement')) 
fig.update_layout(
    title='ETH Price from 2021-01-01 to 2021-12-31',
    # remove rangeslider
    xaxis_rangeslider_visible=False,
    yaxis_title='ETH',
    # shapes = [dict(
    #     x0= from_time_str, x1= to_time_str, y0=0, y1=1, xref='x', yref='paper',
    #     line_width=2)],
    )
# fig.show()


























# 本身ATR和历史位置判断 是做多或是做空 判断BTC ETH



