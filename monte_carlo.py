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

# ===== DEFINATIONS ==============

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

# ====== CODE =========================

#use same seed to see same outcomes
prng.seed(1337)
random.seed(1337)

# FIRST STEP OCCURED REGARDLESS -----ROOT------
root = Node()
randomAction = env.action_space.sample()
state, reward, done, info = env.step(randomAction)
print(info)
#print(randomAction)
#save the inital life number
lifeNum = info["life"]
currentChild = root.returnChild(randomAction, info["x_pos"], bMarioDead(info["life"]))
env.render()


# RUN until completing the level
while(info['flag_get'] == False):
    #RUN until mario dies
    while(currentChild.dead == False):
        #make a random move
        randomAction = env.action_space.sample()
        state, reward, done, info = env.step(randomAction)
        #create new child node
        currentChild = currentChild.returnChild(randomAction, info["x_pos"], bMarioDead(info["life"]))
        # render the action/frame that occured
        print(gameEnv._player_state)
        env.render()

    # ---------Save TravelTree -------------------------
    # should revert time and choose a different action    


    print(gameEnv._player_state)
    #Save all actions done for mario to revert to last state
    print("===============Current Path of Random Actions =================")
    previousActions = []
    childIter = currentChild
    while(childIter != None):
        previousActions.append(childIter.action)
        childIter = childIter.parent

    previousActions.reverse()
    print(previousActions)
    #removed failed state
    previousActions.pop()

    currentChild = currentChild.parent

    # check for a node with at least a new action aviable
    while(not currentChild.unChosenChildren):
        currentChild = currentChild.parent
        previousActions.pop()

    #reset the env
    lifeNum = info["life"]
    
    env.reset()

        # setup up env back to before mario DIED
    for x in previousActions:
        #just used to skip the None Action type of root node
        if(x != None):
            #redo all actions from before except the last
            state, reward, done, info = env.step(x)
            print(info)
            print(gameEnv._is_dead)
            env.render()
    
    while(True):
        lamda = 1

    #pick another path from child not selected
    randomAction = random.choice(currentChild.unChosenChildren)
    state, reward, done, info = env.step(randomAction)
    currentChild = currentChild.returnChild(randomAction, info["x_pos"], bMarioDead(info["life"]))
    env.render()




while(True):
    lamda = 1
    print("MARIO SHOULD HAVE FINISHED!!!")
    #do nothing
#env.close()