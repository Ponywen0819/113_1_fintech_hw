from typing import List
from scipy.optimize import fsolve, root


def genNpvCalcuator(cashFlowVec: List[float], cashFlowPeriod: int, compoundPeriod: int):
    ratio = cashFlowPeriod / compoundPeriod

    def npv(r: int):
        num = 0
        for i, cash in enumerate(cashFlowVec):
            current_rate = (1 + (r / ratio)) ** (ratio * i)
            num += (cash / current_rate)
        return num

    return npv


def irrFind(cashFlowVec: List[float], cashFlowPeriod: int, compoundPeriod: int):
    npvCalcuator = genNpvCalcuator(cashFlowVec, cashFlowPeriod, compoundPeriod)
    res = root(npvCalcuator, 0.01)
    min_num = 1
    for num in res['x']:
        if  num < min_num:
            min_num = num
    return min_num * ( 12 / cashFlowPeriod)


if __name__ == "__main__":
    input_line = "100 -210 130 -250 120 -220 400 12 1"
    input_numbers = [int(x) for x in input_line.strip().split()]
    cashFlowPeriod, compoundPeriod = input_numbers[-2:]
    cashFlowVec = input_numbers[:-2]
    irr = irrFind(cashFlowVec, cashFlowPeriod, compoundPeriod)
    print(f'{round(irr * 100, 4):.4f}')  # IRR in percentage
