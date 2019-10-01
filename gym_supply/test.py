import gym
import math
from gym_supply.envs import SupplyEnv
from gym_supply.wrappers import EOQWrapper

start_date = "2017/01/01"
end_date = "2017/12/31"
lead_time = 7

env = SupplyEnv(start_date=start_date, end_date=end_date, lead_time=lead_time)
env = EOQWrapper(env)

obs = env.reset()

env.render()

done = False

while not done:
    """
    print("Date: {} - Demanda: {} - Inventory: {} - Transito: {} - OP: {} - Inventory Position: {} - ROP: {}".format(
        env.current_date, env.get_demand(), env.get_inventory(), env.get_transit(), env.get_order_pending(), env.get_inventory_position(), rop))
    """
    action = env.sample()

    obs, reward, done, _ = env.step(action)

    env.render()

    if done:
        break

env.chart.figure.savefig("image.png")

print("Environment End")
print(env.history)



