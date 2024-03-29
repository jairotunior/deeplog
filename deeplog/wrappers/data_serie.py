import gym
import pandas as pd
import numpy as np

from abc import ABC
from deeplog.utils import get_value

from functools import partial


class Base(gym.Wrapper):

    def __init__(self, env):
        gym.Wrapper.__init__(self, env)

        # Base variables
        self.start_date = self.unwrapped.start_date
        self.end_date = self.unwrapped.end_date
        self.range_date = self.unwrapped.range_date

        self.fn_demand = self.unwrapped.fn_demand
        self.fn_lead_time = self.unwrapped.fn_lead_time

        self.serie_names = self.unwrapped.serie_names
        self.sources = self.unwrapped.sources

        # Set all base variables
        self.iterator = self.unwrapped.iterator
        self.current_date = self.unwrapped.current_date

    def _set_base_variables(self):
        self.iterator = self.unwrapped.iterator
        self.current_date = self.unwrapped.current_date

    def step(self, action):
        obs, reward, info, _ = self.env.action(action)
        self._set_base_variables()

        return obs, reward, info, _

    def reset(self):
        obs = self.env.reset()
        self._set_base_variables()

        return obs

    @property
    def demand(self):
        return get_value(self.unwrapped.fn_demand)

    @property
    def lead_time(self):
        return get_value(self.unwrapped.fn_lead_time)


def fn_demand(mean, sigma):
    def fn(env):
        return np.ceil(np.random.normal(mean, sigma, 1))

    return fn


class DataSerie(Base):

    def __init__(self, env, name, fn_dist):
        Base.__init__(self, env)

        assert callable(fn_dist) or isinstance(fn_dist, int), "Debe definir una funcion de distribución"

        self.name = name
        self.serie_names.append(self.name)

        if callable(fn_dist):
            self.fn_dist = partial(fn_dist, self)
        else:
            self.fn_dist = fn_dist

        self.sources[self.name] = 0


    def _compute_all_sources(self):
        serie_value = get_value(self.fn_dist)
        self.sources.at[self.current_date, self.name] = serie_value

        return [serie_value]

    def step(self, action):
        serie_value = self._compute_all_sources()

        obs, reward, info, _ = self.env.step(action)
        obs = obs + serie_value

        return obs, reward, info, _

