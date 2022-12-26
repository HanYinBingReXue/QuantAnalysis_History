# Author: Qi
# Time : 2022 Dec 13
# Goal : 本代码是一个买卖策略
# Process : 计算MA 当平均价格高于MA时则开多，当平均价格低于MA时则开空
# 跟踪价格和波动率，当价格从最高点回落1.5个标准差时平多，当价格从最低点回升1.5个标准差时平空（何时卖）
# 
# 并将最后的结果用图像进行了可视化
#
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

expectation_for_long =[];
expectation_for_short = [];
contract_list = []
fig = go.Figure()
fig = make_subplots(rows= 4, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights= [0.25,0.25,0.25,0.25]);
MA_NUM_List = [2,15,45,99];
datasheet = datasheet_path_15m_list
for j in range(0,len(MA_NUM_List)):
    expectation_for_short = [];
    expectation_for_long = [];
    for i in range(0,len(datasheet)):
    # for i in range(0,3):
        contract = (((datasheet[i].split("/"))[-1].split("."))[0].split("_"))[0];
        contract_list.append(contract);
        bar_interval = (((datasheet[i].split("/"))[-1].split("."))[0].split("_"))[1]
        raw_eth_price_data = pd.read_csv(datasheet[i], index_col = 0);
        
        
        [expectation_for_each_long,expectation_for_each_short] = side_test(raw_eth_price_data,1,MA_NUM_List[j])
        expectation_for_long.append(expectation_for_each_long)
        [expectation_for_each_long,expectation_for_each_short] = side_test(raw_eth_price_data,-1,MA_NUM_List[j])
        expectation_for_short.append(expectation_for_each_short)
    # print("expectation_for_long:",expectation_for_long)   
    # print("expectation_for_short:",expectation_for_short)
    index = contract_list;
    fig.add_trace(go.Scatter(x = index, y= expectation_for_short,mode='lines',
                        name='expectation_for_short'),row = j+1,col = 1 )
    fig.add_trace(go.Scatter(x = index, y= expectation_for_long,mode='lines',
                        name='expectation_for_long'),row = j+1,col = 1 )    
    fig.update_layout(
            title = "Expectation from %s to %s,interval %s" %(raw_eth_price_data.iloc[0].name,raw_eth_price_data.iloc[-1].name,bar_interval),
    )
fig.show()