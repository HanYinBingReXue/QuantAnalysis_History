from Setting import *
from scipy import signal
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
contract_index = 40
# for contract_index in range(60,70):
contract = (((datasheet[contract_index].split("/"))[-1].split("."))[0].split("_"))[0];
print(contract)
contract_list.append(contract);
bar_interval = (((datasheet[contract_index].split("/"))[-1].split("."))[0].split("_"))[1]
raw_eth_price_data = pd.read_csv(datasheet[contract_index], index_col = 0);
# raw_eth_price_data["Volatility"] =  (raw_eth_price_data["High"] - raw_eth_price_data["Low"]) / raw_eth_price_data["Open"]
# print(raw_eth_price_data)
# n, bins, patches = plt.hist(raw_eth_price_data["Volatility"], 100, density=True, facecolor='g', alpha=0.75)
# plt.show()
price = (raw_eth_price_data["Open"] + raw_eth_price_data["Close"])/2;
moving_average_data = moving_average(price,18)
b,a = signal.butter(6,0.07,"lowpass")
filterdata = signal.filtfilt(b,a,price)
print(filterdata)
fig = go.Figure()
fig.add_trace(go.Candlestick(
                x= raw_eth_price_data.index,
                open=raw_eth_price_data['Open'],
                high=raw_eth_price_data['High'],
                low=raw_eth_price_data['Low'],
                close=raw_eth_price_data['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))
fig.add_trace(go.Scatter(x = raw_eth_price_data.index, y=price,mode='lines',line_color = "#000000",
                    name='average price'))
fig.add_trace(go.Scatter(x = raw_eth_price_data.index, y=filterdata,mode='lines',line_color = "#000000",
                    name='filterdata'))
fig.add_trace(go.Scatter(x = raw_eth_price_data.index[8:], y=moving_average_data,mode='lines',line_color = "#000000",
                    name='moving_average_data'))                    
fig.show()

