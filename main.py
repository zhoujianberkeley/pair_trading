from train import *
from trade import *
import datetime
import pandas as pd


start = datetime.date(2003, 1, 1)
end = datetime.date(2017, 12, 31)
train_period = 365*2
trade_period = 60
threshold = 1.5
trs_low, trs_high = 0.3, 2.5
df = data

commands = main(start, end, train_period, trade_period, threshold, trs_low, trs_high, df)
result = pd.DataFrame(commands)
result.to_csv("comman.csv")
print(commands)
