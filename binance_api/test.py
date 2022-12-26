#!/usr/bin/env python
from function_set import *
now_time_str_utc = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
print("now_time_str_utc:",now_time_str_utc)
now_time_unix_utc = transform_datestr_to_dateunix(now_time_str_utc,"%Y-%m-%d %H:%M:%S") * 1000; # 13位
bar_interval = "4h"
contract = "BTCUSDT"
settle = contract[-4:];
data = get_history_data(1669870800000,now_time_unix_utc,"BTCUSDT",settle,bar_interval)
print(data)
# bar_interval = "15m"
# data = get_history_data(1669870800000,now_time_unix_utc,"BTCUSDT",settle,bar_interval)
# print(data)

# data = um_futures_client.klines(symbol = contract,interval = bar_interval,startTime = 1671667200000,endTime = now_time_unix_utc)
# print(data)