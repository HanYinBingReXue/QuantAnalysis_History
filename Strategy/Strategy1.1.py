# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略
# Process : 计算MA99 当平均价格穿过MA99时，判断此时MA99斜率（计算方法为当前点和前点做差）
# 判断前10个bar的平均值，如果前10个bar有8个平均值低于MA99则开多，
# 如果前10个bar有8个高于平均值，则开空（何时买）
# 跟踪价格和波动率，当价格从最高点回落1.5个标准差时平多，当价格从最低点回升1.5个标准差时平空（何时卖）
# 
# 并将最后的结果用图像进行了可视化
#
from Setting import *

MA_NUM = 99;
# print(os.listdir("./Historical_Data/Data/BTC_USDT/"))
Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/BTCUSDT/BTCUSDT_15m.csv"
bar_interval = Path[-7:-4]
if bar_interval[-1] == "m":
    bar_interval = bar_interval + "in";
print(bar_interval)
raw_eth_price_data = pd.read_csv(Path, index_col = 0);
if len(raw_eth_price_data > 50000):
    raw_eth_price_data = raw_eth_price_data[-20001:-1];
price = (raw_eth_price_data["Open"] + raw_eth_price_data["Close"])/2;
# price = raw_eth_price_data["Open"]
raw_eth_price_data["Price"] = price;


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
count_num_more = 0;
count_num_less = 0;
highest_price = 0;
lowest_price = 0;
close_long_price = 0;
close_short_price = 0;
long_short_start_time = 0;
MA_list = [];
MA_slope = 0;
for i in range(MA_NUM,len(price)):

    MA_price = average_cal(price[i-MA_NUM+1:i+1],MA_NUM); # 更新MA平均价格
    MA_list.append(MA_price);
    standard_deviation = standard_deviation_cal(price[i-MA_NUM+1:i+1]); # 更新标准差
    if transaction_type_value == 1: # 更新平多标准
        highest_price = max(highest_price,raw_eth_price_data.iloc[i]["High"])
        close_long_price = highest_price  - 1.5 * standard_deviation;
    if transaction_type_value == -1: # 更新平空标准
        lowest_price = min(lowest_price,raw_eth_price_data.iloc[i]["Low"]) 
        close_short_price =  lowest_price + 1.5 * standard_deviation;
    
    if i >= 110:

        MA_slope = (MA_list[i-MA_NUM] - MA_list[i-MA_NUM-1]);

        if price[i] >= MA_price and MA_slope > 0: #平均价格大于MA99
            count_num_less = num_less_than_const(price[i-20:i],MA_price); #且前20个bar中有18个bar的平均值低于MA99
            if  count_num_less >= 18 and transaction_state_value == 0: #开多
                transaction_state_value = 1;
                transaction_type_value = 1;
                transaction_store.append([raw_eth_price_data.iloc[i].name,
                                        transaction_type[transaction_type_value],
                                                transaction_state[transaction_state_value],
                                                price[i]])
                highest_price = raw_eth_price_data.iloc[i]["High"];
                long_short_start_time = raw_eth_price_data.iloc[i].name;
                count_num_less = 0;

        if ((raw_eth_price_data.iloc[i]["Close"] < close_long_price and raw_eth_price_data.iloc[i].name != long_short_start_time)) and transaction_state_value == 1 and transaction_type_value == 1 : #平多
            transaction_state_value = -1;
            transaction_type_value = 2;
            transaction_store.append([raw_eth_price_data.iloc[i].name,
                                    transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_eth_price_data.iloc[i]["Close"]])

            transaction_state_value = 0;   
            transaction_type_value = 0;
            highest_price = 0;
        
        if price[i] <= MA_price and MA_slope < 0: #平均价格小于MA99
            count_num_more = num_more_than_const(price[i-20:i],MA_price); #且前20个bar中有18个bar的平均值大于MA99
            if  count_num_more >= 18 and transaction_state_value == 0: #开空
                transaction_state_value = 1;
                transaction_type_value = -1;
                transaction_store.append([raw_eth_price_data.iloc[i].name,
                                        transaction_type[transaction_type_value],
                                                transaction_state[transaction_state_value],
                                                price[i]])
                lowest_price = raw_eth_price_data.iloc[i]["Low"];
                long_short_start_time = raw_eth_price_data.iloc[i].name;
                count_num_more = 0;

        if ((raw_eth_price_data.iloc[i]["Close"] > close_short_price and raw_eth_price_data.iloc[i].name != long_short_start_time)) and transaction_state_value == 1 and transaction_type_value == -1 : #平空
            transaction_state_value = -1;
            transaction_type_value = -2;
            transaction_store.append([raw_eth_price_data.iloc[i].name,
                                    transaction_type[transaction_type_value],
                                            transaction_state[transaction_state_value],
                                            raw_eth_price_data.iloc[i]["Close"]])   
            transaction_state_value = 0;   
            transaction_type_value = 0;  
            lowest_price = 0;                                                       
# 策略回测
#-------------------------------------
# 策略回测结果
transaction_store = pd.DataFrame(transaction_store,columns=["Transaction Time","Transaction Type","Transaction State","Transaction Price"])



stratagy_result = strategy_test(transaction_store,raw_eth_price_data.index[0],raw_eth_price_data.index[-1],bar_interval);
# print(stratagy_result)


fig = go.Figure()
fig = make_subplots(rows=2, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights=[0.7,0.3]);
fig.add_trace(go.Candlestick(
                x= raw_eth_price_data.index,
                open=raw_eth_price_data['Open'],
                high=raw_eth_price_data['High'],
                low=raw_eth_price_data['Low'],
                close=raw_eth_price_data['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index, y=price,mode='lines',line_color = "#000000",
                    name='average prce'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[110:], y=MA_list,mode='lines',line_color = "#00ff00",
                    name='MA99'),row=1,col=1)
fig.add_trace(go.Scatter(x = stratagy_result.index, y=stratagy_result["profit_loss_ratio"],mode='lines',
                    name='profit_loss_ratio_show'),row=2,col=1)

for i in range(0,len(transaction_store)):
    if transaction_store.iloc[i]["Transaction Type"] == "Long" or transaction_store.iloc[i]["Transaction Type"] == "Close Long":
        arrowcolor = "red"
        arrowside = "start"
        ay = 40
    else:
        arrowcolor = "green"
        arrowside = "end"
        ay = -40

    fig.add_annotation(x=transaction_store.iloc[i]["Transaction Time"], y=transaction_store.iloc[i]["Transaction Price"],
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











