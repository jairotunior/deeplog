import gym
import gym.spaces
import pandas as pd
import numpy as np
from datetime import datetime
from gym.utils import seeding



class SupplyEnv(gym.Env):

    metadata = {'render.modes': ['human', 'system']}

    def __init__(self, start_date, end_date):

        self.start_date = datetime.strptime(start_date, format="%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, format="%Y/%m/%d")

        self.range_date = pd.date_range(start=start_date, end=end_date, freq='D')

        self.current_date = self.range_date[0]

        self.actions = ['pedir', 'no pedir', 'gerenciar']
        
        self.action_space = gym.spaces.Tuple(
            (gym.spaces.Discrete(n=len(self.actions)), 
            gym.spaces.Box(low=1, high=np.inf, shape=(1,), dtype=np.int))
        )
        self.observtion_space = gym.spaces.Box(low=0, high=np.inf, shape=(10, 1), dtype=np.int)


        self.seed()


    def step(self, action):
        pass

    def reset(self):
        pass

    def close(self):
        pass

    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31

        return [seed1, seed2]
    
    def sample(self):
        return self.action_space.sample()