import backtrader as bt

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