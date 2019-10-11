import gym
import numpy as np
import math
from tensor_supply.environments import SupplyEnv
from tensor_supply.wrappers import DataSerie
from models import EOQModel


def fn_demand(mean, sigma):
    def fn(env):
        return np.random.normal(mean, sigma, 1)
    return fn

start_date = "2017/01/01"
end_date = "2017/12/31"

lead_time = 7

env = SupplyEnv(start_date=start_date, end_date=end_date, fn_demand=1000, fn_lead_time=lead_time, initial_stock=10000)
env = DataSerie(env, "Produccion", 10)
env = EOQModel(env)

obs = env.reset()

env.render()

done = False

while not done:
    action = env.sample()

    obs, reward, done, _ = env.step(action)

    env.render()

    if done:
        break

env.chart.figure.savefig("image.png")

print("Environment End")
print(env.history)



