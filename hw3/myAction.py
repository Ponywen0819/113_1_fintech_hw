import numpy as np
from enum import Enum


class Action(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0


# A DP-based approach to obtain the optimal return
def myAction01(priceMat, transFeeRate):
    dataLen, stockCount = priceMat.shape
    initial_cash = 1000.0

    # dp[i][j] 表示第i天持有資產j的最大價值 (j=0表示現金, j=1~stockCount表示股票)
    dp = np.zeros((dataLen, stockCount + 1))
    prev_state = np.zeros((dataLen, stockCount + 1), dtype=int)
    # 初始狀態
    dp[0][0] = initial_cash

    # 動態規劃主循環
    for day in range(1, dataLen):
        best_cash_value, best_stock = get_bast_cash(dp, day, priceMat, transFeeRate)
        dp[day][0] = best_cash_value
        prev_state[day][0] = best_stock

        # 更新持有股票的情況
        for stock in range(stockCount):
            best_stock_value, best_stock = get_best_stock(dp, day, priceMat, transFeeRate, stock)
            dp[day][stock + 1] = best_stock_value / priceMat[day][stock]
            prev_state[day][stock + 1] = best_stock

    # 找出最後一天的最佳狀態
    best_value = dp[dataLen - 1][0]
    best_state = 0

    for stock in range(stockCount):
        value = dp[dataLen - 1][stock + 1] * priceMat[dataLen - 1][stock]
        if value > best_value:
            best_value = value
            best_state = stock + 1

    # 回溯構建交易序列
    actionMat = []
    curr_state = best_state

    # 回溯其他交易
    for day in range(dataLen - 1, -1, -1):
        next_state = curr_state
        curr_state = prev_state[day][next_state]

        if curr_state != next_state:
            sell_to = -1
            buy_from = -1
            equivalent = 0

            if curr_state != 0 and next_state != 0 and curr_state != next_state:
                sell_to = next_state - 1
                buy_from = curr_state - 1
                equivalent = dp[day - 1][curr_state] * priceMat[day][curr_state - 1]
            elif curr_state != 0 and next_state == 0:
                buy_from = curr_state - 1
                equivalent = dp[day - 1][curr_state] * priceMat[day][curr_state - 1]
            elif curr_state == 0 and next_state != 0:
                sell_to = next_state - 1
                equivalent = dp[day - 1][curr_state]

            actionMat.append([int(day), int(buy_from), int(sell_to), float(equivalent)])
    # 反轉使其按時間順序排列
    actionMat.reverse()

    return actionMat


def get_bast_cash(dp, d, priceMat, transFeeRate):
    stock_count = priceMat.shape[1]
    transRate = (1 - transFeeRate)

    possible_choice = []
    # 繼續持有
    possible_choice.append(dp[d - 1][0])

    # 賣出股票
    for i in range(1, stock_count + 1):
        stock_price = priceMat[d][i - 1]
        cash = dp[d - 1][i] * stock_price * transRate
        possible_choice.append(cash)

    bast_value = max(possible_choice)
    best_stock = possible_choice.index(bast_value)

    return bast_value, best_stock


def get_best_stock(dp, d, priceMat, transFeeRate, stock_index):
    stock_count = priceMat.shape[1]
    transRate = (1 - transFeeRate)

    possible_choice = []
    # 現金買入
    current_stock_price = priceMat[d][stock_index]
    cash = dp[d - 1][0]
    stock_value = cash * transRate
    possible_choice.append(stock_value)

    for stock in range(stock_count):
        # 持續持有
        if stock == stock_index:
            possible_choice.append(dp[d - 1][stock + 1] * current_stock_price)
            continue

        other_stock_price = priceMat[d][stock]
        equivalent_cash = dp[d - 1][stock + 1] * other_stock_price * transRate * transRate

        possible_choice.append(equivalent_cash)

    best_value = max(possible_choice)
    best_stock = possible_choice.index(best_value)

    return best_value, best_stock


def myAction02(priceMat, transFeeRate, K):
    dataLen, stockCount = priceMat.shape
    initial_cash = 1000.0

    # dp[i][j] 表示第i天持有資產j的最大價值 (j=0表示現金, j=1~stockCount表示股票)
    dp = np.zeros((dataLen, stockCount + 1, K * 2))
    prev_state = np.zeros((dataLen, stockCount + 1, K * 2, 2), dtype=int)

    # 初始狀態
    dp[0][0][0] = initial_cash

    for stock in range(stockCount):
        dp[0][stock + 1][0] = initial_cash / priceMat[0][stock]
        prev_state[0][stock + 1][0][0] = 0

    # 動態規劃主循環
    for day in range(1, dataLen):
        # 更新持有現金的情況
        for k in range(K):
            if k > day: continue
            best_cash_value, best_stock = get_best_cash_2(dp, day, priceMat, transFeeRate, k, K)
            next_k = k + 1 if best_stock == 0 else k

            if best_cash_value > dp[day][0][next_k]:
                dp[day][0][next_k] = best_cash_value
                prev_state[day][0][next_k][0] = k
                prev_state[day][0][next_k][1] = best_stock

        # 更新持有股票的情況
        for stock in range(stockCount):
            for k in range(K):
                if k > day: continue
                best_stock_value, best_stock = get_best_stock_2(dp, day, priceMat, transFeeRate, k, K - 1, stock)
                next_k = k + 1 if best_stock == 0 else k

                if (best_stock_value / priceMat[day][stock]) > dp[day][stock + 1][next_k]:
                    dp[day][stock + 1][next_k] = best_stock_value / priceMat[day][stock]
                    prev_state[day][stock + 1][next_k][0] = k
                    prev_state[day][stock + 1][next_k][1] = best_stock

    best_value = 0
    best_state = 0
    best_k = 0

    for k in range(K, K * 2):
        v = dp[dataLen - 1][0][k]
        if v > best_value:
            best_value = v
            best_state = 0
            best_k = k

    for stock in range(stockCount):
        for k in range(K, K * 2):
            v = dp[dataLen - 1][stock + 1][k] * priceMat[dataLen - 1][stock]
            if v > best_value:
                best_value = v
                best_state = 0
                best_k = k

    # 回溯構建交易序列
    actionMat = []
    curr_state = best_state
    curr_k = best_k

    # 回溯其他交易
    for day in range(dataLen - 1, -1, -1):
        next_state = curr_state
        next_k = curr_k

        curr_state = prev_state[day][next_state][next_k][1]
        curr_k = prev_state[day][next_state][next_k][0]

        if curr_state != next_state:
            sell_to = -1
            buy_from = -1
            equivalent = 0

            if curr_state != 0 and next_state != 0 and curr_state != next_state:
                sell_to = next_state - 1
                buy_from = curr_state - 1
                equivalent = dp[day - 1][curr_state][curr_k] * priceMat[day][curr_state - 1]
            elif curr_state != 0 and next_state == 0:
                buy_from = curr_state - 1
                equivalent = dp[day - 1][curr_state][curr_k] * priceMat[day][curr_state - 1]
            elif curr_state == 0 and next_state != 0:
                sell_to = next_state - 1
                if (day == 0):
                    equivalent = dp[0][curr_state][curr_k]
                else:
                    equivalent = dp[day - 1][curr_state][curr_k]

            actionMat.append([int(day), int(buy_from), int(sell_to), float(equivalent)])
    # 反轉使其按時間順序排列
    actionMat.reverse()

    return actionMat


def get_best_cash_2(dp, d, price_mat, trans_fee_rate, k, k_max):
    possible_choice = []
    stock_count = price_mat.shape[1]

    for stock in range(stock_count):
        stock_value = dp[d - 1][stock + 1][k] * price_mat[d][stock] * (1 - trans_fee_rate)
        possible_choice.append(stock_value)

    if k < (k_max * 2 - 1):
        possible_choice.append(dp[d - 1][0][k])

    best_value = max(possible_choice)
    best_stock = possible_choice.index(best_value)

    if best_stock == stock_count:
        best_stock = 0
    else:
        best_stock += 1

    return best_value, best_stock


def get_best_stock_2(dp, d, price_mat, trans_fee_rate, k, k_max, stock_index):
    possible_choice = []
    stock_count = price_mat.shape[1]

    for stock in range(stock_count):
        stock_value = dp[d - 1][stock + 1][k] * price_mat[d][stock] * (1 - trans_fee_rate)
        if stock == stock_index:
            stock_value /= (1 - trans_fee_rate)
        possible_choice.append(stock_value)

    if k < (k_max * 2 - 1):
        possible_choice.append(dp[d - 1][0][k] * (1 - trans_fee_rate))

    best_value = max(possible_choice)
    best_stock = possible_choice.index(best_value)

    if best_stock == stock_count:
        best_stock = 0
    else:
        best_stock += 1

    return best_value, best_stock


# An approach that allow consecutive K days to hold all cash without any stocks
def myAction03(priceMat, transFeeRate, K):
    actionMat = []
    return actionMat
