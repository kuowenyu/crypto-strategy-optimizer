import datetime

import backtest
import pandas as pd
import backtrader as bt
import strategy

## Setup
symbol = 'ETH/USD'
timeframe = '1d'
since = datetime.datetime(2019, 1, 1)
end = datetime.datetime.now()
output_file = 'select_days.html'
select_strategy = 3

result_list = []
result_df = None

## Prepare data
factory = backtest.DataFactory()
bt_data = factory.get_bars_from_ccxt(symbol=symbol, timeframe=timeframe, since=since, end=end)

if select_strategy == 0:
    pass
    result = backtest.run(bt_data, strategy.BuyHold, log=True)
    result_list.append(list(result))
    result_df = pd.DataFrame(result_list, columns=['Change', 'Num_Trade',
                                                   'Num_Won', 'Total_Won', 'Max_Won',
                                                   'Num_Lost', 'Total_Lost', 'Max_Lost', 'Won/Lost'])

elif select_strategy == 1:
    ## Run MACross
    for fast in range(5, 15, 2):
        for slow in range(fast + 1, 21, 2):
            result = backtest.run(bt_data, strategy.MACross, p_fast=fast, p_slow=slow)
            row = [fast, slow] + list(result)
            result_list.append(row)
    result_df = pd.DataFrame(result_list, columns=['P_fast', 'P_slow', 'Change', 'Num_Trade',
                                                   'Num_Won', 'Total_Won', 'Max_Won',
                                                   'Num_Lost', 'Total_Lost', 'Max_Lost', 'Won/Lost'])
elif select_strategy == 2:
    ## Run Grid
    result = backtest.run(bt_data, strategy.Grid, plot=True, log=True)
    row = list(result)
    result_list.append(row)
    result_df = pd.DataFrame(result_list, columns=['Change', 'Num_Trade',
                                                   'Num_Won', 'Total_Won', 'Max_Won',
                                                   'Num_Lost', 'Total_Lost', 'Max_Lost', 'Won/Lost'])

elif select_strategy == 3:
    ## Run SelectedDays
    days = []
    for year in range(2019, 2022, 1):
        days.append(datetime.datetime(year, 2, 1))
        days.append(datetime.datetime(year, 7, 19))

    result = backtest.run(bt_data, strategy.SelectedDays, buy_day=days, cash=10, commission=0, plot=True, log=True)
    row = list(result)
    result_list.append(row)
    result_df = pd.DataFrame(result_list, columns=['Change', 'Num_Trade',
                                                   'Num_Won', 'Total_Won', 'Max_Won',
                                                   'Num_Lost', 'Total_Lost', 'Max_Lost', 'Won/Lost'])

if result_df is not None:
    result_df.sort_values('Change', ascending=False, inplace=True)
    print(result_df.head())
    result_df.to_html(output_file, index=False)

