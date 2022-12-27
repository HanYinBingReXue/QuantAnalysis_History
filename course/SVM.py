import pandas as pd
from sklearn import svm,preprocessing
import matplotlib.pyplot as plt

#显示所有行
pd.set_option("display.max_columns",None);
#显示所有列
pd.set_option("display.max_rows",None);
#设置Value的显示长度为100，默认为50
pd.set_option("display.width", None);
pd.set_option("display.max_colwidth", None);

Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/ETHUSDT/ETHUSDT_5m.csv"
raw_data = pd.read_csv(Path,index_col=0)
raw_data = raw_data[:]

# diff列表示本日和上日收盘价的差
raw_data["Diff"] = raw_data["Close"] - raw_data["Close"].shift(1)
raw_data["Diff"].fillna(0,inplace=True)

raw_data["Up"] = raw_data["Diff"]
raw_data["Up"][raw_data["Diff"]>0] = 1;
raw_data["Up"][raw_data["Diff"]<0] = 0;
#预测值暂且初始化为0
raw_data['predictForUp'] = 0
#目标值是真实的涨跌情况
target = raw_data['Up']
length=len(raw_data)
trainNum=int(length*0.8)
predictNum=length-trainNum
#选择指定列作为特征列
feature=raw_data[['Open', 'High', 'Low','Close' ,'Volume']]
#标准化处理特征值
feature=preprocessing.scale(feature)

#训练集的特征值和目标值
featureTrain=feature[1:trainNum-1]
targetTrain=target[1:trainNum-1]
svmTool = svm.SVC(kernel='linear')
svmTool.fit(featureTrain,targetTrain)



predictedIndex=trainNum
predict_list = [];
#逐行预测测试集
while predictedIndex<length:
    print(predictedIndex,"/",length)
    testFeature=feature[predictedIndex:predictedIndex+1]           
    predictForUp=svmTool.predict(testFeature)  
    # print(predictForUp) 
    predict_list.append(predictForUp[0])  
    predictedIndex = predictedIndex+1
predict_list = [0.0] * trainNum + predict_list;
raw_data['predictForUp']=predict_list 
# print(raw_data[trainNum:]['predictForUp'])
count = 0;
for i in range(trainNum,length,1):
    if raw_data.iloc[i]["Up"] == raw_data.iloc[i]["predictForUp"]:
        count += 1;
print("正确率:",count/(length-trainNum))


#该对象只包含预测数据，即只包含测试集
dfWithPredicted = raw_data[trainNum:length]
#开始绘图，创建两个子图
figure = plt.figure()
#创建子图    
(axClose, axUpOrDown) = figure.subplots(2, sharex=True)
dfWithPredicted['Close'].plot(ax=axClose)
dfWithPredicted['predictForUp'].plot(ax=axUpOrDown,color="red", label='Predicted Data')
# dfWithPredicted['Up'].plot(ax=axUpOrDown,color="blue",label='Real Data')
plt.legend(loc='best') #绘制图例
#设置x轴坐标标签和旋转角度
# major_index=dfWithPredicted.index[dfWithPredicted.index%2==0]
# major_xtics=dfWithPredicted['Date'][dfWithPredicted.index%2==0]
# plt.xticks(major_index,major_xtics)
plt.setp(plt.gca().get_xticklabels(), rotation=30)
# plt.title("通过SVM预测603505的涨跌情况")
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.show()