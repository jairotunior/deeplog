from gym.envs.registration import register


register(
    id="SupplyEnv-v0",
    entry_point='deeplog.environments.supply_env:SupplyEnv'
)