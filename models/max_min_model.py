import gym
import gym.spaces
from deeplog.environments import SupplyEnv
from deeplog.wrappers import Model
import pandas as pd
import numpy as np


class MaxMinModel(Model):

    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        Model.__init__(self, env)
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
