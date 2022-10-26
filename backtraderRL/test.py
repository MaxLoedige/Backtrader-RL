from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import pandas as pd
from strategy import PositionBasedStrategy
from utils import actionObserver,rewardObserver,cumRewardObserver
from random import randint
from engine import  BTEngine
from .adapters.GymAdapter import GymAdapter

df = pd.read_csv("backtraderRL/test_data/BNB_USDT_5m.csv",index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)
data = bt.feeds.PandasData(dataname=df)

engine = BTEngine(lookback = 40)
engine.adddata(data)

engine.addstrategy(PositionBasedStrategy)
engine.addobserver(actionObserver)
engine.addobserver(rewardObserver)
engine.addobserver(cumRewardObserver)

# engine.addobserver(bt.observers.BuySell)
# engine.addobserver(bt.observers.Broker)
# engine.addobserver(bt.observers.Trades)

lookback = 10

engine.reset()
terminated = False

rewards = []

while not terminated:
    observation, reward, terminated = engine.step(randint(0,2))

engine.close()
engine.plot()