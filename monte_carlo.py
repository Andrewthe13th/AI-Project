from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv, FrameStackEnv
import gym_super_mario_bros
import time
import random
import copy
from gym_super_mario_bros.actions import RIGHT_ONLY
from gym.spaces import prng
from gym_super_mario_bros.smb_env import SuperMarioBrosEnv

env = gym_super_mario_bros.make('SuperMarioBrosNoFrameskip-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, RIGHT_ONLY)
gameEnv = SuperMarioBrosEnv()
#print(gameEnv._x_position)
#env = FrameStackEnv(env, 5) # implemts storing frames HOWEVER not sure how to restore to failed frame

#GLOBAL
lifeNum = 0
save_state = None

# ===== NODE TREE AND FUNCTIONS ==============

class Node:
    def __init__(self, parent = None, x_pos = None, dead = False, action = None):
        self.children = [None] * 5
        self.unChosenChildren = [0,1,2,3,4] # remove as neccessary
        self.parent = parent
        self.x_pos = x_pos
        self.dead = dead
        self.action = action

    #Makes and return pointer to child
    def returnChild(self, randomAction, x_pos, dead):
        child = Node(self, x_pos, dead, randomAction)
        self.children[randomAction] = child
        self.unChosenChildren.remove(randomAction)
        return child

    # Returns a path not done before
    

def bMarioDead(currentLifeCount):
    global lifeNum
    if(lifeNum != currentLifeCount):
        return True
    else:
        return False

state = env.reset()

# =========== MAIN CODE =========================

#use same seed to see same outcomes
SEED = 1337
prng.seed(SEED)
random.seed(SEED)

# FIRST STEP OCCURED REGARDLESS -----ROOT------
# root = Node()
# #randomAction = env.action_space.sample()
# state, reward, done, info = env.step(0)
# print(info)
# #print(randomAction)
# #save the inital life number
# lifeNum = info["life"]
# currentChild = root.returnChild(0, info["x_pos"], bMarioDead(info["life"]))
# env.render()

lifeNum = 3
currentChild = Node(None,None, False,0)
state, reward, done, info = env.step(0)
env.reset()

#----------------------------SELECTION---------------------
# RUN until completing the level
while(info['flag_get'] == False):
    # --------------------SIMULATION-------------------
    #RUN until mario dies
    while(currentChild.dead == False):
        #---------------------------SELECTION--------------------
        #make a random move
        randomAction = env.action_space.sample()
        state, reward, done, info = env.step(randomAction)
        #create new child node
        currentChild = currentChild.returnChild(randomAction, info["x_pos"], bMarioDead(info["life"]))
        # render the action/frame that occured
        env.render()

    # ---------BACKPROPAGATION -------------------------
    # should revert time and choose a different action    

    print(currentChild.dead)
    # used to reset mario to original self after all lives lost
    if(info["life"] == 256): #256 == 0 lives in super mario
        print("mario lost all lives")


    #Save all actions done for mario to revert to last state
    print("===============Current Path of Random Actions =================")
    previousActions = []
    childIter = currentChild
    while(childIter != None):
        previousActions.append(childIter.action)
        childIter = childIter.parent

    #remove the failure state child from path
    previousActions.reverse()
    previousActions.pop()

    currentChild = currentChild.parent

    # check for a node with at least a new action aviable
    while(not currentChild.unChosenChildren):
        currentChild = currentChild.parent
        previousActions.pop()

    print(previousActions)

    #reset the env
    lifeNum = info["life"]
    env.reset()

    # setup up env back to before mario DIED
    for x in previousActions:
        #just used to skip the None Action type of root node
        #if(x != None):
            #redo all actions from before except the last
        env.step(x)
        env.render()
        # else:
        #     env.render()

    #pick another path from child not selected
    randomAction = random.choice(currentChild.unChosenChildren)
    state, reward, done, info = env.step(randomAction)
    currentChild = currentChild.returnChild(randomAction, info["x_pos"], bMarioDead(info["life"]))
    env.render()

