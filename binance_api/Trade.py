#!/usr/bin/env python
import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from function_set import *
config_logging(logging, logging.DEBUG)


um_futures_client = UMFutures(key=API_public_key, secret=API_secret_key);
Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/ETHUSDT/ETHUSDT_15m.csv"
    
# while(1):
raw_data = pd.read_csv(Path)
latest_data_time_str = raw_data.iloc[-1]["Date"]
latest_data_time_unix = transform_datestr_to_dateunix(latest_data_time_str,"%Y-%m-%d %H:%M:%S") * 1000 \
    - 5 * 60 * 60 * 1000;  
#读日期的时候会自动变成当地的时间，而文件里是utc时间，会多5个小时的时差减5个小时时差
now_time_unix = int(um_futures_client.time()["serverTime"]);
now_time_str = transform_unixtime_to_datetime(now_time_unix);
print(latest_data_time_str,latest_data_time_unix)
print(now_time_str,now_time_unix)
record_date_list = [];
record_data_index_list = [];
# 最新的时间和最新的bar数据的开始时间应该大于15分钟且小于30分钟
# 所以当时差大于30分钟时更新
if(now_time_unix - latest_data_time_unix > 30 * 60 * 1000):
    if check_date(latest_data_time_unix,now_time_unix,"15m"):
        new_data = um_futures_client.klines(symbol="ETHUSDT",interval="15m",start_Time = \
            latest_data_time_unix,endTime = now_time_unix)
        for i in range(0,len(new_data)):
            new_data_time_unix = new_data[i][0];
            # 如果最新的数据时间比文件内的最后一个bar的数据时间多超过15分钟，开始记录数据
            if(new_data_time_unix > latest_data_time_unix + 15 * 60 * 1000):
                #开始记录数据 记录上一个bar的信息，最新的bar才刚开始
                for i in range(i,len(new_data)-1):
                    record_date_list.append(new_data[i][1:6])
                    record_data_index_str = transform_unixtime_to_datetime(new_data[i][0])
                    record_data_index_list.append(record_data_index_str)
                print("开始更新数据")
                new_data = pd.DataFrame(data = record_date_list,columns=["Open","High","Low","Close","Volume"],index=record_data_index_list)
                new_data.to_csv(Path,header = False ,mode = "a")
                print("更新数据成功!");
                break;
    time.sleep(10);

else:
    print("无需更新数据!");
    time.sleep(10);
        



