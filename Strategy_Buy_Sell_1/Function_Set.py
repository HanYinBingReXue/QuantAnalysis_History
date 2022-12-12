import pandas as pd

def normalized(Price):
    Price = (Price - Price.min()) / (Price.max() - Price.min());
    return Price

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
def slope_cal(normalized_date, MA_data, MA_NUM):
    slope = []
    for n in range(0, len(MA_data)):
        slope.append(normalized_date[n + MA_NUM - 1] - MA_data[n]);
    return slope;

def step_normalized(df):
    step_normalized = [];
    for i in range(0,len(df)):
        if df[i-1] <= df[i]:
            step_normalized.append(1);
        elif df[i-1] > df[i]:
            step_normalized.append(0);
    return step_normalized;
