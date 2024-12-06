import sys
import numpy as np
import pandas as pd
from myAction import *
from computeReturnRate import computeReturnRate

if __name__ == "__main__":
    print("Reading %s..." % (sys.argv[1]))
    file = sys.argv[1]  # input file
    df = pd.read_csv(file, delimiter=' ', header=None)
    transFeeRate = float(sys.argv[2])  # Rate for transaction fee
    priceMat = df.values  # Get price as the m×n matrix which holds n stocks' price over m days
    actionMat = myActionSimple(priceMat, transFeeRate)  # Obtain the suggested action
    rr = computeReturnRate(priceMat, transFeeRate, actionMat)  # Compute return rate
    print("rr=%f%%" % (rr * 100))
