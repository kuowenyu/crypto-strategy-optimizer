import backtrader as bt
import strategy

def run(data, p_fast, p_slow, cash=100000, commission=0.002, log=False):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(strategy.MACross, p_fast=p_fast, p_slow=p_slow)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    cerebro.broker.set_cash(cash)
    cerebro.broker.setcommission(commission=commission)
    start_cash = cerebro.broker.getvalue()
    if log:
        print('Starting Portfolio Value: %.2f' % start_cash)

    results = cerebro.run()

    final_cash = cerebro.broker.getvalue()
    if log:
        print('Final Portfolio Value: %.2f' % final_cash)
        print('Final Portfolio Change: %.2f' % (final_cash / start_cash * 100 - 100) + "%")

    result = results[0]
    if log:
        for item in result.analyzers:
            item.print()

    num_trade = result.analyzers[0].rets['total']['total']
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

