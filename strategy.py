import datetime

import backtrader as bt
import math

class BuyHold(bt.Strategy):
    def __init__(self):
        self.close = self.datas[0].close
        self.date = self.datas[0].datetime.date
        self.last_date = self.datas[-1].datetime.date

    def next(self):
        if not self.position:
            size = int(self.broker.getcash() / self.close[0])
            self.buy(size=size)


class MACross(bt.Strategy):
    params = (
        ('p_fast', 27),
        ('p_slow', 5),
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.ma_fast = bt.indicators.MovingAverageSimple(period=self.params.p_fast)
        self.ma_slow = bt.indicators.MovingAverageSimple(period=self.params.p_slow)
        self.date = self.datas[0].datetime.date
        self.sell_date = self.date(-1)
        self.signal = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        if not self.position:
            if self.signal > 0:
                size = int(self.broker.getcash() / self.close[0])
                self.buy(size=size)
        else:
            if self.signal < 0:
                self.sell(size=self.position.size)
                self.sell_date = self.date(0)


class Grid(bt.Strategy):
    params = (
        ('gap', 200),
        ('size', 3)
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.grid = [round(self.close[0] / 100) * 100 - self.params.gap / 2 + x * 200 for x in range(-2, 4, 1)]
        print(self.grid)
        self.current_index = 2

        self.date = self.datas[0].datetime.date
        self.last_date = self.datas[-1].datetime.date

        # init position
        self.buy(size=self.params.size * 3)

    def next(self):
        if self.current_index < len(self.grid) and self.close[0] > self.grid[self.current_index + 1]:
            self.sell(size=self.params.size)
            self.current_index += 1
        elif self.current_index >= 0 and self.close[0] < self.grid[self.current_index]:
            self.buy(size=self.params.size)
            self.current_index -= 1


class SelectedDays(bt.Strategy):
    params = (
        ('buy_day', None),
        ('sell_day', None),
        ('size', 1)
    )

    def __init__(self):
        self.close = self.datas[0].close
        self.date = self.datas[0].datetime.date

    def next(self):
        for day in self.params.buy_day:
            today = bt.utils.date.num2date(self.datetime[0])
            if today == day:
                amount = math.ceil(self.close * self.params.size)
                self.broker.add_cash(amount)
                self.buy(size=self.params.size)
                print("buy 1 at %.1f" % self.close[0])
