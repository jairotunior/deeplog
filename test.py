import gym
from envs import SupplyEnv

start_date = "2017/01/01"
end_date = "2017/12/31"


env = SupplyEnv(start_date=start_date, end_date=end_date)

obs = env.reset()

env.render()

done = False

while not done:
    pedido = env.sample()

    obs, reward, done, _ = env.step(pedido)

    env.render()

    if done:
        break

print("Environment End")
print(env.history)



