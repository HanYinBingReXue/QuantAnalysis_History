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

datasheet = datasheet_path_15m_list
datasheet_Num = 3
contract = (((datasheet[datasheet_Num].split("/"))[-1].split("."))[0].split("_"))[0];
contract_list.append(contract);
bar_interval = (((datasheet[datasheet_Num].split("/"))[-1].split("."))[0].split("_"))[1]
raw_eth_price_data = pd.read_csv(datasheet[datasheet_Num], index_col = 0);

# print(raw_eth_price_data,"\n","contract:",contract,"bar_interval:",bar_interval)

ret = raw_eth_price_data.pct_change().dropna()
# print(ret,"\n","contract:",contract,"bar_interval:",bar_interval)

nsample = 50;
x = np.linspace(0,20,nsample);
# pprint(x)
X = np.column_stack((x,(x-5)**2))
# pprint(X)

X = sm.add_constant(X)

# print(X)

beta  = [5,0.5,-0.01]
sig = 0.5
#The code snippet initializes an array w of size nsample with all elements equal to 1. 
# It then updates the elements in the last 4/10 of the array to be equal to 3.
w = np.ones(nsample)
# print("w:",w)
w[nsample * 6 // 10:] = 3
# print("w_after:",w)
y_true = np.dot(X,beta)
e = np.random.normal(size=nsample)
y = y_true + sig * w * e;
X = X [:,[0,1]]
# print(X)

mod = sm.OLS(y,X)
res = mod.fit()
print(res.summary())
