import gym
import gym.spaces
import math
from deeplog.environments import SupplyEnv
from deeplog.wrappers import Model
import pandas as pd
import numpy as np


class EOQModel(Model):
    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        Model.__init__(self, env)

        # Calculo la demanda anual
        self.demanda_anual = self.demand * 365

        self.s = costo_pedir
        self.h = costo_mantener

        # Calculo del punto de reorden
        self.rop = (self.demanda_anual / 365) * self.lead_time

        # Calculo de la cantidad economica de pedido
        self.eoq = math.ceil(math.sqrt(2 * self.demanda_anual * self.s / self.h))

        # Add serie rop
        self.add_serie('ROP', 'c')
        self.add_serie('Custom', 'b')

    def _plot_series(self):
        self.add_point('ROP', self.rop)
        self.add_point('Custom', 5000)

    def sample(self):
        pedido = 0
        if self.unwrapped.get_inventory_position() <= self.rop:
            pedido = self.eoq

        return [pedido]