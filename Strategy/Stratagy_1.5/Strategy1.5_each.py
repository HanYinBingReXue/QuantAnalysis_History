# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略，为了实现在波谷和波峰开多和开空。
# Process : 使用低通滤波器，计算斜率拐点，反转开多开空，反转平多平空

# 计算数据有：低通滤波器，斜率值
#
# 跟踪价格和波动率，当价格从最高点回落1.5个标准差时平多，当价格从最低点回升1.5个标准差时平空（何时卖）
# 
# 并将最后的结果用图像进行了可视化
#
# 问题：当数据不停的进入时，低筒滤波器的值在不停的改变，可能在上一个低通滤波器计算时拐点数据这个点计算就变成这个点了
# 尝试解决办法，使用高通滤波器，用原数据减去高通滤波器的值

from Setting import *

Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data"
datasheet_path_1h_list = [];
datasheet_path_4h_list = [];
datasheet_path_5m_list = [];
datasheet_path_15m_list = [];
contract_list = os.listdir(Path)
for i in range(0,len(contract_list)):
    # ex /Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/STORJUSDT
    contract_path = Path + "/" + contract_list[i]
    # ex datasheet_path_1h /Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/STORJUSDT/STORJUSDT_1h.csv
    datasheet_path_1h_list.append(contract_path + "/" + contract_list[i] + "_1h.csv");
    datasheet_path_4h_list.append(contract_path + "/" + contract_list[i] + "_4h.csv");
    datasheet_path_5m_list.append(contract_path + "/" + contract_list[i] + "_5m.csv");
    datasheet_path_15m_list.append(contract_path + "/" + contract_list[i] + "_15m.csv");
# pprint(datasheet_path_1h_list)
datasheet = datasheet_path_15m_list

profit_loss_ratio_list = [];
contract_index = 89
# for contract_index in range(60,70):
contract = (((datasheet[contract_index].split("/"))[-1].split("."))[0].split("_"))[0];
print(contract)
contract_list.append(contract);
bar_interval = (((datasheet[contract_index].split("/"))[-1].split("."))[0].split("_"))[1]
raw_eth_price_data = pd.read_csv(datasheet[contract_index], index_col = 0);
profit_loss_ratio = stratagy_test(raw_eth_price_data,2,1);
# profit_loss_ratio_list.append(profit_loss_ratio)

# fig = go.Figure()
# index = contract_list;
# fig.add_trace(go.Scatter(x = index, y= profit_loss_ratio_list,mode='lines',
#                     name='profit_loss_ratio') )    
# fig.show()