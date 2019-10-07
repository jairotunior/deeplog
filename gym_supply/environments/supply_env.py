import gym
import gym.spaces
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from gym.utils import seeding

from gym_supply.environments.render import Chart
from gym_supply.data import DataSource, SinteticDataSource

import matplotlib.pyplot as plt


class SupplyEnv(gym.Env):

    metadata = {'render.modes': ['human', 'system']}

    def __init__(self, start_date, end_date, fn_demand, fn_lead_time, **kwargs):
        assert fn_demand is None, "Debe definir una funcion demanda"
        assert fn_lead_time is None, "Debe definir una funcion lead time"

        self.start_date = datetime.strptime(start_date, "%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, "%Y/%m/%d")

        self.range_date = pd.date_range(start=start_date, end=end_date, freq='D')

        self.sources = pd.DataFrame({'index': self.range_date,
                                'demand': np.zeros((len(self.range_date),)),
                                })
        self.sources = self.sources.set_index('index')

        self.fn_demand = fn_demand
        self.fn_lead_time = fn_lead_time

        self.lead_time = 0

        self.initial_stock = kwargs.get('initial_stock', 0)

        self.orders = pd.DataFrame({'index': self.range_date,
                                    'pedido': np.zeros((len(self.range_date),)),
                                    'fecha_entrega': np.zeros((len(self.range_date),)),
                                    'fecha_vencimiento': np.zeros((len(self.range_date),))
                                    })
        self.orders = self.orders.set_index('index')
        self.orders['fecha_vencimiento'] = self.orders['fecha_vencimiento'].astype('datetime64[ns]')

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

        self.action_space = gym.spaces.Box(low=0, high=2000, shape=(1,), dtype=np.int)
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(10, 1), dtype=np.int)

        self.seed()

        self.chart = Chart()

        self._calculate()


    def _calculate(self):
        # Initial Stock
        self.history.at[self.current_date, 'stock'] = self.initial_stock
        # Generate demand

        current_consumo = self.fn_demand(self)
        self.history.at[self.current_date, 'demanda'] = current_consumo
        # self.history.at[self.current_date, 'demanda'] = np.random.randint(0, 1000, size=(1,))


    def step(self, action):
        current_consumo = self.history.at[self.current_date, 'demanda']

        # Get Lead Time
        self.lead_time = timedelta(self.fn_lead_time(self))

        # Save the order
        self.orders.at[self.current_date, 'pedido'] = action[0]
        self.orders.at[self.current_date, 'fecha_entrega'] = self.range_date[self.iterator] + self.lead_time
        self.orders.at[self.current_date, 'fecha_vencimiento'] = self.range_date[self.iterator] + self.lead_time

        self.history.at[self.current_date, 'pedido'] = action[0]

        # Get the current stock and consumo
        current_stock = self.history.at[self.current_date, 'stock']

        # Get incoming orders
        mask = self.orders['fecha_entrega'] == self.current_date
        incoming_orders = self.orders.loc[mask]
        current_transito = incoming_orders['pedido'].sum()

        # If there are incoming orders, proceed to receive
        if current_transito > 0:
            self.history.at[self.current_date, 'transito'] = current_transito

        # Set current availability
        self.history.at[self.current_date, 'disponible'] = current_stock + current_transito

        # Validate if the environment ends
        done = self.iterator == (len(self.range_date) - 1)

        obs, reward, _ = [current_consumo, 0, None]

        if not done:
            # Update iterator and Current Date
            self.iterator += 1
            self.current_date = self.range_date[self.iterator]

            # Set new stock for next day
            self.history.at[self.current_date, 'stock'] = current_stock + current_transito - current_consumo

        # Generate demand
        self.history.at[self.current_date, 'demanda'] = self.fn_demand(self)
        # self.history.at[self.current_date, 'demanda'] = np.random.randint(0, 1000, size=(1,))

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
            self.chart.render(self.history, self.iterator)

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31

        return [seed1, seed2]
    
    def sample(self):
        return self.action_space.sample()

    """
    API for inventory
    """
    def get_demand(self):
        return self.history.at[self.current_date, 'demanda']

    def get_inventory(self):
        return self.history.at[self.current_date, 'stock']

    def get_transit(self):
        mask = self.orders['fecha_vencimiento'] == self.current_date
        return self.orders.loc[mask]['pedido'].sum()

    def get_availability(self):
        return self.get_inventory() + self.get_transit()

    def get_order_pending(self):
        mask = self.orders['fecha_vencimiento'] > self.current_date
        return self.orders.loc[mask]['pedido'].sum()

    def get_inventory_position(self):
        return self.get_availability() + self.get_order_pending()

    def get_average_daily_demand(self, backperiods=30):
        mask = self.history.index < self.current_date
        return self.history.loc[mask].loc[-backperiods:, 'demanda'].mean()
