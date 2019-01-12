import datetime
import numpy as np
import statsmodels.api as sm
import sklearn.linear_model as lm


def get_period_dataframe(current, period, dataframe):
    return dataframe.loc[current:current - datetime.timedelta(period), :]


def find_co(dataframe):
    df_length = dataframe.shape[1]
    keys = dataframe.columns

    pvalue_mat = np.ones((df_length, df_length))
    str_pairs = []
    for i in range(df_length):
        stock1 = dataframe[keys[i]]
        for j in range(i+1, df_length):
            stock2 = dataframe[keys[j]]
            pvalue = sm.tsa.stattools.coint(stock1, stock2)[1]
            pvalue_mat[i, j] = pvalue
            if pvalue < 0.05:
                str_pairs.append((keys[i], keys[j], pvalue))
    return pvalue_mat, str_pairs


def select_str(pvalue_mat, str_pairs):
    '''this funciton is used to select the most '''
    p_min = np.min(pvalue_mat)
    for i in str_pairs:
        if i[2] == p_min:
            return i
    print("无强协整关系")
    return None

#cython : vectorize, speed up the entire changing
# we are suppoosed to use to cython package here to somehow reduce the computational time
# even though we have no clue why it works


def find_relation(pair, dataframe):
    y = np.array(dataframe[pair[1]])
    x = np.array(dataframe[pair[0]]).reshape(-1, 1)
    lm_model = lm.LinearRegression()
    lm_model.fit_intercept = True

    lm_model.fit(x, y)
    y_hat = lm_model.predict(x)
    mean = np.mean(y - y_hat)
    std = np.std(y - y_hat)
    return lm_model.coef_, lm_model.intercept_, mean, std


def cal_res(coef, intercept, x, y):
    return y - x*coef - intercept


def z_score(residaul, mean, std):
    return (residaul - mean) / std


def signal(threshold, zscore):
    if zscore >= threshold:
        # 建仓
        print('y正建仓')
        return True
    elif zscore <= -threshold:
        # 建仓
        print('y负建仓')
        return False
    else:
        print('不建仓')
        # 不建仓
        return None


def close_signal(threshold_low, threshold_high, zscore):
    if abs(zscore) <= threshold_low:
        # 收敛清仓
        print("收敛清仓")
        return True
    elif abs(zscore) >= threshold_high:
        print("发散清仓")
        return False
    else:
        return None
