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
N_velo_states = 16
epsilon = -0.1
guided = False
qsa0 = [[[0.0 for p in range(0,3)] for q in range(N_velo_states)] for r in range(N_boxes)]
qsa1 = [[[0.0 for p in range(0,5)] for q in range(N_velo_states)] for r in range(N_boxes)]

# for q in range(N_boxes):
#     for r in range(N_velo_states):
#         qsa1[q][r][0] = 100*random.random()   
#         qsa1[q][r][1] = 100*random.random()   
#         qsa1[q][r][2] = 100*random.random()   
#         qsa1[q][r][3] = 100*random.random()   
#         qsa1[q][r][4] = 500   

# for q in range(N_boxes):
#     for r in range(N_velo_states):
#         qsa0[q][r][1] = 100*random.random()   
#         qsa0[q][r][2] = 100*random.random()  
#         qsa0[q][r][0] = 100*random.random()  
qsa0 = [[[1.3908056566866173e+39, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.3429459576186237e+39, 0.0, 0.0], [0.0, 1.39788759475431e+39, 0.0], [0.0, 1.7647452212431637e+39, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.330907677416112e+39, 0.0, 0.0], [1.9516323697648837e+39, 0.0, 6.549400062155779e+38], [6.982489207858865e+38, 1.4834891281448137e+39, 0.0], [1.4999058446041943e+39, 0.0, 0.0]], [[6.885367230816199e+38, 4.860903628796343e+38, 5.079670346979857e+38], [0.0, 0.0, 0.0], [5.1979165135710314e+38, 0.0, 0.0], [1.4682127295811084e+39, 1.689079877045473e+39, 0.0], [0.0, 0.0, 0.0], [5.3082827400912334e+38, 0.0, 0.0], [0.0, 0.0, 1.663807037361127e+39], [0.0, 0.0, 7.10226664524608e+38], [1.4865769398194536e+39, 4.875515553786556e+38, 0.0], [0.0, 6.789596158607592e+38, 0.0], [0.0, 0.0, 1.3605270766427166e+39], [1.4317503232079543e+39, 0.0, 0.0], [4.9690832175285175e+38, 6.728733649170392e+38, 6.823646221455006e+38], [6.810005752658317e+38, 5.019048446041942e+38, 6.803195746905658e+38], [4.8511866824423786e+38, 4.856042725167546e+38, 4.860903628796342e+38], [4.865769398194537e+38, 0.0, 0.0]], [[1.3838655225586472e+39, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [4.969083217528516e+38, 0.0, 0.0], [1.4418127850478178e+39, 0.0, 0.0], [0.0, 0.0, 0.0], [4.959150020176676e+38, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.490487130658032e+39, 4.9097810876679896e+38], [5.009015368198303e+38, 0.0, 0.0]]]
qsa1 = [[[0.0, 0.0, 0.0, 1.519177834252208e+39, 5.079670346979857e+38], [0.0, 0.0, 0.0, 4.899966435273744e+38, 9.050755719235907e+38], [0.0, 0.0, 0.0, 0.0, 4.764603609955654e+38], [0.0, 0.0, 0.0, 0.0, 8.915940607031185e+38], [0.0, 0.0, 0.0, 6.4712380841827685e+38, 0.0], [0.0, 0.0, 0.0, 5.004006352830106e+38, 0.0], [0.0, 0.0, 0.0, 0.0, 9.439181521088595e+38], [0.0, 0.0, 0.0, 6.419649012238956e+38, 0.0], [0.0, 0.0, 0.0, 9.785358962312019e+38, 4.726619923492541e+38], [0.0, 0.0, 0.0, 9.785358962312019e+38, 9.785358962312019e+38], [0.0, 0.0, 0.0, 9.775573603349707e+38, 4.693632677780121e+38], [0.0, 0.0, 0.0, 4.717171410265479e+38, 4.7789260561247865e+38], [0.0, 0.0, 0.0, 0.0, 1.3004818937281233e+39], [0.0, 0.0, 0.0, 1.1449726434204052e+39, 0.0], [0.0, 0.0, 0.0, 1.4564409824917265e+39, 4.619095170944615e+38], [0.0, 0.0, 0.0, 1.4725583764083837e+39, 4.75032408817201e+38]], [[0.0, 0.0, 0.0, 9.687944541651588e+38, 4.411328186196818e+38], [0.0, 0.0, 0.0, 6.40681613386349e+38, 5.8609863870587905e+38], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.1158967393619622e+39, 5.1000399268427266e+38], [0.0, 0.0, 0.0, 0.0, 1.2541101469889317e+39], [0.0, 0.0, 0.0, 0.0, 1.0256491280658994e+39], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 4.4069168580106215e+38, 1.440250994115261e+39], [0.0, 0.0, 0.0, 1.0643286450568563e+39, 4.7550791673393486e+38], [0.0, 0.0, 0.0, 4.9940033441307954e+38, 1.3294241660216367e+39], [0.0, 0.0, 0.0, 1.6665382810655688e+39, 1.3495259675038646e+39], [0.0, 0.0, 0.0, 9.601100994212341e+38, 4.460145209974155e+38], [0.0, 0.0, 0.0, 4.491491486100745e+38, 4.491491486100745e+38], [0.0, 0.0, 0.0, 4.332595625874914e+38, 4.336932558433347e+38], [0.0, 0.0, 0.0, 4.3586824273106624e+38, 4.354323744883352e+38]], [[1.0590176344800568e+39, 0.0, 0.0, 6.112518790281489e+38, 0.0], [6.4971878785519595e+38, 0.0, 0.0, 5.1771560142293636e+38, 0.0], [0.0, 0.0, 0.0, 5.1564784324050846e+38, 6.516718490384361e+38], [5.802639565486582e+38, 0.0, 0.0, 5.486469074854968e+38, 4.895066468838471e+38], [0.0, 0.0, 0.0, 0.0, 6.033531078655691e+38], [0.0, 0.0, 0.0, 0.0, 1.3671932284432862e+39], [0.0, 0.0, 0.0, 4.614476075773671e+38, 0.0], [5.2031196332042365e+38, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 9.150913979628164e+38, 5.0644465698702846e+38], [0.0, 0.0, 0.0, 4.999002346477276e+38, 9.023630595294603e+38], [0.0, 0.0, 0.0, 5.0543227411771185e+38, 1.0338913678762105e+39], [0.0, 0.0, 0.0, 4.86576939819454e+38, 4.846335495759938e+38], [0.0, 0.0, 0.0, 4.851186682442381e+38, 5.4427306365316955e+38], [0.0, 0.0, 0.0, 4.527585652147787e+38, 5.530559000531677e+38], [0.0, 0.0, 0.0, 1.4573111525195287e+39, 4.5776892144096955e+38], [0.0, 0.0, 0.0, 4.523058066495639e+38, 4.755079167339349e+38]]]
class Task1():

    def __init__(self):


        super().__init__()
    def getState(self,state):
        global qsa0,qsa1,epsilon,gamma,alpha,guided
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
        s_velo = angle + moving * 8

        s_box = 0
        #180*180 centered at (350 - 90, (150-100)/2)
        y = state[1] 
        if(y>(25-60) and y<(25+60)):
            s_box = 2
        elif(y<(25-60)):
            s_box = 1
        else:
            s_box = 0


        # print(state[3])
        # print(s_box," ",int(x)," ",int(y)) 

        return s_box,s_velo

    def next_action(self, state):
        global qsa0,qsa1,epsilon,gamma,alpha,guided
        sbox,svelo = self.getState(state)
        action_steer,action_acc = 0, 0

        if(sbox<N_boxes+1):
            if(random.random()>epsilon):
                q0_fordiff_a = qsa0[sbox][svelo]
                q1_fordiff_a = qsa1[sbox][svelo]
                action_steer = q0_fordiff_a.index(max(q0_fordiff_a))
                action_acc = q1_fordiff_a.index(max(q1_fordiff_a))
            else:
                action_steer = np.random.randint(low = 0, high = 3, dtype = int)
                action_acc = np.random.randint(low = 3, high = 5, dtype = int)
        else:
            x = state[0]
            y = state[1]
            action_steer, action_acc = 1,3
            if guided:
                if(y<-65):
                    if(state[3]>70 and state[3]<110):
                        action_steer = 1
                        action_acc = 4
                    else:
                        action_steer = 0
                        action_acc = 0

                elif(y>105):
                    if(state[3]>250 and state[3]<290):
                        action_steer = 1
                        action_acc = 4
                    else:
                        action_steer = 0
                        action_acc = 0
                else:
                    if(state[3]>320):
                        action_steer = 1
                        action_acc = 4
                    else:
                        action_steer = 0
                        action_acc = 0
            else:
                if(y<-65):
                    sbox = 1
                elif(y>105):
                    sbox = 0
                else:
                    sbox = 2
                q0_fordiff_a = qsa0[sbox][svelo]
                q1_fordiff_a = qsa1[sbox][svelo]
                action_steer = q0_fordiff_a.index(max(q0_fordiff_a))
                action_acc = q1_fordiff_a.index(max(q1_fordiff_a))
        action = np.array([action_steer, action_acc])  
        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        global qsa0,qsa1,epsilon,gamma,alpha,guided

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

        f = open('value function.txt','w')
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
                epsilon = 0.2
            if(e>50):
                epsilon = 0.2    
            if(e>250):
                guided = False


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
                if(sbox_ < N_boxes + 1 and sbox < N_boxes + 1):
                    qsa0[sbox][svelo][action[0]] = qsa0[sbox][svelo][action[0]] + alpha*(reward + gamma*qsa0[sbox_][svelo_][action_[0]] - qsa0[sbox][svelo][action[0]])
                    qsa1[sbox][svelo][action[1]] = qsa1[sbox][svelo][action[1]] + alpha*(reward + gamma*qsa1[sbox_][svelo_][action_[1]] - qsa1[sbox][svelo][action[1]])
                elif(sbox< N_boxes + 1 and sbox_ >= N_boxes + 1):
                    reward = -100
                    qsa0[sbox][svelo][action[0]] = qsa0[sbox][svelo][action[0]] + alpha*(reward - qsa0[sbox][svelo][action[0]])
                    qsa1[sbox][svelo][action[1]] = qsa1[sbox][svelo][action[1]] + alpha*(reward - qsa1[sbox][svelo][action[1]])
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
            if(e%40 == 0):
                f.write("Episode = " + str(e) + "\n\n")
                f.write(str(qsa0) + "\n\n\n\n")
                f.write(str(qsa1) + "\n\n\n\n")
        print(qsa0)
        print(qsa1)
        f.close()



class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
    def getState(self,state):

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
