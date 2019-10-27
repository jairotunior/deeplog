import gym
import gym.spaces
from deeplog.environments import SupplyEnv
import pandas as pd
import numpy as np

from deeplog.wrappers import Base

from abc import ABC, abstractmethod


class Model(Base):

    def __init__(self, env):
        Base.__init__(self, env)

        self.series: pd.DataFrame = pd.DataFrame({'date': self.env.range_date})
        self.series = self.series.set_index('date')

        self.series_info: dict = {}

        self.legends = []

    def step(self, action):
        self._plot_series()
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        self.env.render(mode=mode)

        # Plot all series
        self._plot()

    def _plot_series(self):
        pass

    def _plot(self):
        if self.unwrapped.iterator > 0:
            window_size = 20
            window_start = max(self.unwrapped.iterator - window_size, 1)
            step_range = slice(window_start, self.unwrapped.iterator + 1)

            # Plot all series
            for serie in self.series.columns:
                self.unwrapped.chart.history.plot(self.series.iloc[window_start:self.unwrapped.iterator][serie].index.values,
                                                self.series.iloc[window_start:self.unwrapped.iterator][serie].values,
                                                color=self.series_info[serie]['color'])

        self.unwrapped.chart.history.legend(self.unwrapped.chart.legends + self.legends)


    def add_serie(self, serie_name, color='r'):
        if serie_name in self.series_info.keys():
            assert ValueError("El nombre de serie '{}' ya ha sido asignado, seleccione un nombre unico.".format(serie_name))

        self.series_info[serie_name] = {
            #'type': type,
            'color': color
        }

        self.legends.append(serie_name)

        self.series[serie_name] = 0
        #self.series[serie_name] = self.series[serie_name].astype(type)
        #self.env.history[serie_name] = initial_value


    def add_point(self, serie_name, value):
        #self.env.history.at[self.env.current_date, serie_name] = value

        if serie_name not in self.series:
            assert ValueError("La serie nombre {} no existe.".format(serie_name))

        self.series.at[self.unwrapped.current_date, serie_name] = value