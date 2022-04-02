import backtrader as bt
import ccxt
import pandas as pd
import datetime
import matplotlib


class DataFactory:
    def __init__(self):
        pass

    def get_bars_from_ccxt(*args, **kwargs):
        exchange = ccxt.binanceus()
        start_date = int(kwargs['since'].timestamp() * 1000)
        end_date = int(kwargs['end'].timestamp() * 1000)

        bars = []
        last_date = start_date
        while True:
            if last_date >= end_date:
                break
            batch = exchange.fetch_ohlcv(kwargs['symbol'], timeframe=kwargs['timeframe'], since=last_date, limit=500)
            bars = bars + batch

            if last_date == batch[-1][0]:
                break

            last_date = batch[-1][0]

        df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        bt_data = bt.feeds.PandasDirectData(dataname=df, datetime=df.columns.get_loc('timestamp') + 1,
                                            open=df.columns.get_loc('open') + 1,
                                            high=df.columns.get_loc('high') + 1,
                                            low=df.columns.get_loc('low') + 1,
                                            close=df.columns.get_loc('close') + 1,
                                            volume=df.columns.get_loc('volume') + 1, openinterest=-1)

        return bt_data


def run(data, strategy, cash=100000, commission=0.002, log=False, plot=False, *args, **kwargs):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(strategy, *args, **kwargs)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    cerebro.broker.set_cash(cash)
    cerebro.broker.setcommission(commission=commission)
    start_cash = cerebro.broker.getvalue()
    if log:
        print('Starting Portfolio Value: %.2f' % start_cash)

    results = cerebro.run()

    if plot:
        cerebro.plot()

    final_cash = cerebro.broker.getvalue()
    if log:
        print('Final Portfolio Value: %.2f' % final_cash)
        print('Final Portfolio Change: %.2f' % (final_cash / start_cash * 100 - 100) + "%")

    result = results[0]
    if log:
        for item in result.analyzers:
            item.print()

    num_trade = result.analyzers[0].rets['total']['total']
    try:
        won_num = result.analyzers[0].rets['won']['total']
        won_max = round(result.analyzers[0].rets['won']['pnl']['max'], 2)
        won_total = round(result.analyzers[0].rets['won']['pnl']['total'], 2)
        lost_num = result.analyzers[0].rets['lost']['total']
        lost_max = round(result.analyzers[0].rets['lost']['pnl']['max'], 2)
        lost_total = round(result.analyzers[0].rets['lost']['pnl']['total'], 2)
        if lost_total == 0:
            ratio = 100
        else:
            ratio = abs(won_total / lost_total)

        return round(final_cash / start_cash * 100 - 100, 2), num_trade, \
               won_num, won_total, won_max, \
               lost_num, lost_total, lost_max, \
               ratio

    except:
        return round(final_cash / start_cash * 100 - 100, 2), num_trade, \
               0, 0, 0, 0, 0, 0, 0



