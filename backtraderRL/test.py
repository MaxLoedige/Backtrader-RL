from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import pandas as pd
from strategy import AgentStrategy
from observers import actionObserver,minPeriodIndicator
from datetime import datetime,timedelta
from env import BTgym
from tensorforce.environments import Environment

df = pd.read_csv("backtraderRL/test_data/BNB_USDT_5m.csv",index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)
data = bt.feeds.PandasData(dataname=df)

cerebro = BTgym(lookback = 10,only_close=False)
cerebro.adddata(data)
cerebro.addstrategy(AgentStrategy)
cerebro.addobserver(actionObserver)

lookback = 10

environment = Environment.create(environment='gym', level=cerebro ,max_episode_timesteps=len(df)-lookback)



environment.reset()
terminated = False

while not terminated:
    observation, reward, terminated, truncated, info = environment.step()

print(len(df))

environment.close()
environment._environment.plot()