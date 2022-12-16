# 本代码是为了查询历史价格并写入文档（爬取5年内的所有数据并保存，从2021年5月的数据开始）
import csv
from Config import *
import os
import gate_api
#from Function import *
from gate_api.exceptions import ApiException, GateApiException
#获取数据--》存储数据
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from Get_Data_Function import *

settle = 'usdt' # str | Settle currency
contract = 'BNB_USDT' # str | Futures contract
final_time = int(time.time())
bar_interval = ["1m","5m","1h","4h","1d","1w"]
# print(os.listdir("./plot_history_candlestick/Historical_Data/Data/BTC"))
# 2015.1.1 --------2020.3.1
# 1420606800      1583038800
for i in range(0, len(bar_interval)-1):
    print("准备写入第%d个文件..." %i)
    print("准备读取数据")
    data = get_history_data(1420606800,final_time,contract,settle,bar_interval[i])
    # print(os.listdir("./plot_history_candlestick/ETH_Historical_Data"))
    path = ("./plot_history_candlestick/Historical_Data/%s/" %contract)
    folder = os.path.exists(path);
    if not folder:
        os.makedirs(path)
    filename = contract +"_" + str(bar_interval[i]) + ".csv" ;
    path = path + filename;
    print("准备写入文件")
    data.to_csv(path,index_label=("Date"))
    print("写入文件成功！！")





