# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略，为了实现在波谷和波峰开多和开空。
# Process : 计算MA2和 MA45 MA99 计算 波动率和标准差，并判断此时是震荡还是趋势
# 当此时是震荡行情时： MA2<MA45<MA99时开多，MA2>MA45>MA99上方是开空
# 当此时是趋势行情时：MA2<MA45<MA99 且 前一个 bar 长上影线上涨且目前这个bar下跌，开空；
#                  MA2>MA45>MA99 且 前一个bar长下影线，且这个bar上涨，开多。

# 感悟：趋势和震荡
# 当价格走趋势时 MA2<MA45<MA99时开空，MA2>MA45>MA99上方是开多
# 当价格走震荡时 MA2<MA45<MA99时开多，MA2>MA45>MA99上方是开空
# 如何判断价格走趋势和震荡？
# 注：波动率和标准差有区别。标准差是与均值做差平方和再开放，波动率是指（最高价-最低价） / 开盘价
# 尝试通过波动率来判断，当平均波动率在3%（暂定）之内时看为是震荡；当平均波动率在5%（暂定）以上时看为是趋势
#
# 计算数据有：MA值，标准差 波动率
#
# 跟踪价格和波动率，当价格从最高点回落1.5个标准差时平多，当价格从最低点回升1.5个标准差时平空（何时卖）
# 
# 并将最后的结果用图像进行了可视化
#

# 问题：无法准确判断震荡和趋势，可能判断本身就是伪命题。

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
profit_loss_ratio_list.append(profit_loss_ratio)

# fig = go.Figure()
# index = contract_list;
# fig.add_trace(go.Scatter(x = index, y= profit_loss_ratio_list,mode='lines',
#                     name='profit_loss_ratio') )    
# fig.show()