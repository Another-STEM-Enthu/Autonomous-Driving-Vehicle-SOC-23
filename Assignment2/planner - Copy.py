import math
import numpy as np
import random,argparse,sys
import re   #to find float in a str
from pulp import *   #lp solver

parser = argparse.ArgumentParser()

def solve(filename, algo="vi"):
    file = open(filename)
    lines = file.readlines()
    file.close()
    N_S = int( re.findall(r'\d+', lines[0])[0] ) 
    N_A = int( re.findall(r'\d+', lines[1])[0] )
    start = int( re.findall(r'\d+', lines[2])[0] )
    end = ( re.findall(r'\d+', lines[3]) )
    gamma = float( (re.findall( r'[+-]?\d+\.*\d*', lines[-1]))[0] ) 


    tpm = [[[0 for p in range(N_A)] for q in range(N_S)] for r in range(N_S)]
    rewards = [[[0 for p in range(N_A)] for q in range(N_S)] for r in range(N_S)]

    N_defs = len(lines) - 6
    for i in range(4,N_defs+4) :
        arr = re.findall( r'[+-]?\d+\.*\d*', lines[i])
        arr[0] = int(arr[0])
        arr[1] = int(arr[1])
        arr[2] = int(arr[2])
        arr[3] = float(arr[3])
        arr[4] = float(arr[4])
        tpm[arr[0]][arr[2]][arr[1]] = arr[4]        #tpm[s1][s2][action]
        rewards[arr[0]][arr[2]][arr[1]] = arr[3]               
        # print(arr)
        # print(tpm)
        # print(i)

    V = [0 for p in range(N_S)]     #value function 
    V[start] = 1
    A = [0 for p in range(N_S)]     #policy
    a = [0 for p in range(N_S)]     # temporary variable for policy



    if(algo == "vi"):
        delta = 0.1
        while(delta>1e-10):
            sum_diff = 0
            vn = [0 for p in range(N_S)]
            an = [0 for p in range(N_S)]
            for p in range(0,N_S):
                vn[p] = V[p]
                an[p] = A[p]

            for s in range(0,N_S): 
                sum_fordiff_a = [0 for p in range(N_A)]
                for action in range(0,N_A):
                    sum = 0 
                    for s_ in range(0,N_S):
                        sum += tpm[s][s_][action]*(rewards[s][s_][action] + gamma*vn[s_])    #s_ is s'
                    sum_fordiff_a[action] = sum
                max_a = sum_fordiff_a.index(max(sum_fordiff_a))
                A[s] = max_a
                V[s] = max(sum_fordiff_a)
            # print(delta)

            for u in range(0,N_S):
                sum_diff += abs(an[u] - A[u])
            delta = sum_diff
            
        for p in range(0,N_S):  #results
            print(V[p],"\t",A[p])




    elif(algo == "hpi"):
        
        #policy improvement:
        policy_stable = False

        while(not(policy_stable)):
            #policy evaluation:
            delta_pe = 0.1
            while(delta_pe>1e-10):
                sum_diff = 0
                vn = [0 for p in range(N_S)]
                for p in range(0,N_S):
                    vn[p] = V[p]

                for s in range(0,N_S): 
                    sum = 0 
                    for s_ in range(0,N_S):
                        sum += tpm[s][s_][A[s]]*(rewards[s][s_][A[s]] + gamma*vn[s_])    #s_ is s'
                    V[s] = sum

                for u in range(0,N_S):
                    sum_diff += abs(vn[u] - V[u])
                delta_pe = sum_diff


            policy_stable = True
            for s in range(0,N_S):
                a[s] = A[s]     #a = pi(s)
                
                sum_fordiff_a = [0 for p in range(N_A)]
                for action in range(0,N_A):
                    sum = 0 
                    for s_ in range(0,N_S):
                        sum += tpm[s][s_][action]*(rewards[s][s_][action] + gamma*V[s_])    #s_ is s'
                    sum_fordiff_a[action] = sum
                max_a = sum_fordiff_a.index(max(sum_fordiff_a))
                A[s] = max_a    #pi(s) = argmax ()
                
                if(a[s] != A[s]):
                    policy_stable = False



        for p in range(0,N_S):  #results
            print(V[p],"\t",A[p])




    elif(algo == "lp"):
        problem = LpProblem("mdp")
        choices = LpVariable.dicts("Choice",(V,A),cat = "Continuous")


    os.chdir("D:/SoC_ADV/Assignment2/")
    policyfile = open("value_and_policy_file.txt", "w")
    policyfile.write("numStates "+str(N_S)+str('\n'))
    policyfile.write("numActions "+str(N_A)+str('\n'))
    for p in range(0,N_S): 
        policyfile.write(str(V[p])+str('\n'))
    for p in range(0,N_S): 
        if(p!=(N_S -1)):
            policyfile.write(str(A[p])+str('\n'))
        else:
            policyfile.write(str(A[p]))
    policyfile.close()







if __name__ == "__main__":
    parser.add_argument("--mdp",type=str,default="D:/SoC_ADV/Assignment2/base/data/mdp/episodic-mdp-2584-4.txt")
    parser.add_argument("--algorithm",type=str,default="vi")

    args = parser.parse_args()

    solve(args.mdp,args.algorithm)