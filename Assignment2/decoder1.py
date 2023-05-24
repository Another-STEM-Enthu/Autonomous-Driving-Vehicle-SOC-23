import math
import numpy as np
import random,argparse,sys,os
import re   #to find float in a str

parser = argparse.ArgumentParser()


def find_xy(mazee,grid_len,state):
    for i in range(0,grid_len):
        for j in range(0,grid_len):
            if(mazee[i][j] == state):
                return i,j


def decode(gridlines, policylines):
    arr = (re.findall( r'[+-]?\d+\.*\d*', gridlines[0]))
    start = int(re.findall(r'\d+', gridlines[1])[0])
    end = int(re.findall(r'\d+', gridlines[2])[0])
    grid_len = int(math.sqrt(len(arr)))
    mazee = [[-1 for p in range(grid_len+1)] for q in range(grid_len+1)]
    
    #storing the text maze into an array
    for x in range(0,grid_len):
        for y in range(0,grid_len):
            mazee[x][y] = int(arr[x*grid_len + y])

    N_S = int(re.findall(r'\d+', policylines[0])[0])
    N_A = int(re.findall(r'\d+', policylines[1])[0])
    V = [0.0 for p in range(N_S)]
    A = [0 for p in range(N_S)]

    #the values
    for u in range(2, 2+ N_S):
        V[u-2] = float(policylines[u])
    #the actions
    for u in range(2 +N_S, 2 + 2*N_S):
        A[u-2-N_S] = int(policylines[u]) 

    #now let us simulate   
    state = [0]
    state[0] = start
    steps = []

    while(state[-1]!=end):
        action = A[state[-1]]
        x,y = find_xy(mazee,grid_len,state[-1])

        if(action == 0):
            state.append(mazee[x-1][y])
            steps.append("N")
            # print(x,y)
        elif(action == 1):
            state.append(mazee[x][y+1])
            steps.append("E")
            # print(x,y)
        elif(action == 2):
            state.append(mazee[x+1][y])
            steps.append("S")
            # print(x,y)
        elif(action == 3):
            state.append(mazee[x][y-1])
            steps.append("W")
            # print(x,y)
        print(state[-1],"\t\t",action)
    
    os.chdir("D:/SoC_ADV/Assignment2/")
    pathfile = open("path.txt", "w")
    for p in range(0,len(steps)):
        print(steps[p], end =" ")
        pathfile.write(str(steps[p])+" ")
    pathfile.close()
    
    


if __name__ == "__main__":
    parser.add_argument("--grid",type=str,default="D:/SoC_ADV/Assignment2/base/data/mdp/episodic-mdp-209-4.txt")
    parser.add_argument("--algorithm",type=str,default="vi")

    file = open("D:/SoC_ADV/Assignment2/encoded_maze.txt")
    gridlines = file.readlines()    
    file.close()
    file = open("D:/SoC_ADV/Assignment2/value_and_policy_file.txt")
    policylines = file.readlines() 
    file.close()
    decode(gridlines,policylines)