import backtrader as bt

class AgentStrategy(bt.Strategy):

    def __init__(self):
        self.action = 1

    def _setAction(self,action):
        self.action = action

    def next(self):
        if self.action == 2:
            # if current position is sell
            # then we are closing a trade
            if self.position.size < 0:
                self.reward = self._get_reward()
                self.close()
            elif self.position.size == 0:
                self.buy()
        elif self.action == 0:
            # if current position is buy
            # then we are closing a trade
            if self.position.size > 0:
                self.reward = self._get_reward()
                self.close()
            elif self.position.size == 0:
                self.sell()        
