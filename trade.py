from co_intergrated import *
import datetime


def train_mod(start, train_period, dataframe):
    data = get_period_dataframe(start,train_period,dataframe)
    pvalue_mat, str_pairs = find_co(data)
    select = select_str(pvalue_mat, str_pairs)
    stock_x = select[0]
    stock_y = select[1]
    if select is not None:
        coef, intercept, mean, std = find_relation(select, data)
        return coef, intercept, mean, std, stock_x, stock_y
    else:
        train_mod(start + datetime.timedelta(30), train_period, dataframe)


def cal_zscore(date, coef, intercept, mean, std, stock_x, stock_y, dataframe):
    if date not in dataframe.index:
        cal_zscore((date + datetime.timedelta(1), coef, intercept, mean, std, stock_x, stock_y))
    residual = cal_res(coef, intercept, dataframe.loc[date, stock_x], \
                       dataframe.loc[date, stock_y])
    zscore = z_score(residual, mean, std)
    return zscore


def buy(stock_x, stock_y, date, threshold, zscore):
    sign = signal(threshold, zscore)
    global holdings
    if sign == True:
        holdings = True
        #invest.buy(stock_x, dataframe.loc[i,stock_x])
        return (stock_x, date, 'buy')
        #long x short y
    elif sign == False:
        #invest.buy(stock_y, dataframe.loc[i,stock_y])
        holdings = True
        return (stock_y, date, 'buy')
        #short x long y


def close(stock, date, zscore, threshold_low, threshold_high):
    sign = close_signal(threshold_low, threshold_high, zscore)
    if sign is not None:
        global holdings
        holdings = False
        return (stock, date, 'sell')


def trade(start, train_period, trade_period, threshold, trs_low, trs_high, dataframe):
    coef, intercept, mean, std, stock_x, stock_y = train_mod(start, train_period, dataframe)
    global holdings
    holdings = False
    stock = None
    date = start
    command = []

    while date < start + datetime.timedelta(365):
        date += datetime.timedelta(1)
        if date not in dataframe.index:
            continue
        print("date", date)
        print("st_x", stock_x)
        print("st_y", stock_y)

        zscore = cal_zscore(date, coef, intercept, mean, std, stock_x, stock_y, dataframe)
        if holdings == False:
            tem = buy(stock_x, stock_y, date, threshold, zscore)
            counter = 0
            if tem is not None:
                stock = tem[0]
                command.append(tem)

        else:
            if counter >= trade_period:
                tem = (stock, date,'sell')
                command.append(tem)
                return command
            tem = close(stock, date, zscore, trs_low, trs_high)
            counter += 1
            if tem is not None:
                command.append(tem)
                return command
    if holdings:
        command.append((stock, date,'sell'))
    return command


def main(start, end, train_period, trade_period, threshold, trs_low, trs_high, dataframe):
    commands = []
    date = start
    while date < end:
        command = trade(date, train_period, trade_period, threshold, trs_low, trs_high, dataframe)
        commands.extend(command)
        if command == []:
            date += datetime.timedelta(365)
        elif date >= datetime.date(2018,4,20):
            break
        else:
            date = commands[-1][1]
    return commands
