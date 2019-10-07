import gym
import pandas as pd
import numpy as np


class Base(gym.Wrapper):

    def __init__(self, env):
        gym.Wrapper.__init__(self, env)

        # Base variables
        self.start_date = self.unwrapped.start_date
        self.end_date = self.unwrapped.end_date
        self.range_date = self.unwrapped.range_date
        self.sources = self.unwrapped.sources

        # Set all base variables
        self._set_base_variables()

    def _set_base_variables(self):
        self.iterator = self.unwrapped.iterator
        self.current_date = self.unwrapped.current_date

    def get_data_serie_value(self):
        pass

    def step(self, action):
        obs, reward, info, _ = self.env.action(action)
        self._set_base_variables()

        return obs, reward, info, _

    def reset(self):
        obs = self.env.reset()
        self._set_base_variables()

        return obs


def fn_demand(mean, sigma):
    def fn(env):
        return np.ceil(np.random.normal)


class DataSerie(Base):

    def __init__(self, env, name, dist_fn):
        Base.__init__(self, env)

        self.name = name

        self.dist_fn = dist_fn

    @override
    def _generate(self):
        raise NotImplementedError("El metodo _generate no ha sido implementado en la clase hija.")

