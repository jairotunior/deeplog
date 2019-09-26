import gym
import gym.spaces
from envs import SupplyEnv
import pandas as pd
import numpy as np


class CustomModelWrapper(gym.Wrapper):

    def __init__(self, env: SupplyEnv, costo_pedir=1000, costo_mantener=2.5):
        gym.Wrapper.__init__(self, env)

        self.series: pd.DataFrame = pd.DataFrame({'date': self.env.range_date})
        self.series = self.series.set_index('date')

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        self.env.render(mode=mode)

        window_size = 20
        window_start = max(self.env.iterator - window_size, 0)
        step_range = slice(window_start, self.env.iterator + 1)

        # Plot all series
        for serie in self.series.columns:
            self.env.chart.history.plot(self.series.iloc[window_start:self.env.iterator][serie].index.values,
                                        self.series.iloc[window_start:self.env.iterator][serie].values,
                                        color='r')

    def add_serie(self, serie_name, type=int):
        if serie_name in self.series:
            assert ValueError("El nombre de serie '{}' ya ha sido asignado, seleccione un nombre unico.".format(serie_name))

        self.series[serie_name] = 0
        #self.series[serie_name] = self.series[serie_name].astype(type)
        #self.env.history[serie_name] = initial_value

    def add_point(self, serie_name, value):
        #self.env.history.at[self.env.current_date, serie_name] = value

        if serie_name not in self.series:
            assert ValueError("La serie nombre {} no existe.".format(serie_name))

        self.series.at[self.env.current_date, serie_name] = value