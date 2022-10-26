import backtrader as bt

class minPeriodIndicator(bt.Indicator):
    lines = ("state",)
    params = (('period',5),)
    plotinfo = dict(plot = False,
                    subplot=False)
                    
    def __init__(self) -> None:
        self.addminperiod(self.params.period+1)

class rewardObserver(bt.Observer):
    alias = ("reward",)
    lines = ("rewards",)
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Reward")

    def next(self):
        self.lines.rewards[0] = self._owner.reward

class cumRewardObserver(bt.Observer):
    alias = ("cumReward",)
    lines = ("cumRewards",)
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Cumulative Reward")

    def next(self):
        if len(self.lines.cumRewards) == 1:
            self.lines.cumRewards[0] = self._owner.reward
        else:
            self.lines.cumRewards[0] = self.lines.cumRewards[-1] + self._owner.reward

class cumRewardAnalyzer(bt.Analyzer):

    def __init__(self):
        self.reward = 0

    def next(self):
        self.reward += self.strategy.reward

    def get_analysis(self):
        return dict(cumreward=self.reward )

class actionObserver(bt.Observer):
    alias = ("action",)
    lines = ("actions",)
    
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Action Space",
                    plotyticks=(0,1,2),
                    plothlines = (0,1,2))

    def next(self):
        self.lines.actions[0] = self._owner.action
