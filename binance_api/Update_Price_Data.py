# 代码主要为更新文件库里的数据

import os
import time
import csv
import pandas as pd
from datetime import datetime,timezone
from function_set import *
# print(os.listdir("./plot_history_candlestick/Historical_Data/Data"))
Program_Start_Time = time.time();
Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data"
contract_list = os.listdir(Path)
record_date_list = [];
record_data_index_list = [];

# print(contract_list)
for i in range (0,len(contract_list)):
    contract = contract_list[i] #选择一个合约
    contract_name = contract.split("_")[0]
    print(contract_name)
    contract_path = Path + "/" + contract_list[i] #选择合约的路径
    datasheet = os.listdir(contract_path) #选择合约路径下的历史数据
    # print(datasheet)
    for each in datasheet: #查询每个datasheet最后一行数据的时间是否与此刻相同
        print(each)
        datasheet_path = contract_path + "/" + each
        print(datasheet_path)
        raw_data = pd.read_csv(datasheet_path)
        latest_data_time_str = raw_data.iloc[-1]["Date"]
        latest_data_time_unix = transform_datestr_to_dateunix(latest_data_time_str,"%Y-%m-%d %H:%M:%S") * 1000;
        print("latest_data_time_unix:",latest_data_time_unix)
        print("latest_data_time_str:",latest_data_time_str)
        barinterval = each[-7:-4]
        barinterval = check_bar_interval(barinterval)
        print("barinterval:",barinterval)
        bar_interval_unix = check_bar_interval_unix(barinterval)
        print("bar_interval_unix:",bar_interval_unix)
        now_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_time_unix = transform_datestr_to_dateunix(now_time_str,"%Y-%m-%d %H:%M:%S") * 1000;
        print("now_time_unix:",now_time_unix,"now_time_str:",now_time_str)
             
        if check_date(latest_data_time_unix,now_time_unix,barinterval):
            print("文件 %s 需要更新数据！" %(each))
            print(contract_name,barinterval,latest_data_time_unix,now_time_unix);
            new_data = um_futures_client.klines(symbol=contract_name,interval= barinterval,start_Time = latest_data_time_unix,endTime = now_time_unix)
            for i in range(0,len(new_data)):
                new_data_time_unix = new_data[i][0]
                if(new_data_time_unix >= latest_data_time_unix + bar_interval_unix):
                    #开始记录数据
                    for i in range(i,len(new_data)-1):
                        record_date_list.append(new_data[i][1:6])
                        record_data_index_str = transform_unixtime_to_datetime(new_data[i][0])
                        record_data_index_list.append(record_data_index_str)
                    print("开始更新数据")
                    new_data = pd.DataFrame(data = record_date_list,columns=["Open","High","Low","Close","Volume"],index=record_data_index_list)
                    print(new_data)
                    new_data.to_csv(datasheet_path,header = False ,mode = "a+")
                    print("更新数据成功!\n");
                    record_date_list = [];
                    record_data_index_list = [];
                    record_data_index_str = [];

                    break;
        else:
            print("无需更新数据!")

Program_End_Time = time.time();
Program_Total_Time = Program_End_Time - Program_Start_Time;
print("程序运行总时长:",Program_Total_Time,"s");

    





