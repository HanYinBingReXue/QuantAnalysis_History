import gate_api
import time
from Config import *
from pprint import pprint
from datetime import datetime
import random
import pandas as pd
# pd setting 显示完全
#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);
Max_Bar_Num = 300;


def get_history_data(from_time_unix,to_time_unix,contract,settle,bar_interval):
# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.
    configuration = gate_api.Configuration(
        host = "https://api.gateio.ws/api/v4",
        key = Gate_API1_Public_Key,
        secret = Gate_API1_Private_Key,
    )
# Configure APIv4 key authorization
    api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
    api_instance = gate_api.FuturesApi(api_client)
    print("Logged in Successfully!")
    print("Getting history raw future data....")
    history_close_price = [];
    history_high_price = [];
    history_low_price = [];
    history_open_price = [];
    history_timestamp = [];
    history_volume = [];
    
    print("Settle Currency: %s" % settle);
    print("Contract: %s" % contract);
    #limit = 100 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
    print("Interval: %s" % bar_interval);
    to_time_str = datetime.utcfromtimestamp(to_time_unix).strftime('%Y-%m-%d %H:%M:%S');
    from_time_str = datetime.utcfromtimestamp(from_time_unix).strftime('%Y-%m-%d %H:%M:%S');
    print("Time: %s  %s" % (from_time_str , to_time_str ));
        
    if "s" in bar_interval:
        bar_interval_value = int(bar_interval.replace("s",""))
        total_bar_number = (to_time_unix - from_time_unix) / bar_interval_value;
        [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
        each_bar_interval = bar_interval_value;

    if "m" in bar_interval:
        bar_interval_value = int(bar_interval.replace("m",""))
        total_bar_number = (to_time_unix - from_time_unix)/ 60 / bar_interval_value;
        [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
        each_bar_interval = bar_interval_value * 60;

    if "h" in bar_interval:
        bar_interval_value = int(bar_interval.replace("h",""))
        total_bar_number = (to_time_unix - from_time_unix)/ 60 / 60 / bar_interval_value;
        [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
        each_bar_interval = bar_interval_value * 60 * 60;
    
    if "d" in bar_interval:
        bar_interval_value = int(bar_interval.replace("d",""))
        total_bar_number = (to_time_unix - from_time_unix)/ 60 / 60 / 24 / bar_interval_value;
        [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
        each_bar_interval = bar_interval_value * 60 * 60 * 24;


    if "w" in bar_interval:
        bar_interval_value = int(bar_interval.replace("w",""))
        total_bar_number = (to_time_unix - from_time_unix)/ 60 / 60 / 24 / 7 / bar_interval_value;
        [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
        each_bar_interval = bar_interval_value * 60 * 60 * 24 * 7;
   
    for i in range(0,int(total_require_number)):
        print("%s / %s" %(i , total_require_number))
        _from = (from_time_unix + i * Max_Bar_Num * bar_interval_value * each_bar_interval);
        _to = (from_time_unix + (i+1) * Max_Bar_Num * bar_interval_value * each_bar_interval);
        api_response = api_instance.list_futures_candlesticks(settle, contract, _from=_from, to=_to, interval=bar_interval)
        for each in  api_response:
            history_close_price.append(each.c);
            history_high_price.append(each.h);
            history_low_price.append(each.l);
            history_open_price.append(each.o);
            history_volume.append(each.v); 
            TimeIndex = datetime.utcfromtimestamp(each.t).strftime('%Y-%m-%d %H:%M:%S')
            history_timestamp.append(TimeIndex);  
    
    _from = to_time_unix - left_number * each_bar_interval
    api_response = api_instance.list_futures_candlesticks(settle, contract, _from=_from, to=to_time_unix, interval=bar_interval)
    for each in  api_response:
            history_close_price.append(each.c);
            history_high_price.append(each.h);
            history_low_price.append(each.l);
            history_open_price.append(each.o);
            history_volume.append(each.v); 
            TimeIndex = datetime.utcfromtimestamp(each.t).strftime('%Y-%m-%d %H:%M:%S')
            history_timestamp.append(TimeIndex); 

    d = {'Open': history_open_price,'High': history_high_price,'Low': history_low_price,'Close': history_close_price,'Volume':history_volume}
    df = pd.DataFrame(data=d,index=history_timestamp)
    # print(df)
    print("Get Data Successfully!")
    return df;

def transform_datestr_to_dateunix(str_date,format):
    if format == "%Y-%m-%d %H:%M:%S":
        unix_date = int(time.mktime(datetime.strptime(str_date, format).timetuple()))
    return unix_date

def check_date(latest_data_time_unix,now_time_unix,barinterval):
    time_interval = now_time_unix - latest_data_time_unix;
    if "m" in barinterval:
        time_bar = 60 * int(barinterval[0]);
    if "h" in barinterval:
        time_bar = 60 * 60 * int(barinterval[0]);
    if "d" in barinterval:
        time_bar = 60 * 60 * 24 * int(barinterval[0]);
    if "w" in barinterval:
        time_bar = 60 * 60 * 24 * 7 * int(barinterval[0]);
    if time_interval > time_bar:
        print("%s 需要更新数据！" % barinterval)
        return 1;
    else:
        print("%s 无需更新数据!" % barinterval)
        return 0;
