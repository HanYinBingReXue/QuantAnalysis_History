from Stratagy_Function import *
#Modify Path
os.chdir("/Users/han/Crypto/QuantAnalysis/")
current_directory = os.getcwd()
#pd setting 显示完全
#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);


transaction_state = { 0 : "Waiting",
                      1  :  "Start",
                      -1  :  "End"};                       
transaction_type = {1 : "Long",
                    2 : "Close Long",
                    0 : "Waiting",
                    -1 : "Short",
                    -2 : "Close Short"};     # "1": Buy; "2": 平多 "-1": Short; “-2”：平空 "0": 空仓
