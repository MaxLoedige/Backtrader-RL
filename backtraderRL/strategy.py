import backtrader as bt

class BaseStrategy(bt.Strategy):

    def __init__(self):
        self.action = 1
        self.reward = 0
        self.mapping = {"buy" : 2, "sell" : 0, "hold":1}

    def _set_action_mapping(self,mapping):
        self.mapping = mapping

    def _setAction(self,action):
        self.action = action

    def next(self):
        if self.action == self.mapping["buy"]:
            # if current position is sell
            # then we are closing a trade
            if self.position.size < 0:
                self.close()
            elif self.position.size == 0:
                self.buy()
        elif self.action == self.mapping["sell"]:
            # if current position is buy
            # then we are closing a trade
            if self.position.size > 0:
                self.close()
            elif self.position.size == 0:
                self.sell()        

    def _computeReward(self):
        try:
            reward = self.computeReward()
        except:
            reward = 0
        self.reward = reward
        return self.reward

class PositionBasedStrategy(BaseStrategy):

    def computeReward(self):
        if self.position.size == 0:
            return 0

        a = self.position.price
        b = self.datas[0].close[0]
        d = (b-a)/((b+a)/2)
        return d * 100 * (self.position.size/abs(self.position.size))        