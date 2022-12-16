# Author: Qi
# Time : 2022 Dec 12
# Goal : 本代码针对2021年ETH，DOW，NAS，VIX，FED Interest进行分析判断ETH买卖点
# Process : 
# 本代码先将数据进行清理（格式归一，补齐缺的数据）
# 然后对数据进行了归一化
# 接着通过斜率构造了判断线条，并计算了在当前值与MA 7 15 30 60的情况下，权重的最优解
# 并将最后的结果用图像进行了可视化
from Function_Set import *

#Modify Path
os.chdir("/Users/han/Crypto/QuantAnalysis_History_ETH/Strategy_Buy_Sell_1")
current_directory = os.getcwd()
#pd setting 显示完全
#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);
#print(current_directory) 
# get all relevant historical data
#sheet name
#ETH_USDT_2022_06_1m
#ETH_USDT_2022_06_5m
#ETH_USDT_2022_06_1h
#ETH_USDT_2022_06_4h
#ETH_USDT_2022_06_1d
raw_data_eth = pd.read_csv("ETH-USD-2021.csv");
raw_data_dow = pd.read_csv("Dow-2021.csv");
raw_data_nas = pd.read_csv("nasdaq-2021.csv");
raw_data_vix = pd.read_csv("VIX_History.csv");
raw_data_fed = pd.read_csv("FEDFUNDS.csv");
#------------------------------------------------------------------


