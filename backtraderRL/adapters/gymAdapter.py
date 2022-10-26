import gym
from gym import spaces

class GymAdapter(gym.Env):

    def __init__(self,engine,**kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def step(self,action):
        observation, reward, self.terminated = super().step(action)
