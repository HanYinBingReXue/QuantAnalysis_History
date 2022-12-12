import pandas as pd

# create a sample data frame
data = {"Date": ["2022-01-01", "2022-01-02", "2022-01-03"],
        "Open": [100, 101, 99],
        "High": [105, 103, 102],
        "Low": [95, 99, 97],
        "Adj Close": [104, 102, 101]}
data_df = pd.DataFrame(data)

# rename the columns
data_df = data_df.rename(columns={"Open":"open", "High": "high","Low":"low", "Adj Close" : "close"})

# print the data frame
print(data_df)
