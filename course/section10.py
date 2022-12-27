import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.svm import LinearSVC, SVC
import pandas as pd
import numpy as np
import datetime
def create_lagged_series(df,lags = 5):
    # Create the new lagged DataFrame
    dflag = pd.DataFrame(index=df.index)
    dflag["Today"] = df["Close"]
    dflag["Volume"] = df["Volume"]
    # Create the shifted lag series of prior trading period close values
    for i in range (0,lags):
        dflag["Lag%s" % str(i+1)] = df["Close"].shift(i+1) 
        dfret = pd.DataFrame(index = dflag.index)
        dfret["Volume"] = dflag["Volume"]
        dfret["Today"] = dflag["Today"].pct_change()
    for i,x in enumerate(dfret["Today"]):
        if(abs(x)) < 0.0001:
            dfret["Today"][i] = 0.0001
            # Create the lagged percetage returns columns
    for i in range(0,lags):
        dfret["Lag%s" %str(i+1)] = \
        dflag["Lag%s" %str(i+1)].pct_change()*100.0
        # Create the Direction Colimn(+1 or -1) indicating an up/down day
    dfret["Direction"] = np.sign(dfret["Today"])
    dfret = dfret[dfret.index >= df.iloc[0].name]
    return dfret

if __name__ == "__main__":
    # Create a lagged series
    Path = "/Users/han/Crypto/QuantAnalysis/binance_api/Future_Data/ETHUSDT/ETHUSDT_1m.csv"
    raw_data = pd.read_csv(Path,index_col=0)
    # print(raw_data.iloc[0].name)
    snpret = create_lagged_series(raw_data[207400:])
    snpret = snpret.fillna(0)
    # print(snpret)
    # print(snpret)
    # # Use the prior two days of returns as predictor
    # # values, with direction as the reponse
    X = snpret[["Lag1","Lag2"]]
    Y = snpret["Direction"]
    # # The test data is split into two pairs: Before and after 2022-12-20 00:00:00
    start_test = "2022-12-24 00:00:00"
    # # Create training and test sets
    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    Y_train = Y[Y.index < start_test]
    Y_test = Y[Y.index >= start_test]
    # Create the  (parametrised) models
    print("Hit Rates/Confusion Matrices: \n")
    models = [("LR",LogisticRegression(
        penalty="l2",dual=False,tol=0.0001,
        C = 1.0,fit_intercept=True,intercept_scaling=1,class_weight=None,random_state=None,
        solver="liblinear",max_iter=100,multi_class="ovr",verbose=0,warm_start=False,n_jobs=1
    )),
    ("LDA",LDA(solver="svd",shrinkage=None,priors=None,n_components=None,store_covariance=False,tol=0.0001)),
    # ("QDA",QDA()),
    ("LSVC",LinearSVC()),
    ("RSVM",SVC(
        C = 1000.0,cache_size=200,class_weight=None,
        coef0=0.0,degree=3,gamma=0.0001,kernel="rbf",
        max_iter= -1,probability=False,random_state=None,
        shrinking=True,tol= 0.001,verbose=False
    )),
    ("RF",RandomForestClassifier(
        n_estimators=1000,criterion="gini",
        max_depth=None,min_samples_split=2,
        min_samples_leaf=1,
        bootstrap= True,oob_score=False,n_jobs=1,
        random_state=None,verbose=0
    ))]

    # Iterate through the models
    for m in models:
        # Train each of the models on the training set
        m[1].fit(X_train,Y_train)
        # Make an array of predictions on the test set
        pred = m[1].predict(X_test)
        # Output the hit-rate and the confusion matrix for each model
        print("%s:\n%0.3f" %(m[0],m[1].score(X_test,Y_test)))
        print("%s\n" % confusion_matrix(pred,Y_test))