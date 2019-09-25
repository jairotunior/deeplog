import gym
import gym.spaces
import math
from envs import SupplyEnv
import pandas as pd
import numpy as np


class EOQWrapper(gym.Wrapper):

    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        gym.Wrapper.__init__(self, env)
        self.demanda_anual = 1000 * 365

        self.lead_time = self.env.lead_time
        self.s = costo_pedir
        self.h = costo_mantener

        self.rop = (self.demanda_anual / 365) * self.lead_time.days
        self.eoq = math.ceil(math.sqrt(2 * self.demanda_anual * self.s / self.h))
        print("EOQ: ", self.eoq)

    def step(self, action):
        print("wrapper")
        pedido = 0
        if self.env.get_inventory_position() <= self.rop:
            pedido = self.eoq

        obs, reward, info, _ = self.env.step([pedido])
        return obs, reward, info, _

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        self.env.render(mode=mode)

        #self.env.chart.history.plot()