import ccxt
import pandas as pd
import numpy as np
import datetime
import time 

def toDatetime(value):
    return datetime.datetime.fromtimestamp(int(value/1000))

binance = ccxt.binance()

pair = "BTC/USDT"
timeframe = "1h"
timedelta = datetime.timedelta(hours = 1)
chunk_size = 1000   # max is 1000
normalize = False

p = pair.split("/")
csv_name = f"examples/{p[0]}_{p[1]}_{timeframe}.csv"

save_interval = 1000

start = datetime.datetime(2021,1,1)
end = datetime.datetime(2022,1,1)

steps = int((end-start)/(timedelta))
num = int(np.ceil(steps/chunk_size)) if end else 10

t = int(start.timestamp() * 1000)
df = pd.DataFrame(columns = ["timestamp","open","high","low","close","volume"])

for i in range(num):    
    candles = np.array(binance.fetch_ohlcv( pair,
                                            timeframe,
                                            limit = chunk_size + 1 if i != num -1 else steps - (num-1) * chunk_size,
                                            since=t))
    
    if normalize:
        for n in range(1,6):
            candles[:,n] = (candles[:,n] - candles[:,n].min())/ (candles[:,n].max() - candles[:,n].min())

    temp = pd.DataFrame(candles, columns = ["timestamp","open","high","low","close","volume"])
    t = int(temp.tail(1).timestamp) + timedelta.seconds * 1000

    temp.timestamp = list(map(toDatetime,candles[:,0]))

    df = pd.concat([df, temp], ignore_index=True)

    print(f"{i*chunk_size}/{steps}")
    df.to_csv(csv_name)

    time.sleep(0.5)

# TODO clean up and interpolate when time index is missing

print(f"{steps}/{steps}")

print("done")
print("Dataframe length {}".format(len(df)))

df.to_csv(csv_name)