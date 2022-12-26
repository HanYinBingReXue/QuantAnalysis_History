# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略
# Process : 
# 当价格高于标准差的1.5倍时开多，或价格低于1.5倍标准差时开空（何时买）
# 当开单时，计算前N个蜡烛的平均波动率 
# 价格回落至线平仓
# 
# 并将最后的结果用图像进行了可视化
#
# 结论：开单太慢，很容易刚买就跌
#
#
from Setting import *

MA_NUM = 30;
# print(os.listdir("./Historical_Data/Data/BTC_USDT/"))
Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/BTCUSDT/BTCUSDT_1m.csv"
bar_interval = Path[-6:-4]
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
up_limit = []
down_limit = []
highest_price = 0;
lowest_price = 0;
close_long_price = 0;
close_short_price = 0;
long_short_start_time = 0;
# 在每一个bar结束的时候，计算前 MA_NUM个bar 的平均值和标准差
# 在偏离1.5个标准差时开仓
# 跟踪价格，在最高价减去1.5个标准差时平仓
for i in range(MA_NUM,len(price)):

    average_price = average_cal(price[i-MA_NUM:i],MA_NUM); # 更新平均价格
    standard_deviation = standard_deviation_cal(price[i-MA_NUM:i]); # 更新标准差
    up_limit_value = average_price + 1.5 * standard_deviation # 更新开多标准 1
    up_limit.append(up_limit_value)
    
    down_limit_value = average_price - 1.5 * standard_deviation # 更新开空标准 1
    down_limit.append(down_limit_value)

    if transaction_type_value == 1: # 更新平多标准
        highest_price = max(highest_price,raw_eth_price_data.iloc[i-1]["High"])
        close_long_price = highest_price  - 1.5 * standard_deviation;
    if transaction_type_value == -1: # 更新平空标准
        lowest_price = min(lowest_price,raw_eth_price_data.iloc[i-1]["Low"]) 
        close_short_price =  lowest_price + 1.5 * standard_deviation;
    

    if price[i] >= up_limit_value and price[i-1] < up_limit_value and \
        raw_eth_price_data.iloc[i]["High"] - raw_eth_price_data.iloc[i]["Low"] > price[i] * 0.01 \
        and transaction_state_value == 0: #开多
        transaction_state_value = 1;
        transaction_type_value = 1;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         raw_eth_price_data.iloc[i]["Close"]])
        highest_price = raw_eth_price_data.iloc[i]["High"];
        long_short_start_time = raw_eth_price_data.iloc[i].name;


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

        

    if price[i] < down_limit_value and price[i-1] >= down_limit_value and transaction_state_value == 0: #开空
        transaction_state_value = 1;
        transaction_type_value = -1;
        transaction_store.append([raw_eth_price_data.iloc[i].name,
                                  transaction_type[transaction_type_value],
                                         transaction_state[transaction_state_value],
                                         raw_eth_price_data.iloc[i]["Close"]])
        lowest_price = raw_eth_price_data.iloc[i]["Low"];
        long_short_start_time = raw_eth_price_data.iloc[i].name;

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
                    name='aveage prce'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[MA_NUM:], y=up_limit,mode='lines',
                    name='Uplimit'),row=1,col=1)
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[MA_NUM:], y=down_limit,mode='lines',
                    name='Downlimit'),row=1,col=1)
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





























