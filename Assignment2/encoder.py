import math
import numpy as np
import random,argparse,sys,os
import re   #to find float in a str

parser = argparse.ArgumentParser()

def encode(lines):

    #print(lines)
    grid_len = len( re.findall(r'\d+', lines[0]) )
    start = 0
    end = []
    mazee = [[-1 for p in range(grid_len+1)] for q in range(grid_len+1)] #creating an additional boundary around input to remove possible array index out of bounds later
    counter = 0     #for naming points on path; wall is state -1
    for line in range(0,len(lines)):
        arr = re.findall(r'\d+', lines[line])
        for t in range(0,grid_len):
            if(int(arr[t])==1):
                mazee[line][t] = -1
            else:
                if(int(arr[t])==2):
                    start = counter
                elif(int(arr[t])==3):
                    end.append(counter)
                mazee[line][t] = int(counter)
                counter += 1
    maze = np.matrix(mazee) #to display neatly
    print(maze) 
    os.chdir("D:/SoC_ADV/Assignment2/")
    mazefile = open("encoded_maze.txt", "w")
    mazefile.write(str(mazee)+str('\n'))
    mazefile.write("start "+str(start)+str('\n'))
    mazefile.write("end  "+str(end[0]))                #think about appending multiple end points!
    mazefile.close()



    N_S = counter
    N_A = 4
    gamma = 0.99

    os.chdir("D:/SoC_ADV/Assignment2/base/data/mdp/")
    encoded = open("episodic-mdp-"+str(N_S)+"-"+str(N_A)+".txt", "w")
    encoded.write("numStates "+str(N_S)+str('\n'))
    encoded.write("numActions "+str(N_A)+str('\n'))
    encoded.write("start "+str(start)+str('\n'))
    encoded.write("end  "+str(end[0])+str('\n'))                #think about appending multiple end points!


    #actions : N=0 E=1 S=2 W=3 (CW)
    
    for x in range(1,grid_len):
        
        for y in range(0,grid_len):
            if(mazee[x][y] != -1):
                if(mazee[x][y]==end[0]):                #think about multiple end points!
                    tp_to_others = 0
                    
                else:
                    take_step = [1,1,1,1]       #1 indicates transition possible, 0 indicates not possible,(0,1,2,3) = (N,E,S,W)
                    steps_possible = 4
                    if(mazee[x-1][y] == -1):      #N
                        steps_possible -= 1
                        take_step[0] = 0
                    if(mazee[x][y+1] == -1):    #E
                        steps_possible -= 1
                        take_step[1] = 0
                    if(mazee[x+1][y] == -1):    #S
                        steps_possible -= 1
                        take_step[2] = 0
                    if(mazee[x][y-1] == -1):    #W
                        steps_possible -= 1                    
                        take_step[3] = 0

                    #now actualy taking the step!     
                    p = 1.0/steps_possible
                    r0,r_reached = 0,100000000000000000000000
                    if(grid_len >= 30 and grid_len <= 39):    
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 40 and grid_len <= 49):
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 50 and grid_len <= 59):
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 60 and grid_len <= 69):
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 70 and grid_len <= 79):
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 80 and grid_len <= 89):
                        r_reached = 1000000000000000000000000000
                    elif(grid_len >= 90 and grid_len <= 100):
                        r_reached = 1000000000000000000000000000
                    #as grid size increases, the exploration increases, hence the value functions of states increases, means that the final reward
                    #must also increase, to get that shortest policy pinned!
                    #need 7 zeroes for grid30, 3 zeroes for grid10 and grid20


                    r = r0
                    
                    if(take_step[0] == 1):
                        if(mazee[x-1][y] == end[0]):
                            r = r_reached
                        encoded.write("transition " + str(mazee[x][y]) + " 0 " + str(mazee[x-1][y]) + " " + str(r) +" " + str(p) + " \n")
                        r = r0
                    if(take_step[1] == 1):
                        if(mazee[x][y+1] == end[0]):
                            r = r_reached
                        encoded.write("transition " + str(mazee[x][y]) + " 1 " + str(mazee[x][y+1]) + " " + str(r) +" " + str(p) + " \n")
                        r = r0
                    if(take_step[2] == 1):
                        if(mazee[x+1][y] == end[0]):
                            r = r_reached
                        encoded.write("transition " + str(mazee[x][y]) + " 2 " + str(mazee[x+1][y]) + " " + str(r) +" " + str(p) + " \n")
                        r = r0
                    if(take_step[3] == 1):
                        if(mazee[x][y-1] == end[0]):
                            r = r_reached
                        encoded.write("transition " + str(mazee[x][y]) + " 3 " + str(mazee[x][y-1]) + " " + str(r) +" " + str(p) + " \n")
                        r = r0

    encoded.write("mdptype episodic \n")
    encoded.write("discount "+str(gamma))

    encoded.close()















if __name__ == "__main__":
    parser.add_argument("--mdp",type=str,default="D:/SoC_ADV/Assignment2/base/data/maze/grid60.txt")
    parser.add_argument("--algorithm",type=str,default="vi")

    args = parser.parse_args()
    file = open(args.mdp)
 
    lines = file.readlines()    
    
    encode(lines)