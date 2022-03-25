import backtest
import pandas as pd
import backtrader as bt

data_name = 'ETH_1d_20210510_20211031.csv'
result_name = 'ETH_1d_20210510_20211031_result.html'

hist = pd.read_csv(data_name)
hist['timestamp'] = pd.to_datetime(hist['timestamp'], infer_datetime_format=True)

bt_data = bt.feeds.PandasDirectData(dataname=hist, datetime=hist.columns.get_loc('timestamp')+1,
                                    open=hist.columns.get_loc('open')+1, high=hist.columns.get_loc('high')+1,
                                    low=hist.columns.get_loc('low')+1, close=hist.columns.get_loc('close')+1,
                                    volume=hist.columns.get_loc('volume')+1, openinterest=-1)

result_list = []

for fast in range(5, 15, 2):
    for slow in range(fast + 1, 21, 2):
        result = backtest.run(bt_data, fast, slow)
        row = [fast, slow] + list(result)
        result_list.append(row)
# print(result_list)

result_df = pd.DataFrame(result_list, columns=['P_fast', 'P_slow', 'Change', 'Num_Trade',
                                               'Num_Won', 'Total_Won', 'Max_Won',
                                               'Num_Lost', 'Total_Lost', 'Max_Lost', 'Won/Lost'])
result_df.sort_values('Change', ascending=False, inplace=True)
print(result_df.head())
result_df.to_html(result_name, index=False)

backtest.run(bt_data, 5, 12, log=False)

