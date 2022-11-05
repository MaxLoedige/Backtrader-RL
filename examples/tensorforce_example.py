from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd

import backtrader as bt
from backtrader_rl.strategys import BaseStrategy
from backtrader_rl.utils import actionObserver,rewardObserver,cummulativeRewardObserver
from backtrader_rl.engines import  BTEngine
from backtrader_rl.adapters.tensorforceAdapter import tensorforceAdapter

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

import matplotlib.pyplot as plt
import numpy as np

# ================
# Reward Shema
# ================

class RewardSchema(BaseStrategy):

    lastRef = -1
    total = []
    down = []
    lastSortino = 0
    lastNonZeroChange = 0
    steps_from_change = 0
    useLastingReward = True

    def claclSortino(self):

        trades = list(list(self._trades.copy().values())[0].values())[0]
        filterd_trades = list(filter(lambda x : x.isclosed, trades))

        if len(filterd_trades) < 1:
            return 0

        lastTrade = filterd_trades[-1]

        if self.lastRef != lastTrade.ref:
            self.lastRef = lastTrade.ref
            ret = (lastTrade.pnlcomm/lastTrade.price)*100
            if ret <= 0:
                self.down.append(ret)
            self.total.append(ret)

        m = np.mean(self.total)

        std = np.std(self.down)

        if std == 0 or type(std) == np.nan:
            return 0


        sr = np.sqrt(len(filterd_trades))

        return (m*sr)/std

    # cal sortiono ratio
    def computeReward(self):

        sortino = self.claclSortino()

        change = sortino - self.lastSortino
        change = change if not np.isnan(change) else 0

        if change != 0:
            self.lastNonZeroChange = change
            self.steps_from_change = 0
        else:
            self.steps_from_change += 1

        self.lastSortino = sortino

        if self.useLastingReward:
            return (self.lastNonZeroChange / (self.steps_from_change + 1))

        return change

# ================
# Defining constants
# ================

# the length of data points available to the agent at each step
LOOKBACK = 15
DATA_LENGTH = 10000

# ================
# Preparing test data
# ================

from pathlib import Path
root = Path().absolute()
file_name = "examples\BTC_USDT_5m.csv"
df = pd.read_csv(Path(root,file_name),index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)

# df = df.iloc[500:500+DATA_LENGTH]
# df = df.reset_index()


data = bt.feeds.PandasData(dataname=df)

engine = BTEngine(  lookback = LOOKBACK, 
                    state_rows=("ohlcv",),
                    normalize = True,
                    canhold = True)

engine.broker.set_cash(100)
engine.adddata(data)

# ================
# Defining the Strategy
# ================

# the strategy defines the reward schema
# the position based strategy uses the position PNL as a reward at each step 
engine.addstrategy(RewardSchema)

# observeres allow us to peak into the actions taken by the agent over the episode
engine.addobserver(actionObserver)
engine.addobserver(rewardObserver)
engine.addobserver(cummulativeRewardObserver)


# default backtrader observers also work just fine
engine.addobserver(bt.observers.BuySell)
engine.addobserver(bt.observers.Value)
engine.addobserver(bt.observers.Trades)

#

environment = Environment.create(
    environment=tensorforceAdapter(engine), max_episode_timesteps=len(df)-LOOKBACK-1
)

agent = Agent.create(
    agent = "ppo" , environment = environment, batch_size = 2
)

import time

times = []
for episode in range(5):
    # Episode using act and observe
    start_time = time.time()
    num_steps  = 0
    states = environment.reset()
    terminal = False
    sum_rewards = 0.0
    num_updates = 0

    while not terminal:
        actions = agent.act(states=states)
        states, terminal, reward = environment.execute(actions=actions)
        num_updates += agent.observe(terminal=terminal, reward=reward)
        sum_rewards += reward
        num_steps += 1

    print('Episode {}: return= {} updates= {}'.format(episode, sum_rewards, num_updates))

    end_time = time.time()
    times.append(end_time-start_time)

print("total time[s]: ", sum(times))
print("time per episode", np.mean(times))
print("total steps per episode: ", num_steps)
print("seconds per step: ", np.mean(times)/num_steps)

# Evaluate for 100 episodes
sum_rewards = 0.0
num = 1
for _ in range(num):
    states = environment.reset()
    internals = agent.initial_internals()
    terminal = False
    while not terminal:
        actions, internals = agent.act(
            states=states, internals=internals, independent=True, deterministic=False
        )
        states, terminal, reward = environment.execute(actions=actions)
        sum_rewards += reward

print('Mean evaluation return:', sum_rewards / num)

environment.plot()

# Close agent and environment
agent.close()
environment.close()