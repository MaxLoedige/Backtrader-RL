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
LOOKBACK = 40
DATA_LENGTH = 10000

# ================
# Preparing test data
# ================

from pathlib import Path
root = Path().absolute()
file = "examples\BTC_USDT_5m.csv"
df = pd.read_csv(Path(root,file),index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)

print(df.isnull().values.any())