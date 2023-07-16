from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse
import numpy as np

# Do NOT change these values
TIMESTEPS = 1000
FPS = 5
NUM_EPISODES = 500
alpha = 1
gamma = 0.999
N_boxes = 3
N_velo_states = 8
epsilon = -0.1
qsa0 = [[[0.0 for p in range(0,3)] for q in range(N_velo_states)] for r in range(N_boxes)]
qsa1 = [[[0.0 for p in range(0,5)] for q in range(N_velo_states)] for r in range(N_boxes)]

for q in range(N_boxes):
    for r in range(N_velo_states):
        qsa1[q][r][0] = 100*random.random()   
        qsa1[q][r][1] = 100*random.random()   
        qsa1[q][r][2] = 100*random.random()   
        qsa1[q][r][3] = 100*random.random()   
        qsa1[q][r][4] = 500   

for q in range(N_boxes):
    for r in range(N_velo_states):
        qsa0[q][r][1] = 100*random.random()   
        qsa0[q][r][2] = 100*random.random()  
        qsa0[q][r][0] = 100*random.random()  

qsa0[0][1][1] = 100
qsa0[1][6][1] = 100
qsa0[2][0][1] = 100



class Task1():

    def __init__(self):


        super().__init__()
    def getState(self,state):
        global qsa0,qsa1,epsilon,gamma,alpha
        # X = int(math.floor(state[0]/100.0)) + 5
        # Y = int(math.floor(state[1]/100.0)) + 5
        # s_box = X*10 + Y 

        moving = 0
        if(state[2]>0):
            moving = 1
        angle = 0
        if(state[3]<=45):
            angle = 0
        elif(state[3]<=90):
            angle = 1
        elif(state[3]<=135):
            angle = 2
        elif(state[3]<=180):
            angle = 3
        elif(state[3]<=225):
            angle = 4
        elif(state[3]<=270):
            angle = 5
        elif(state[3]<=315):
            angle = 6
        else:
            angle = 7
        s_velo = angle #+ moving * 8

        s_box = 0
        # if(state[0]>250):
        #     s_box = 1
        # with the above two lines, the car is learning to turn towards to the right correctly and move horizontally. now we need to adjust vertical height of horiz motion 

        if(state[1]>-110 and state[1]<80):
            s_box = 2
        elif(state[1]<150):
            s_box = 1
        else:
            s_box = 0


        # print( s_box," ",int(state[0])," ",int(state[1]) )

        return s_box,s_velo

    def next_action(self, state):
        global qsa0,qsa1,epsilon,gamma,alpha
        sbox,svelo = self.getState(state)
        action_steer,action_acc = 0, 0

        if(random.random()>epsilon):
            q0_fordiff_a = qsa0[sbox][svelo]
            q1_fordiff_a = qsa1[sbox][svelo]
            action_steer = q0_fordiff_a.index(max(q0_fordiff_a))
            action_acc = q1_fordiff_a.index(max(q1_fordiff_a))
        else:
            action_steer = np.random.randint(low = 0, high = 3, dtype = int)
            action_acc = np.random.randint(low = 3, high = 5, dtype = int)
        action = np.array([action_steer, action_acc])  
        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        global qsa0,qsa1,epsilon,gamma,alpha

        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(2)
        ##############################################
#Ideation:
################################################################################
#divide the 1000*1000 board into squares of 50*50 and 0 for stationary, 1 for moving, 4 quadrants for angles => 400*2*4 states.
#Q_S_A_0 for steering and Q_S_A_1 for acceleration i.e. 400*3 and 400*5
################################################################################

        
        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################
            if(e>0):
                epsilon = 0.1


            sbox,svelo = self.getState(state)
            action = self.next_action(state)


            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                




                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                sbox_,svelo_ = self.getState(state)
                action_ = self.next_action(state)
                qsa0[sbox][svelo][action[0]] = qsa0[sbox][svelo][action[0]] + alpha*(reward + gamma*qsa0[sbox_][svelo_][action_[0]] - qsa0[sbox][svelo][action[0]])
                qsa1[sbox][svelo][action[1]] = qsa1[sbox][svelo][action[1]] + alpha*(reward + gamma*qsa1[sbox_][svelo_][action_[1]] - qsa1[sbox][svelo][action[1]])
                cur_time += 1

                sbox,svelo = sbox_,svelo_
                action[0] = action_[0]
                action[1] = action_[1]




                if terminate:
                    road_status = reached_road
                    break
                # print("x= ",state[0]," y= ",state[1],"\t\t",state[3],"\t\t")

            # Writing the output at each episode to STDOUT
            print(e,"\t",str(road_status) ,"\t",str(cur_time))
            if(e%30 == 0):
                print(qsa0,"\t",qsa1)
        print(qsa0)
        print(qsa1)


class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
    def getState(self,state):
        # X = int(math.floor(state[0]/100.0)) + 5
        # Y = int(math.floor(state[1]/100.0)) + 5
        # s_box = X*10 + Y 

        moving = 0
        if(state[2]>0):
            moving = 1
        angle = 0
        if(state[3]<=90):
            angle = 0
        elif(state[3]<=180):
            angle = 1
        elif(state[3]<=270):
            angle = 2
        else:
            angle = 3
        s_velo = angle + moving * 4

        s_box = 0
        if(state[1]>-50 and state[1]<50):
            s_box = 1
        # if(state[1]>-30 and state[1]<30):
        #     if(state[0]>0):
        #         s_box = 2
        else:
            s_box = 0
            

        # print(X,"\t",Y,"\t",s_box)

        return s_box,s_velo

    def next_action(self, state):
        sbox,svelo = self.getState(state)
        q0_fordiff_a = qsa0[sbox][svelo]
        q1_fordiff_a = qsa1[sbox][svelo]
        action_steer = q0_fordiff_a.index(max(q0_fordiff_a))
        action_acc = q1_fordiff_a.index(max(q1_fordiff_a))
        # if(state[3]>270):
        #     action_steer = 1

        # if(state[2]<1):
        #     action_acc = 4
        # elif(state[2]>1 and state[2] < 3):
        #     action_acc = 3
        # elif(state[2] > 6):
        #     action_acc = 1
        # elif(state[2] > 7):
        #     action_acc = 0
        action = np.array([action_steer, action_acc])
        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False
            sbox,svelo = self.getState(state)
            action = self.next_action(state)

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)
                sbox_,svelo_ = self.getState(state)
                action_ = self.next_action(state)
                qsa0[sbox][svelo][action[0]] = qsa0[sbox][svelo][action[0]] + alpha*(reward + gamma*qsa0[sbox_][svelo_][action_[0]] - qsa0[sbox][svelo][action[0]])
                qsa1[sbox][svelo][action[1]] = qsa1[sbox][svelo][action[1]] + alpha*(reward + gamma*qsa1[sbox_][svelo_][action_[1]] - qsa1[sbox][svelo][action[1]])
                cur_time += 1

                sbox,svelo = sbox_,svelo_
                action[0] = action_[0]
                action[1] = action_[1]


                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(e,"\t",str(road_status),"\t", str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
