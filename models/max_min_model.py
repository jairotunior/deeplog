import gym
import gym.spaces
from deeplog.environments import SupplyEnv
from deeplog.wrappers import Model
import pandas as pd
import numpy as np


class MaxMinModel(Model):

    def __init__(self, env: SupplyEnv, demand_prom:int, demand_max:int, demand_min:int):
        Model.__init__(self, env)

        self.demand_prom = demand_prom
        self.demand_min = demand_min
        self.demand_max = demand_max

        self.inv_min = self.demand_min * self.lead_time
        self.inv_max = (self.demand_max * self.lead_time) + self.inv_min

        self.rop = (self.demand_prom * self.lead_time) + self.demand_min

        # Add serie rop
        self.add_serie('ROP', 'c')

    def _plot_series(self):
        self.add_point('ROP', self.rop)


    def sample(self):
        pedido = 0
        if self.unwrapped.get_inventory_position() <= self.rop:
            pedido = self.inv_max - self.unwrapped.get_inventory_position()

        return [pedido]
