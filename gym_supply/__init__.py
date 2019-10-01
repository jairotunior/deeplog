from gym.envs.registration import register


register(
    id="SupplyEnv-v0",
    entry_point='gym_supply.environments.supply_env:SupplyEnv'
)