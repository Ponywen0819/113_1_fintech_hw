import sys
import pandas as pd
from myAction import *
import time
from computeReturnRate import computeReturnRate

# Compute return rate over a given price Matrix & action Matrix


if __name__ == "__main__":
    df = pd.read_csv('priceMat0992.txt', delimiter=' ', header=None)
    transFeeRate = 0.01  # Rate for transaction fee
    priceMat = df.values

    K = 0
    problem_type = 1
    # print("------------Problem 1-------------")
    # start = time.time()
    # actionMat = myAction01(priceMat, transFeeRate)  # Obtain the suggested action
    # rr, cashHolding, cash_longest_day = computeReturnRate(priceMat, transFeeRate, actionMat, K,
    #                                                       problem_type)  # Compute return rate
    # end = time.time()
    # print("Time:", end - start)
    # print("rr=%f%%" % (rr * 100))
    # print("Non continueous cash holding=%d" % (cashHolding))
    # print("Continueous cash holding=%d" % (cash_longest_day))
    #
    # K_list = [200, 300, 400]
    # problem_type = 2
    # print("------------Problem 2-------------")
    # start = time.time()
    # total_rr = 0
    # for K in K_list:
    #     actionMat = myAction02(priceMat, transFeeRate, K)  # Obtain the suggested action
    #     rr, cashHolding, cash_longest_day = computeReturnRate(priceMat, transFeeRate, actionMat, K,
    #                                                           problem_type)  # Compute return rate
    #     total_rr += rr
    #
    # end = time.time()
    # print("Time:", end - start)
    # print("rr=%f%%" % (total_rr * 100 / 3))
    # print("Non continueous cash holding=%d" % (cashHolding))
    # print("Continueous cash holding=%d" % (cash_longest_day))

    K_list = [200, 300, 400]
    problem_type = 3
    print("------------Problem 3-------------")
    start = time.time()
    total_rr = 0
    for K in K_list:
        actionMat = myAction03(priceMat, transFeeRate, K)  # Obtain the suggested action
        rr, cashHolding, cash_longest_day = computeReturnRate(priceMat, transFeeRate, actionMat, K,
                                                              problem_type)  # Compute return rate
        total_rr += rr

    end = time.time()
    print("Time:", end - start)
    print("rr=%f%%" % (total_rr * 100 / 3))
    print("Non continueous cash holding=%d" % (cashHolding))
    print("Continueous cash holding=%d" % (cash_longest_day))
