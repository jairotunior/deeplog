import gym
import gym.spaces
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from gym.utils import seeding

from envs.render.chart import Chart

import matplotlib.pyplot as plt

class DataSource:
    def __init__(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, "%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, "%Y/%m/%d")

        self.range_date = pd.date_range(start=start_date, end=end_date, freq='D')

        self.history = pd.DataFrame({'index': self.range_date,
                                    'demanda': np.zeros((len(self.range_date),)),
                                    })
        self.history = self.history.set_index('index')

        self.iterator = 0
        self.current_date = self.range_date[self.iterator]

    def next(self):
        # Get the consumo
        self.history.at[self.current_date, 'demanda'] = np.random.randint(0,
                                    1900,
                                    size=(1,)
                                    )

        obs = self.history.loc[self.current_date]

        self.iterator += 0
        self.current_date = self.range_date[self.iterator]

        return obs


class SupplyEnv(gym.Env):

    metadata = {'render.modes': ['human', 'system']}

    def __init__(self, start_date, end_date):

        self.start_date = datetime.strptime(start_date, "%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, "%Y/%m/%d")

        self.lead_time = timedelta(days=10)

        self.range_date = pd.date_range(start=start_date, end=end_date, freq='D')


        self.orders = pd.DataFrame({'index': self.range_date,
                                    'pedido': np.zeros((len(self.range_date),)),
                                    'fecha_entrega': np.zeros((len(self.range_date),)),
                                    'fecha_vencimiento': np.zeros((len(self.range_date),))
                                    })
        self.orders = self.orders.set_index('index')

        self.history = pd.DataFrame({'index': self.range_date,
                                    'demanda': np.zeros((len(self.range_date),)),
                                    'stock': np.zeros((len(self.range_date),)),
                                    'transito': np.zeros((len(self.range_date),)),
                                    'disponible': np.zeros((len(self.range_date),)),
                                    'pedido': np.zeros((len(self.range_date),))
                                    })
        self.history = self.history.set_index('index')

        self.iterator = 0
        self.current_date = self.range_date[self.iterator]

        #self.actions = ['pedir', 'no pedir']
        
        """
        self.action_space = gym.spaces.Tuple(
            (gym.spaces.Discrete(n=len(self.actions)), 
            gym.spaces.Box(low=1, high=np.inf, shape=(1,), dtype=np.int))
        )
        """

        self.action_space = gym.spaces.Box(low=0, high=2000, shape=(1,), dtype=np.int)
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(10, 1), dtype=np.int)

        self.seed()

        self.chart = None

        self._calculate()


    def _calculate(self):
        # Initial Stock
        self.history.at[self.current_date, 'stock'] = 2000


    def step(self, action):
        # Get the consumo
        self.history.at[self.current_date, 'demanda'] = np.random.randint(0,
                                    1900,
                                    size=(1,)
                                    )

        # Save the order
        self.orders.at[self.current_date, 'pedido'] = action[0]
        self.orders.at[self.current_date, 'fecha_entrega'] = self.range_date[self.iterator] + self.lead_time
        self.orders.at[self.current_date, 'fecha_vencimiento'] = self.range_date[self.iterator] + self.lead_time

        self.history.at[self.current_date, 'pedido'] = action[0]

        # Get incoming orders
        mask = self.orders['fecha_entrega'] == self.current_date
        incoming_orders = self.orders.loc[mask]
        current_transito = incoming_orders['pedido'].sum()

        # If there are incoming orders, proceed to receive
        if current_transito > 0:
            self.history.at[self.current_date, 'transito'] = current_transito

        # Get the current stock and consumo
        current_stock = self.history.at[self.current_date, 'stock']
        current_consumo = self.history.at[self.current_date, 'demanda']

        # Set current availability
        self.history.at[self.current_date, 'disponible'] = current_stock + current_transito - current_consumo

        # Validate if the environment ends
        done = self.iterator == (len(self.range_date) - 1)

        if not done:
            # Update iterator and Current Date
            self.iterator += 1
            self.current_date = self.range_date[self.iterator]

            # Set new stock for next day
            self.history.at[self.current_date, 'stock'] = current_stock + current_transito - current_consumo
            
        obs, reward, _ = [None, 0, None]

        return obs, reward, done, _


    def reset(self):
        self.iterator = 0
        self.current_date = self.range_date[self.iterator]

    def close(self):
        pass

    def render(self, mode='human'):
        if self.chart is None:
            self.chart = Chart()
        else:
            self.chart.render(self.history.iloc[:self.iterator])

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31

        return [seed1, seed2]
    
    def sample(self):
        return self.action_space.sample()

    """
    API for inventory
    """
    def get_inventory(self):
        return self.history.at[self.current_date, 'stock']

    def get_transit(self):
        return self.history.at[self.current_date, 'transito']

    def get_availability(self):
        return self.history.at[self.current_date, 'disponible']

    def get_order_pending(self):
        mask = self.orders['fecha_vencimiento'] > self.current_date
        return self.history.loc[mask]['pedido'].sum()

    def get_inventory_position(self):
        return self.inventory() + self.order_pending()

    def get_average_daily_demand(self, backperiods=30):
        mask = self.history.index < self.current_date
        return self.history.loc[mask].loc[-backperiods:, 'demanda'].mean()
