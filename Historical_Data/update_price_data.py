# 代码主要为更新文件库里的数据



import os
import time
import csv
import pandas as pd
from datetime import datetime
from Get_Data_Function import *
# print(os.listdir("./plot_history_candlestick/Historical_Data/Data"))
contract_list = os.listdir("./Historical_Data/Data")[1:] #显示所有合约
# print(contract_list)
for i in range (0,len(contract_list)):
    contract = contract_list[i] #选择一个合约
    contract_path = "./Historical_Data/Data/" + contract_list[i] #选择合约的路径
    datasheet = os.listdir(contract_path) #选择合约路径下的历史数据

    for each in datasheet: #查询每个datasheet最后一行数据的时间是否与此刻相同
        
        datasheet_path = contract_path + "/" + each
        # print(datasheet_path)
        raw_data = pd.read_csv(datasheet_path)
        latest_data_time_str = raw_data.iloc[-1]["Date"]
        latest_data_time_unix = transform_datestr_to_dateunix(latest_data_time_str,"%Y-%m-%d %H:%M:%S")
        now_time_str = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        now_time_unix = transform_datestr_to_dateunix(now_time_str,"%Y-%m-%d %H:%M:%S")
        if(latest_data_time_str != now_time_str):
            # print("需要更新数据！")
            #开始时间，结束时间，合约名称，pair，barinterval
            barinterval = each[-6:-4]
            if check_date(latest_data_time_unix,now_time_unix,barinterval):
                new_data = get_history_data(latest_data_time_unix,now_time_unix,contract,"usdt",barinterval)
                #print(new_data.index[0])
                for i in range(0,len(new_data.index)):
                    new_data_time_unix = transform_datestr_to_dateunix(new_data.index[i],"%Y-%m-%d %H:%M:%S")
                    if(new_data_time_unix > latest_data_time_unix):
                        #开始记录数据
                        print("开始更新数据")
                        new_data = new_data[i:]
                        new_data.to_csv(datasheet_path,index_label=("Date"),header = False ,mode = "a")
                        print("%s 更新数据成功" % each)
                        break;

        else:
            print("无需更新数据!")

    





