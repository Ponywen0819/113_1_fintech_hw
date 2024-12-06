from enum import Enum
import numpy as np
import pandas as pd


class Action(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0


class Strategy():
    def __init__(self,
                 bollinger={'windowSize': 3, 'k': 0.1, 'std': 1},
                 macd={'windowFast': 3, 'windowSlow': 5, 'windowSignal': 3},
                 ):
        # bollinger
        self.bollingerWindowSize = bollinger['windowSize']
        self.bollingerK = bollinger['k']
        self.bollingerStd = bollinger['std']

        # MACD
        self.macdWindowFast = macd['windowFast']
        self.macdWindowSlow = macd['windowSlow']
        self.macdWindowSignal = macd['windowSignal']

    def calculate_ma(self, vec, window):
        if len(vec) < window:
            return np.mean(vec)
        else:
            return np.mean(vec[-window:])

    def bollinger(self, price_vec):
        window = self.bollingerWindowSize
        num_std = self.bollingerStd
        bb_mavg = self.calculate_ma(price_vec, window)
        bb_std = np.std(price_vec[-window:])
        bb_bbh = bb_mavg + num_std * bb_std
        bb_bbl = bb_mavg - num_std * bb_std
        return {
            'bb_mavg': bb_mavg,
            'bb_std': bb_std,
            'bb_bbh': bb_bbh,
            'bb_bbl': bb_bbl

        }

    # ma = pd.DataFrame(pastPriceVec)[].rolling(window=self.bollingerWindowSize).mean()

    @staticmethod
    def calculate_ema(series, span):
        return series.ewm(span=span, adjust=False).mean()

    def macd(self, price_vec):
        vec = pd.DataFrame(price_vec)[0]

        ema_fast = self.calculate_ema(vec, self.macdWindowFast)
        ema_slow = self.calculate_ema(vec, self.macdWindowSlow)
        macd = ema_fast - ema_slow
        macd_signal = self.calculate_ema(macd, self.macdWindowSignal)
        macd_diff = macd - macd_signal

        return {
            'macd': macd.iloc[-1],
            'macd_signal': macd_signal.iloc[-1],
            'macd_diff': macd_diff.iloc[-1]
        }

    def getAction(self, past_price_vec, current_price):
        price_pd = np.append(past_price_vec, current_price)

        bollinger = self.bollinger(price_pd)
        macd = self.macd(price_pd)

        buy_signal = (
                (current_price < bollinger['bb_bbl']) &
                (macd['macd'] > macd['macd_signal']) &
                (len(past_price_vec) >= self.bollingerWindowSize)
        )

        sell_signal = (
                (current_price > bollinger['bb_bbh']) &
                (macd['macd'] < macd['macd_signal']) &
                (len(past_price_vec) >= self.bollingerWindowSize)
        )

        if buy_signal:
            return Action.BUY.value
        elif sell_signal:
            return Action.SELL.value
        else:
            return Action.HOLD.value


def myStrategy(pastPriceVec, currentPrice):
    return Strategy(bollinger={'windowSize': 20, 'k': 1.5, 'std': 1.5},
                    macd={'windowFast': 5, 'windowSlow': 30, 'windowSignal': 5}).getAction(pastPriceVec, currentPrice)
