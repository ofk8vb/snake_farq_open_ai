import pygame, sys, time, random
from pygame.surfarray import array3d
from pygame import display

import numpy as np
import gym
from gym import error,spaces,utils
from gym.utils import seeding

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)


class SnakeEnv(gym.Env): # Gym specific-code
    
    metadata = {'render.modes':['human']} # Gym-specific code # to allow human playibility
    
    def __init__(self):
        
        self.action_space = spaces.Discrete(4) # Gym-specific code # 4 actions up down left right
        self.frame_size_x = 200
        self.frame_size_y = 200
        self.game_window = pygame.display.set_mode((self.frame_size_x,self.frame_size_y))
        
        # Reset the Game
        self.reset()
        self.STEP_LIMIT = 1000 # Gym-specific code # game will be over when user takes 1000 steps
        self.sleep = 0 # Gym-specific code # this can be used if we want to allow human playability to prevent ultra fast gameplay
        
        
    def reset(self):
        
        '''
        reset() NEEDS to return ONLY observation img , [2,3] etc
        '''
        
        
        self.game_window.fill(BLACK)
        self.snake_pos = [100,50] # x , y coordinates snake is a single pos is a 10 pixel square 
        self.snake_body = [[100,50],[100-10,50],[100-(2*10),50]] # snake will be 3 squares long at start # each square is 10 pixels
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        self.direction = 'RIGHT' # snake starts the game moving to right
        self.action = self.direction
        
        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface()) # Gym-specific code # returns surface of pygame window and returns it back as an image array
        img = np.swapaxes(img,0,1) # Gym-specific code # for tf reason
        return img # Gym-specific code # returns back final image # OBSERVATION 
#         print('GAME RESET')
    
    @staticmethod # this is a method that will keep all SnakeEnv class attributes static , not directly interfere
    def change_direction(action,direction):
        
         # checking so snake cannot go through itself in single action
        if action == 'UP' and direction != 'DOWN':
            direction ='UP'
            
        if action == 'DOWN' and direction != 'UP':
            direction ='DOWN'
            
        if action == 'LEFT' and direction != 'RIGHT':
            direction ='LEFT'
            
        if action == 'RIGHT' and direction != 'LEFT':
            direction ='RIGHT'
        
        # if action is same as direction just keep going in the same direction
        return direction 
    
    @staticmethod # this is a method that will keep all SnakeEnv class attributes static , not directly interfere
    def move(direction, snake_pos):
        
        if direction == 'UP': # -y
            snake_pos[1] -= 10
            
        if direction == 'DOWN': # +y
            snake_pos[1] += 10
            
        if direction == 'LEFT': # -x
            snake_pos[0] -=10
            
        if direction == 'RIGHT': # +x
            snake_pos[0] +=10
        
        return snake_pos
    
    def spawn_food(self):
        # // means division with no remainders
        # returns something like [100,50] for food position
        # self.food_pos = spawn_food()
        return [random.randrange(1,(self.frame_size_x//10))*10,random.randrange(1,(self.frame_size_y//10))*10] 
        
    
    def eat(self):
        # check if snake position is exactly same as food position
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]
    
    def step(self, action): # event comes from pygame
        '''
        What happens when your agent performs the action on the env?
        
        '''
        
        scoreholder = self.score
        reward = 0
        self.direction = SnakeEnv.change_direction(action,self.direction)
        self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
        self.snake_body.insert(0,list(self.snake_pos))
        
        reward = self.food_handler() # reward_handler # report back reward
        self.update_game_state() # how do we update the env, after action?
        
        reward,done = self.game_over(reward)
        
        img = self.get_image_array_from_game() # GET OBSERVATIONS
        
        info = {'score': self.score}      
        self.steps = +=1
        time.sleep(self.sleep)
        
        # observation, reward, done ,info observation is image in this case since this will only be trainable by images
        return img, reward, done, info
      
    def food_handler(self):
        if self.eat():
            self.score += 1
            reward = 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward = 0
            
        if not self.food_spawn:
            self.food_pos = self.spawn_food
        self.food_spawn = True
        
        return reward
        
    
    def get_image_array_from_game(self):
        img = array3d(display.get_surface()) # Gym-specific code # returns surface of pygame window and returns it back as an image array
        img = np.swapaxes(img,0,1) # Gym-specific code # for tf reason
        return img 
       
    
    def update_game_state(self):
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.game_window, WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
    def render(self,mode ='human'):
        if mode =='human':
            display.update()
            
    def close(self):
        pass
        
    def game_over(self):
        ''' 
        Checks if the snake has touched the bounding box or itself
        '''
        
        # TOUCH THE BOUNDED BOX
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return -1, True
            
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return -1, True
        
        # TOUCH OWN BODY
        # if snake's head (snake_pos) matches any of the positions in snake_body, it means snake has touched it its own body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return -1, True
            
        if self.steps >= self.STEP_LIMIT:
            return 0 , True
        
        return reward, False

    
            
        