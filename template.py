from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
import gym_super_mario_bros
import time
from gym_super_mario_bros.actions import RIGHT_ONLY
from gym.spaces import prng

env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, RIGHT_ONLY)

# DATA FROM INFO
# {'coins': 0, 'flag_get': False, 'life': 3, 'score': 0, 'stage': 1, 'status': 'small', 'time': 400, 'world': 1, 'x_pos': 40}

# LOCATION 
# cd /home/andrew/.local/lib/python3.6/site-packages/gym_super_mario_bros

# MOVES POSSIBLE
# RIGHT_ONLY = [
#     ['NOP'],
#     ['right'],
#     ['right', 'A'],
#     ['right', 'B'],
#     ['right', 'A', 'B'],
# ]

class Node:
    #node in the game tree
    def _init_(self,distance = None, visited = None, parent = None, state = None):
        self.distance = distance
        self.visited = visited
        self.parent = parent
        self.unvisitedActions = [
            ['NOP'],
            ['right'],
            ['right', 'A'],
            ['right', 'B'],
            ['right', 'A', 'B'],
        ]
        self.children = []

    def AddChild(self, randomAction)
        children.append(randomAction)
        self.unvisitedActions.remove()

    def selectRandomAction(self, randomValue)
        #not random right now
        unvisitedActions[]

state = env.reset()

#use same seed to see same outcomes
prng.seed(1337)

# FIRST STEP OCCURED REGARDLESS
state, reward, done, info = env.step(env.action_space.sample())
#env.render()

#save the inital life number
lifeNum = info["life"] # always supposed to be 3

# check if the level has been completed
while(info['flag_get'] == False):
    state, reward, done, info = env.step(env.action_space.sample())
    # render the action/frame that occured
    #env.render()

    print(info["life"])

    # MARIO HAS DEAD!!!!
    if(lifeNum != info["life"]):
        # should revert time and choose a different action
        break

env.close()

