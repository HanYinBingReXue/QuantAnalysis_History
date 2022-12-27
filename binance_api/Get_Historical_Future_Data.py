from function_set import *
# 1200 requests per minute
# 10 orders per second
# 100,000 orders per 24hrs

# 得到所有的合约名称
# info = um_futures_client.exchange_info();
# Future_list = []
# for each in info["symbols"]:
#     Future_list.append(each["pair"])
# contract = Future_list;
contract = ["ETHUSDT"]
now_time_str_utc = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("now_time_str_utc:",now_time_str_utc)
now_time_unix_utc = transform_datestr_to_dateunix(now_time_str_utc,"%Y-%m-%d %H:%M:%S") * 1000; # 13位
bar_interval = ["1m"]
total_file_number = len(contract) * len(bar_interval);
for j in range(0,len(contract)):
    settle = contract[j][-4:];
    for i in range(0,1):
        print("准备读取数据")
        # 起始日期 2022-12-01 00：00:00
        data = get_history_data(1654056000000,now_time_unix_utc,contract[j],settle,bar_interval[i])
        # print(os.listdir("./plot_history_candlestick/ETH_Historical_Data"))
        path = ("/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/%s/" %contract[j])
        folder = os.path.exists(path);
        if not folder:
            os.makedirs(path)
        filename = contract[j] +"_" + str(bar_interval[i]) + ".csv" ;
        path = path + filename;
        print("准备写入文件 %s / %s" %( (j * len(bar_interval) + i) ,total_file_number))
        data.to_csv(path,index_label=("Date"))
        print("写入文件成功！！")