# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略
# Process : 
# 当价格高于标准差的1.5倍时开多，或价格低于1.5倍标准差时开空（何时买）
# 当开单时，计算前7个蜡烛的平均波动率 
# 价格回落至线平仓
# 
# 并将最后的结果用图像进行了可视化
#
from Setting import *

MA_NUM = 30;
# print(os.listdir("./Historical_Data/Data/BTC_USDT/"))
Path = "./Historical_Data/Data/ETH_USDT/ETH_USDT_1h.csv"
raw_eth_price_data = pd.read_csv(Path, index_col = 0)[:];
price = (raw_eth_price_data["Open"] + raw_eth_price_data["Close"])/2;
raw_eth_price_data["Price"] = price;
average_price = moving_average(price,MA_NUM);
standard_deviation = standard_deviation_cal(price,MA_NUM);
# print(len(average_price))
# print(len(standard_deviation))
up_limit = []
for i in range(0,len(standard_deviation)):
    up_limit_value = average_price[i] + 1.5 * standard_deviation[i]
    up_limit.append(up_limit_value)
down_limit = []
for i in range(0,len(standard_deviation)):
    down_limit_value = average_price[i] - 1.5 * standard_deviation[i]
    down_limit.append(down_limit_value)

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

for i in range(MA_NUM,len(price)):
    index = i - MA_NUM;
    if price[i] >= up_limit[index] and price[i-1] < up_limit[index -1] and transaction_state_value == 0: #开多
        transaction_state_value = 1;
        transaction_type_value = 1;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         price[i]])
    if price[i] < up_limit[index] and price[i-1] >= up_limit[index-1] and transaction_state_value == 1 and transaction_type_value == 1: #平多
        transaction_state_value = -1;
        transaction_type_value = 2;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         price[i]])
        transaction_state_value = 0;   
        transaction_type_value = 0;
    if price[i] < down_limit[index] and price[i-1] >= down_limit[index-1] and transaction_state_value == 0: #开空
        transaction_state_value = 1;
        transaction_type_value = -1;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         price[i]])
    if price[i] > down_limit[index] and price[i-1] <= down_limit[index-1] and transaction_state_value == 1 and transaction_type_value == -1: #平空
        transaction_state_value = -1;
        transaction_type_value = -2;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         price[i]])   
        transaction_state_value = 0;   
        transaction_type_value = 0;                                                      
# 策略回测
#-------------------------------------
# 策略回测结果
transaction_store = pd.DataFrame(transaction_store,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])



stratagy_result = strategy_test(transaction_store,raw_eth_price_data.index[0],raw_eth_price_data.index[-1],"5min");
# print(stratagy_result)


# fig = go.Figure()
# fig.add_trace(go.Scatter(x = short_start_record["Transaction Time"], y=short_start_record["Transaction Price"],mode='lines',
#                     name='short_start'))
# fig.add_trace(go.Scatter(x = short_end_record["Transaction Time"], y=short_end_record["Transaction Price"],mode='lines',
#                     name='short_end'))
# fig.show()
# fig = go.Figure()
fig = make_subplots(rows=2, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights=[0.7,0.3]);
fig.add_trace(go.Scatter(x = raw_eth_price_data.index, y=price,mode='lines',
                    name='ETH'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[MA_NUM:], y=up_limit,mode='lines',
                    name='Uplimit'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[MA_NUM:], y=down_limit,mode='lines',
                    name='Downlimit'),row=1,col=1)
fig.add_trace(go.Scatter(x = stratagy_result.index, y=stratagy_result["profit_loss_ratio"],mode='lines',
                    name='profit_loss_ratio_show'),row=2,col=1)
# fig.add_annotation(x = long_start_record["Transaction Time"], y = long_start_record["Transaction Price"],
#                     xref="x",yref="y",
#                     text="Long start",arrowcolor="green",showarrow= True ,arrowhead = 1,
#                     )
# fig.add_annotation(x = long_end_record["Transaction Time"], y = long_end_record["Transaction Price"],
#                     text="Long end",arrowcolor="green",showarrow= True ,arrowhead = 1,
#                     row=1,col=1)
# fig.add_annotation(x = short_start_record["Transaction Time"], y = short_start_record["Transaction Price"],
#                     text="Short start",arrowcolor="red",showarrow= True ,arrowhead = 1,
#                     row=1,col=1)
# fig.add_annotation(x = short_end_record["Transaction Time"], y = short_end_record["Transaction Price"],
#                     text="Short end",arrowcolor="red",showarrow= True ,arrowhead = 1,
#                     row=1,col=1)                     
fig.show()





























