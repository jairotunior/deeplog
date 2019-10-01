import gym
import gym.spaces
import math
from envs import SupplyEnv
from wrappers import CustomModelWrapper
import pandas as pd
import numpy as np


class EOQWrapper(CustomModelWrapper):
    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        CustomModelWrapper.__init__(self, env)
        self.demanda_anual = 1000 * 365

        self.lead_time = self.env.lead_time
        self.s = costo_pedir
        self.h = costo_mantener

        self.rop = (self.demanda_anual / 365) * self.lead_time.days
        self.eoq = math.ceil(math.sqrt(2 * self.demanda_anual * self.s / self.h))

        # Add serie rop
        self.add_serie('ROP')

    def step(self, action):
        self.add_point('ROP', self.rop)

        return self.env.step(action)

    def sample(self):
        pedido = 0
        if self.env.get_inventory_position() <= self.rop:
            pedido = self.eoq

        return [pedido]