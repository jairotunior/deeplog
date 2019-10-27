import gym
import numpy as np
import math
from deeplog.environments import SupplyEnv
from deeplog.wrappers import DataSerie
from models import EOQModel, MaxMinModel


def fn_demand(mean, sigma):
    def fn(env):
        return np.ceil(np.random.normal(mean, sigma, 1))[0]
    return fn

start_date = "2017/01/01"
end_date = "2017/12/31"

lead_time = 7
demand = 1000

env = SupplyEnv(start_date=start_date, end_date=end_date, fn_demand=demand, fn_lead_time=lead_time, initial_stock=10000)
#env = DataSerie(env, "Produccion", fn_demand(2000, 500))
#env = EOQModel(env)
env = MaxMinModel(env, demand, 1500, 200)

obs = env.reset()

env.render()

done = False

while not done:
    action = env.sample()

    obs, reward, done, _ = env.step(action)

    print(obs)

    env.render()

    if done:
        break

env.chart.figure.savefig("image.png")

print("Environment End")
print(env.history)



