import gym
import math
from envs import SupplyEnv

start_date = "2017/01/01"
end_date = "2017/12/31"

lead_time = 7

env = SupplyEnv(start_date=start_date, end_date=end_date, lead_time=lead_time)

obs = env.reset()

env.render()

done = False


demanda = 1900 * 365

q = math.ceil(math.sqrt(2*demanda*1000/2.5))

print("EOQ: ", q)

demanda_promedio_dia = demanda / 365

rop = demanda_promedio_dia * lead_time

env.history['rop'] = rop

while not done:
    #pedido = env.sample()
    pedido = 0

    print("Date: {} - Demanda: {} - Inventory: {} - Transito: {} - OP: {} - Inventory Position: {} - ROP: {}".format(
        env.current_date, env.get_demand(), env.get_inventory(), env.get_transit(), env.get_order_pending(), env.get_inventory_position(), rop))

    if env.get_inventory_position() <= rop:
        pedido = q

    obs, reward, done, _ = env.step([pedido])

    env.render()

    if done:
        break

env.chart.figure.savefig("image.png")

print("Environment End")
print(env.history)



