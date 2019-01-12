import pandas as pd
import datetime

data = pd.read_csv('./中信传媒行业收盘价.csv', index_col=0, skiprows = 1, encoding = 'ISO-8859-1')

data = pd.read_csv('./中信传媒行业收盘价.csv', skiprows = 1, encoding = 'ISO-8859-1')
data.index = [datetime.date(int(i.split('/')[0]), int(i.split('/')[1]), int(i.split('/')[2])) for i in data.iloc[:,0]]
data.drop(columns=data.iloc[:,0].name, inplace= True)
