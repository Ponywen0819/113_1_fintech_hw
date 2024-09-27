from typing import List
from scipy.optimize import fsolve


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
    r = fsolve(npvCalcuator, 0.01)
    return r[0]


if __name__ == "__main__":
    input_line = "-16320 -16157 -16157 -16157 -16157 -16157 100000 12 12"
    input_numbers = [int(x) for x in input_line.strip().split()]
    cashFlowPeriod, compoundPeriod = input_numbers[-2:]
    cashFlowVec = input_numbers[:-2]
    irr = irrFind(cashFlowVec, cashFlowPeriod, compoundPeriod)
    print(f'{round(irr * 100, 4):.4f}')  # IRR in percentage
