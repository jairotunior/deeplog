import gym
import gym.spaces
import math
from gym_supply.environments import SupplyEnv
from gym_supply.wrappers import CustomModelWrapper
import pandas as pd
import numpy as np


class MaxMinWrapper(CustomModelWrapper):

    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        CustomModelWrapper.__init__(self, env)
        self.demanda_anual = 1000 * 365

        self.lead_time = self.env.lead_time
        self.min = 0
        self.max = 10

        self.rop = 0
        self.cantidad_pedido = 0


        # Add serie rop
        self.add_serie('rop', self.rop)

    def sample(self, action):
        pedido = 0
        if self.env.get_inventory_position() <= self.rop:
            pedido = self.eoq

        return self.env.step([pedido])

    def render(self, mode='human'):
        self.env.render(mode=mode)

        self.env.chart.history.plot(self.env.history.index.values, self.env.history['rop'].values, 'r')