#data preprocessing
#------------------------------------------------------------------
#格式统一 
#日期格式 2021-01-01 %Y-%M-%D to 2021-12-31
# Column Date Open High Low Close
#drop columns we dont need
for each in range(0,len(raw_data_eth)):
    raw_data_eth.loc[each,"Date"] = datetime.strptime(raw_data_eth.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
Index = raw_data_eth["Date"];
raw_data_eth = raw_data_eth.set_index(Index)
raw_data_eth = raw_data_eth.drop(["Close","Volume","Date"], axis = 1);
raw_data_eth = raw_data_eth.rename(columns={"Adj Close" : "Close"});
#ETH Format Done

for each in range(0,len(raw_data_dow)):
    raw_data_dow.loc[each,"Date"] = datetime.strptime(raw_data_dow.loc[each,"Date"],"%m/%d/%y").strftime("%Y-%m-%d %H:%M:%S");
raw_data_dow = raw_data_dow.loc[::-1].reset_index(drop=True);
#change object type to datetime type
raw_data_dow["Date"] = pd.to_datetime(raw_data_dow["Date"]);
Index = raw_data_dow["Date"];
raw_data_dow = raw_data_dow.set_index(Index)
raw_data_dow = raw_data_dow.drop(["Date"], axis = 1);
raw_data_dow = raw_data_dow.rename(columns= {' Open': "Open", ' High': "High", ' Low' : "Low", ' Close':"Close"});
#Dow Format Done

for each in range(0,len(raw_data_nas)):
    raw_data_nas.loc[each,"Date"] = datetime.strptime(raw_data_nas.loc[each,"Date"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
#change object type to datetime type
raw_data_nas["Date"] = pd.to_datetime(raw_data_nas["Date"]);
Index = raw_data_nas["Date"];
raw_data_nas = raw_data_nas.set_index(Index)
raw_data_nas = raw_data_nas.drop(["Close","Volume","Date"], axis = 1);
raw_data_nas = raw_data_nas.rename(columns={"Adj Close" : "Close"});
#Nas Format Done

for each in range(0,len(raw_data_vix)):
    raw_data_vix.loc[each, "DATE"] = ((datetime.strptime(raw_data_vix.loc[each, "DATE"],"%m/%d/%Y")).strftime("%Y-%m-%d %H:%M:%S"))
raw_data_vix = raw_data_vix.rename(columns={"DATE" : "Date"});
raw_data_vix = raw_data_vix[7808:8060];
#change object type to datetime type
raw_data_vix["Date"] = pd.to_datetime(raw_data_vix["Date"]);
Index = raw_data_vix["Date"];
raw_data_vix = raw_data_vix.set_index(Index)
raw_data_vix = raw_data_vix.drop(["Date"], axis = 1); 
#Vix Format Done


for each in range(0,len(raw_data_fed)):
    raw_data_fed.loc[each,"DATE"] = datetime.strptime(raw_data_fed.loc[each,"DATE"],"%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S");
#change object type to datetime type
raw_data_fed["DATE"] = pd.to_datetime(raw_data_fed["DATE"]);
Index = raw_data_fed["DATE"];
raw_data_fed = raw_data_fed.set_index(Index)
raw_data_fed = raw_data_fed.drop(["DATE"], axis = 1);
raw_data_fed = raw_data_fed.rename(columns={"FEDFUNDS" : "Interest"});
raw_data_fed = raw_data_fed[0:12]

#补齐所有日期 
from_date = "2021-01-01";
end_date = "2021-12-31";
raw_data_dow = add_missing_date(from_date,end_date,raw_data_dow);
raw_data_nas = add_missing_date(from_date,end_date,raw_data_nas);
raw_data_vix = add_missing_date(from_date,end_date,raw_data_vix);
raw_data_fed = add_missing_date(from_date,end_date,raw_data_fed);


#data Processing
#------------------------------------------------------------------
#使用average price = (open + close) / 2;
raw_data_eth["Ave_Price"] = (raw_data_eth["Open"] + raw_data_eth["Close"])/2;
raw_data_dow["Ave_Price"] = (raw_data_dow["Open"] + raw_data_dow["Close"])/2;
raw_data_nas["Ave_Price"] = (raw_data_nas["Open"] + raw_data_nas["Close"])/2;
raw_data_vix["Ave_Price"] = (raw_data_vix["Open"] + raw_data_vix["Close"])/2;
raw_data_fed["Ave_Price"] = (raw_data_fed["Interest"]);


#print(raw_data_dow)
#将normalized函数化为1和0的函数（称为step_normalized)，如果前值比后值大，则为1；如果前值比后值小则为0；EX data(59) < data(60); 则取1
# step_normalized_eth = step_normalized(raw_data_eth["Nor_Ave_Price"]);
#----------------------------------------------------------
# 构造一条曲线以判断 通过5条直线的斜率判断
MA_num_list = [7,15,30,60];
# 计算ma 然后以当前的最新数据计算与ma的斜率
# 计算ma
MA_Num = MA_num_list[0];
# step_normalized_eth = step_normalized_eth[MA_Num-1:];
MA_eth = moving_average(raw_data_eth["Ave_Price"],MA_Num)
MA_dow = moving_average(raw_data_dow["Ave_Price"],MA_Num)
MA_nas = moving_average(raw_data_nas["Ave_Price"],MA_Num)
MA_vix = moving_average(raw_data_vix["Ave_Price"],MA_Num)
MA_fed = moving_average(raw_data_fed["Ave_Price"],MA_Num)

#以后一天的数据计算斜率 
slope_eth = slope_cal(raw_data_eth["Ave_Price"],MA_eth,MA_Num);
slope_dow = slope_cal(raw_data_dow["Ave_Price"],MA_dow,MA_Num);
slope_nas = slope_cal(raw_data_nas["Ave_Price"],MA_nas,MA_Num);
slope_vix = slope_cal(raw_data_vix["Ave_Price"],MA_vix,MA_Num);
slope_fed = slope_cal(raw_data_fed["Ave_Price"],MA_fed,MA_Num);
# Normalize Price change slope 
normalized_price_slope_eth = normalized_minus1_to_1(slope_eth); #2021-01-01 -- 2021-12-31
normalized_price_slope_dow = normalized_minus1_to_1(slope_dow); #2021-01-01 -- 2021-12-31
normalized_price_slope_nas = normalized_minus1_to_1(slope_nas); #2021-01-01 -- 2021-12-31
normalized_price_slope_vix = normalized_minus1_to_1(slope_vix); #2021-01-01 -- 2021-12-31
normalized_price_slope_fed = normalized_minus1_to_1(slope_fed); #2022-01-01 -- 2022-12-31

normalized_price_slope_eth = np.insert(normalized_price_slope_eth,0,[0]*7);
normalized_price_slope_dow = np.insert(normalized_price_slope_dow,0,[0]*7);
normalized_price_slope_nas = np.insert(normalized_price_slope_nas,0,[0]*7);
normalized_price_slope_vix = np.insert(normalized_price_slope_vix,0,[0]*7);
normalized_price_slope_fed = np.insert(normalized_price_slope_fed,0,[0]*7);

raw_data_eth["Nor_Slope"] = normalized_price_slope_eth;
raw_data_dow["Nor_Slope"] = normalized_price_slope_dow;
raw_data_nas["Nor_Slope"] = normalized_price_slope_nas;
raw_data_vix["Nor_Slope"] = normalized_price_slope_vix;
raw_data_fed["Nor_Slope"] = normalized_price_slope_fed;
print(raw_data_eth)




# fig.add_trace(go.Scatter(x= FED_index, y=nor_data_fed_trendline,mode='lines',
#                     name='FED')) 
# fig.add_trace(go.Scatter(x= DOW_index, y= nor_judgement,mode='lines',
#                     name='Judgement')) 


