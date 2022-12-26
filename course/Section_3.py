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
# print(res.summary())


price = raw_eth_price_data["Close"]
# print(ts.adfuller(price,1))
#(-0.6632498468209983, 0.8560404416872684, 1, 2265, {'1%': -3.4332403869849286, '5%': -2.862816899390905, '10%': -2.567449752837351}, -20870.76046805427)
# 统计量                p值，如果p值大于0.05，则表明原序列并不满足均值回复


# Hurst Exponent
# H < 0.5 时间序列是平均回复
# H = 0.5 时间序列是几何布朗运动
# H > 0.5 时间序列具有趋势

from numpy import sqrt,std,polyfit,log,subtract
def hurst(df):
    lags = range(2,100);
    tau = [sqrt(std(subtract(df[lag:],df[:lag])))for lag in lags]
    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags),log(tau),1)
    return poly[0] * 2.0
print(len(price))
result = hurst(price)
print(result)
