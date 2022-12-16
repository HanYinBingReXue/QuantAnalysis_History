from Function_Set import *
#Modify Path
os.chdir("/Users/han/Crypto/QuantAnalysis_History_ETH/Strategy_Buy_Sell_1")
current_directory = os.getcwd()
#pd setting 显示完全
#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);