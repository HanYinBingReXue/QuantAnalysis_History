import time
from pprint import pprint
from datetime import datetime
import pandas as pd
from config import *
from binance.um_futures import UMFutures
import os

from datetime import timezone
# pd setting 显示完全
#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);
Max_Bar_Num = 500; #最大500 如果多了会可能数据显示不完全
MAX_Storage_Num = 5000;

um_futures_client = UMFutures(key=API_public_key, secret=API_secret_key);
def get_history_data(from_time_unix,to_time_unix,contract,settle,bar_interval):
    print("Getting history raw future data....")
    history_close_price = [];
    history_high_price = [];
    history_low_price = [];
    history_open_price = [];
    history_timestamp = [];
    history_volume = [];
    bar_interval_value_unix = 0;
    print("Settle Currency: %s" % settle);
    print("Contract: %s" % contract);
    #limit = 100 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
    print("Interval: %s" % bar_interval);
    to_time_str = transform_unixtime_to_datetime(to_time_unix);
    from_time_str = transform_unixtime_to_datetime(from_time_unix);
    print("Time: %s to %s" % (from_time_str , to_time_str ));
    print("to_time_unix:",to_time_unix,"from_time_unix:",from_time_unix,"bar_interval:",bar_interval)
    bar_interval_value_unix = check_bar_interval_unix(bar_interval)
    total_bar_number = int((to_time_unix - from_time_unix) / bar_interval_value_unix);
    print("Time interval:",(to_time_unix - from_time_unix),"bar_interval_value_unix:",bar_interval_value_unix)
    [total_require_number, left_number] = divmod(total_bar_number,Max_Bar_Num)
    print("total_bar_number:",total_bar_number)
    print("total_require_number:",total_require_number)
    print("left_number:",left_number)
    
    
    if(total_require_number >= MAX_Storage_Num):
        print("数据量过大！")
        from_time_unix = to_time_unix - (MAX_Storage_Num * bar_interval_value_unix);
        total_require_number = MAX_Storage_Num;
        for i in range(0,int(total_require_number)):
            print("%s / %s" %(i , total_require_number))
            # 每次取Max_Bar_Num个bar
            _from = (from_time_unix + i * Max_Bar_Num * bar_interval_value_unix);
            _to = (from_time_unix + (i+1) * Max_Bar_Num * bar_interval_value_unix);
            data = um_futures_client.klines(symbol = contract,interval = bar_interval,startTime = _from,endTime = _to)
            for i in  range(0, len(data) - 1) :
                history_open_price.append(data[i][1]);
                history_high_price.append(data[i][2]);
                history_low_price.append(data[i][3]);
                history_close_price.append(data[i][4]);
                history_volume.append(data[i][5]); 
                TimeIndex = datetime.fromtimestamp(data[i][0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                history_timestamp.append(TimeIndex);  
    else:
        for i in range(0,int(total_require_number)):
            print("%s / %s" %(i , total_require_number))
            _from = (from_time_unix + i * Max_Bar_Num *bar_interval_value_unix);
            _to = (from_time_unix + (i+1) * Max_Bar_Num * bar_interval_value_unix);
            data = um_futures_client.klines(symbol = contract, interval = bar_interval,startTime = _from,endTime = _to)
            for i in  range(0, len(data)) :
                history_open_price.append(data[i][1]);
                history_high_price.append(data[i][2]);
                history_low_price.append(data[i][3]);
                history_close_price.append(data[i][4]);
                history_volume.append(data[i][5]); 
                TimeIndex = datetime.fromtimestamp(data[i][0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                history_timestamp.append(TimeIndex);  
        _from = to_time_unix - left_number * bar_interval_value_unix
        data = um_futures_client.klines(symbol = contract, interval = bar_interval,startTime = str(_from),endTime = str(to_time_unix))
        for i in  range(0, len(data) - 1) :
                history_open_price.append(data[i][1]);
                history_high_price.append(data[i][2]);
                history_low_price.append(data[i][3]);
                history_close_price.append(data[i][4]);
                history_volume.append(data[i][5]); 
                TimeIndex = datetime.fromtimestamp(data[i][0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
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

def check_bar_interval(bar_interval):
    if "_" in bar_interval:
        bar_interval = bar_interval.replace("_","");
    return bar_interval;

def check_bar_interval_value(bar_interval):
    barintervalvalue  = 0;
    if "_" in bar_interval:
        bar_interval = bar_interval.replace("_","")
    if "m" in bar_interval:
        barintervalvalue = bar_interval.replace("m","")
    if "h" in bar_interval:
        barintervalvalue = bar_interval.replace("h","")
    if "d" in bar_interval:
        barintervalvalue = bar_interval.replace("d","")
    if "w" in bar_interval:
        barintervalvalue = bar_interval.replace("w","")
    return int(barintervalvalue)

def check_bar_interval_unit(bar_interval):
    unit = bar_interval[-1]
    return unit;

def check_bar_interval_unix(bar_interval):
    barintervalvalue = 0;
    barintervalunit = 0;
    bar_interval_unix = 0;
    barintervalvalue =  check_bar_interval_value(bar_interval);
    barintervalunit =  check_bar_interval_unit(bar_interval)
    if barintervalunit == "m":
        bar_interval_unix = barintervalvalue * 60 * 1000;
    if barintervalunit == "h":
        bar_interval_unix = barintervalvalue * 60 * 60 * 1000;
    if barintervalunit == "d":
        bar_interval_unix = barintervalvalue * 60 * 60 * 24 * 1000;
    if barintervalunit == "w":
        bar_interval_unix = barintervalvalue * 60 * 60 * 24 * 7* 1000;
    return bar_interval_unix;

def check_date(latest_data_time_unix,now_time_unix,barinterval):
    time_interval = (now_time_unix - latest_data_time_unix);
    
    print("time_interval:",time_interval);
    barintervalvalue = check_bar_interval_value(barinterval);
    print(barintervalvalue)

    if "m" in barinterval:
        time_bar = 60 * int(barintervalvalue) * 1000;
    if "h" in barinterval:
        time_bar = 60 * 60 * barintervalvalue * 1000;
    if "d" in barinterval:
        time_bar = 60 * 60 * 24 * barintervalvalue * 1000;
    if "w" in barinterval:
        time_bar = 60 * 60 * 24 * 7 * barintervalvalue * 1000;
    print(time_bar)
    if time_interval > 2 * time_bar:
        print("%s 需要更新数据！" % barinterval)
        return 1;
    else:
        print("%s 无需更新数据!" % barinterval)
        return 0;


def update_data():
    Path = "/Users/han/Crypto/QuantAnalysis/Data"
    contract_list = os.listdir("/Users/han/Crypto/QuantAnalysis/Data")


    # print(contract_list)
    for i in range (0,len(contract_list)):
        contract = contract_list[i] #选择一个合约
        contract_path = Path + "/" + contract_list[i] #选择合约的路径
        datasheet = os.listdir(contract_path) #选择合约路径下的历史数据
        # print(datasheet)
        for each in datasheet: #查询每个datasheet最后一行数据的时间是否与此刻相同
            
            datasheet_path = contract_path + "/" + each
            raw_data = pd.read_csv(datasheet_path)
            latest_data_time_str = raw_data.iloc[-1]["Date"]
            latest_data_time_unix = transform_datestr_to_dateunix(latest_data_time_str,"%Y-%m-%d %H:%M:%S")
            now_time_str = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            now_time_unix = transform_datestr_to_dateunix(now_time_str,"%Y-%m-%d %H:%M:%S")
            if(latest_data_time_str != now_time_str):
                print("文件 %s 需要更新数据！" %(each))
    #             #开始时间，结束时间，合约名称，pair，barinterval
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

def transform_unixtime_to_datetime(unixtime):
    if unixtime > 1e11:
        unixtime = unixtime / 1000;
    unixtime = datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S');
    return unixtime
    