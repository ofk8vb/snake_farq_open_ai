from gym.envs.registration import register

register(id='snake-v0',entry_point='snake.envs:SnakeEnv') # go into snake folder, envs folder then in the .py file SnakeEnv class is the entry point

