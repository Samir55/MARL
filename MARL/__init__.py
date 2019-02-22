from gym.envs.registration import register

register(
    id='marl-v0',
    entry_point='marl.envs:MARLEnv',
)
