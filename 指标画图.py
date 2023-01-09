# 此代码是为了在一个图中显示 MACD，EMA和KDJ
import stock_pandas as spd
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import math
def EMA_Cal(df,Num,Decay_Co):
    result = []
    for i in range(Num,len(df)):
        # print(i)
        fenzi_list = []
        fenmu_list = []
        for j in range(0,Num):
            # print(j)
            eachfenzi = df[i-j-1] * (Decay_Co ** j)
            # print("eachfenzi:",eachfenzi)
            eachfenmu = Decay_Co ** j
            # print("eachfenmu:",eachfenmu)
            fenzi_list.append(eachfenzi)
            fenmu_list.append(eachfenmu)
        # print("fenzi_list:",fenzi_list,"fenmu_list:",fenmu_list)
        each_ema = sum(fenzi_list) / sum(fenmu_list)
        result.append(each_ema)
    return result




ZRX_raw_data = spd.StockDataFrame(pd.read_csv("/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/LUNA2USDT/LUNA2USDT_1h.csv"),date_col="Date",time_frame="1h")

ZRX_raw_data.alias('open', 'Open')
ZRX_raw_data.alias('high', 'High')
ZRX_raw_data.alias('low', 'Low')
ZRX_raw_data.alias('close', 'Close')
ZRX_raw_data = ZRX_raw_data
# print(len(ZRX_raw_data))


# 指数均线计算
sEMA = 12
mEMA = 26

EMA_12 = [math.nan] * sEMA+ EMA_Cal(ZRX_raw_data["Close"],sEMA,0.1)
EMA_26 = [math.nan] * mEMA + EMA_Cal(ZRX_raw_data["Close"],mEMA,0.5)
# EMA_21 = [math.nan] * lMEA + EMA_Cal(ZRX_raw_data["Close"],lMEA,0.9)
EMAs = pd.DataFrame({"EMA_12":EMA_12,"EMA_26":EMA_26})

# 布林带
std_bollinger_midtrail = ZRX_raw_data["boll"]
std_bollinger_uptaril = ZRX_raw_data["boll.upper"]
std_bollinger_lowtaril = ZRX_raw_data["boll.lower"]
# print(std_bollinger_uptaril)
bollinger = pd.DataFrame({"bollinger_uptrail":std_bollinger_uptaril,"bollinger_downtrail":std_bollinger_lowtaril})

# MACD
exp12     = ZRX_raw_data['Close'].ewm(span=12, adjust=False).mean()
exp26     = ZRX_raw_data['Close'].ewm(span=26, adjust=False).mean()
macd      = exp12 - exp26
signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

fb_green = dict(y1=macd.values,y2=signal.values,where=signal<macd,color="#93c47d",alpha=0.6,interpolate=True)
fb_red   = dict(y1=macd.values,y2=signal.values,where=signal>macd,color="#e06666",alpha=0.6,interpolate=True)
fb_green['panel'] = 1
fb_red['panel'] = 1
fb       = [fb_green,fb_red]


macd_deriv = macd - macd.shift(1) 
# print(macd_deriv)
macd_deriv_list = []
for i in range(0,len(macd_deriv)):
    if macd_deriv[i] > 0:
        macd_deriv_list.append(1.05 * ZRX_raw_data['Close'].max())
    else:
        macd_deriv_list.append(ZRX_raw_data['Close'].min() / 1.05)

macd_buy_sell = pd.DataFrame({"macd_buy_sell_line":macd_deriv_list})

# KDJ
# KDJ_K = ZRX_raw_data["kdj.k"]
# KDJ_D = ZRX_raw_data["kdj.d"]
KDJ_J = ZRX_raw_data["kdj.j"]
KDJ = pd.DataFrame({"KDJ_J":KDJ_J,})
KDJ_deriv = KDJ - KDJ.shift(1) 
# print(KDJ_deriv)
KDJ_deriv_list = []
for i in range(0,len(KDJ_deriv)):
    if KDJ_deriv.values[i] > 0:
        KDJ_deriv_list.append(ZRX_raw_data['Close'].max())
    else:
        KDJ_deriv_list.append(ZRX_raw_data['Close'].min())

KDJ_buy_sell = pd.DataFrame({"KDJ_buy_sell":KDJ_deriv_list})

macd_and_kdj_buy_sell_list = []


transaction_type = {1 : "Long",
                    2 : "Close Long",
                    0 : "Waiting",
                    -1 : "Short",
                    -2 : "Close Short"};     # "1": Buy; "2": 平多 "-1": Short; “-2”：平空 "0": 空仓
transaction_type_value = 0

for i in range(1,len(KDJ_deriv)):
    if  macd_deriv[i] > 0:
        transaction_type_value = 1
        if KDJ_deriv.values[i-1] == 1 and  KDJ_deriv.values[i] == 0 and temporary_value == ZRX_raw_data['Close'].max():
            temporary_value = ZRX_raw_data['Close'].min();
            macd_and_kdj_buy_sell_list.append(temporary_value)
        el


    #     temporary_value = ZRX_raw_data['Close'].max();
    #     macd_and_kdj_buy_sell_list.append(ZRX_raw_data['Close'].max())
    # elif KDJ_deriv.values[i] < 0 and macd_deriv[i] < 0:
    #     temporary_value = ZRX_raw_data['Close'].min();
    #     macd_and_kdj_buy_sell_list.append(ZRX_raw_data['Close'].min())
    else:
        macd_and_kdj_buy_sell_list.append(temporary_value)
print(len(macd_and_kdj_buy_sell_list))
macd_and_kdj_buy_sell_line = pd.DataFrame({"macd_and_kdj_buy_sell_line":macd_and_kdj_buy_sell_list})

apds = [
        # mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
        #                  color='dimgray',alpha=1,secondary_y=True),
        # mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=False),
        # mpf.make_addplot(signal,panel=1,color='b',secondary_y=False),#,fill_between=fb),
        # mpf.make_addplot(EMAs),
        # mpf.make_addplot(macd_buy_sell),
        # mpf.make_addplot(KDJ_buy_sell),
        mpf.make_addplot(macd_and_kdj_buy_sell_line),
       ]

s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

# mpf.plot(ZRX_raw_data,type='candle',style = "yahoo",addplot=apds,figscale=1.6,figratio=(6,5),title='\n\nMACD',
#             volume=True,volume_panel=2,panel_ratios=(3,4,1),fill_between=fb)#,show_nontrading=True)
mpf.plot(ZRX_raw_data,type='candle',style = "yahoo",addplot=apds)#,show_nontrading=True)









