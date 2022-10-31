from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd

import backtrader as bt
from backtrader_rl.strategys import PositionBasedStrategy as strat
from backtrader_rl.utils import actionObserver,rewardObserver,cummulativeRewardObserver
from backtrader_rl.engines import  BTEngine
from backtrader_rl.adapters.tensorforceAdapter import tensorforceAdapter

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

import matplotlib.pyplot as plt
import numpy as np
# ================
# Defining constants
# ================

# the length of data points available to the agent at each step
LOOKBACK = 100
DATA_LENGTH = 10000

# ================
# Preparing test data
# ================

from pathlib import Path
root = Path().absolute()
file = "examples\BTC_USDT_1h.csv"
df = pd.read_csv(Path(root,file),index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)

# df = df.iloc[500:500+DATA_LENGTH]
# df = df.reset_index()


data = bt.feeds.PandasData(dataname=df)

engine = BTEngine(lookback = LOOKBACK, state_rows=("close",),normalize = False,canhold = False)
engine.broker.set_cash(100)
engine.adddata(data)

# ================
# Defining the Strategy
# ================

# the strategy defines the reward schema
# the position based strategy uses the position PNL as a reward at each step 
engine.addstrategy(strat)

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
    agent = "ppo" , environment = environment, batch_size = 1
)
rewards = []
for episode in range(100):
    # Episode using act and observe

    states = environment.reset()
    terminal = False
    sum_rewards = 0.0
    num_updates = 0

    while not terminal:
        actions = agent.act(states=states)
        states, terminal, reward = environment.execute(actions=actions)
        num_updates += agent.observe(terminal=terminal, reward=reward)
        sum_rewards += reward

    print('Episode {}: return= {} updates= {}'.format(episode, sum_rewards, num_updates))
    rewards.append(sum_rewards)

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

plt.plot(rewards)
plt.show()

environment.plot()

# Close agent and environment
agent.close()
environment.close()