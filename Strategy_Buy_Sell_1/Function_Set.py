import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd;
from datetime import datetime
from pprint import pprint
import os




def normalized(Price): #归一到 【0 1】
    Price = (Price - min(Price)) / (max(Price) - min(Price));
    return Price

def normalized_minus1_to_1(Price):
    Price = Price - np.mean(Price);
    Price = Price / np.max(np.abs(Price))
    return Price;



def add_missing_date(_from,to,df):
    date_range = pd.date_range(start = _from, end = to);
    # Use the 'reindex()' function to add the missing dates to the data frame
    df = df.reindex(date_range)
    # Fill missing values with the previous value
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    #print(df)
    return df;

def moving_average(data, n):
    moving_average_values = []
    for i in range(len(data) - n + 1):
        moving_average_values.append(sum(data[i:i+n]) / n)
    return moving_average_values
#斜率计算
def slope_cal(date, MA_data, MA_NUM):
    slope = []
    for n in range(0, len(MA_data) -1):
        slope.append(date[n + MA_NUM] - MA_data[n]);
    return slope;

def step_normalized(df):
    step_normalized = [];
    for i in range(0,len(df)):
        if df[i-1] <= df[i]:
            step_normalized.append(1);
        elif df[i-1] > df[i]:
            step_normalized.append(0);
    return step_normalized;
