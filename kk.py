import argparse
import numpy as np
import json
import sys
import random
import os
#test_data=json.loads("test.json")
#json.dumps(mydictionary)
# ./kk inputfile

# where you may assume inputfile is a list of 100 (unsorted) integers, one per line, and the
# desired output is the residue obtained by running Karmarkar-Karp with these 100 numbers
# as input
arr=[1,3,7,9]
signs=[1,1,1,1]
#N=len(arr)
N=100
max_iter=250
DEBUG=False

def load_int_array(inputfile):
    with open(inputfile) as f:
        lst = [int(x) for x in f.read().split()]
        return lst

def karmarkar_karp(arr):
    k=2
    while np.count_nonzero(arr)>1:
        indices = np.argpartition(arr, len(arr) - k)[-k:]
        arr[indices[1]]-=arr[indices[0]]
        arr[indices[0]]=0
    residue=np.sum(arr)
    return residue

def get_residue(arr,signs):
    return np.sum(np.dot(arr,signs))

def get_random_signs():
    return [np.random.randint(2)*2-1 for _ in range(N)]

def get_neighbor(arr):
    idx = np.random.randint(N)
    arr[idx]*=-1
    return arr

def hill_climbing_standard(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    for _ in range(max_iter):
        signs_prime = get_neighbor(signs)
        if get_residue(arr,signs_prime)<get_residue(arr,signs):
            signs=signs_prime
            num_updates+=1
            index_of_last_update=_
    #print(f"Residue of final arr: {get_residue(arr,signs)}")
    residue=get_residue(arr,signs)
    return residue,num_updates,index_of_last_update
    #return signs

def prepart_to_arr(arr, S):
    p = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        p[S[i]-1] += arr[i]
    return p

def hill_climbing_prepart(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    p = prepart_to_arr(arr, signs)
    for _ in range(max_iter):
        signs_prime = get_neighbor(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        if (karmarkar_karp(p2) < karmarkar_karp(p)):
            signs = signs_prime
            p = p2
            num_updates+=1
            index_of_last_update=_
    #print(f"Residue of Hill Climbing Prepart: {get_residue(arr,signs)}")
    residue=get_residue(arr,signs)
    return residue,num_updates,index_of_last_update
    #return signs

def T(iter):
    return 10**10 * 0.8**(int(iter/300))

def simulated_annealing_standard(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    signs_pp=signs
    for iter in range(max_iter):
        signs_prime = get_neighbor(signs)
        residue,residue_prime=get_residue(arr,signs),get_residue(arr,signs_prime)
        exp_prob = np.exp(-(residue_prime-residue)/T(iter))
        if residue_prime<residue or np.random.rand() < exp_prob:
            signs=signs_prime
        if residue<get_residue(arr,signs_pp):
            signs_pp=signs
            num_updates+=1
            index_of_last_update=iter
    #print(f"Residue of final arr: {get_residue(arr,signs_pp)}")
    residue=get_residue(arr,signs)
    return residue,num_updates,index_of_last_update
    #return signs_pp

def simulated_annealing_prepart(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    signs_pp=signs
    p = prepart_to_arr(arr, signs)
    p3 = prepart_to_arr(arr, signs_pp)
    for iter in range(max_iter):
        signs_prime = get_neighbor(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        residue,residue_prime=karmarkar_karp(p),karmarkar_karp(p2)
        exp_prob = np.exp(-(residue_prime-residue)/T(iter))
        if residue_prime<residue or np.random.rand() < exp_prob:
            signs=signs_prime
            p=p2
            if residue_prime<karmarkar_karp(p3):
                signs_pp=signs
                p3=p
                num_updates+=1
                index_of_last_update=iter
    #print(f"Residue of final arr: {get_residue(arr,signs_pp)}")
    residue=get_residue(arr,signs)
    return residue,num_updates,index_of_last_update
    #return signs_pp

def repeated_random(arr, f=0):
    if f == 1:
        if DEBUG:
            print('standard representation \narray: ', arr)
        return repeated_random_std(arr)
    if f == 11:
        if DEBUG:
            print('prepart representation \narray: ', arr)
        return repeated_random_prepart(arr)

def repeated_random_std(arr):
    num_updates,index_of_last_update=0,-1
    S = [np.random.randint(2)*2-1 for _ in range(len(arr))]
    for i in range(1, max_iter):
        S_prime = [np.random.randint(2)*2-1 for _ in range(len(arr))]
        if (get_residue(arr, S_prime) < get_residue(arr, S)):
            if DEBUG:
                print("updated S: ", S_prime)
                print("residue: ", get_residue(arr, S_prime))
            S = S_prime
            num_updates+=1
            index_of_last_update=i
    residue=get_residue(arr,S)
    return residue,num_updates,index_of_last_update
    #return S

def repeated_random_prepart(arr):
    num_updates,index_of_last_update=0,-1
    S = [random.randint(1, len(arr)) for _ in range(len(arr))]
    p = prepart_to_arr(arr, S)
    for i in range(1, max_iter):
        S_prime = [random.randint(1, len(arr)) for _ in range(len(arr))]
        p2 = prepart_to_arr(arr, S_prime)
        if (karmarkar_karp(p2) < karmarkar_karp(p)):
            if DEBUG:
                print("updated S: ", S_prime)
                print("updated array: ", p2)
                print("residue: ", karmarkar_karp(p2))
            S = S_prime
            p = p2
            num_updates+=1
            index_of_last_update=i
    residue=get_residue(arr,S)
    return residue,num_updates,index_of_last_update
    #return S

def get_inputfile_from_command_line():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('text', action='store', type=str, help='The text to parse.')
    args = parser.parse_args()
    inputfile = args.text
    print(inputfile)

# @param partition_function - returns residue,num_updates,index_of_last_update given integer array
def run_alg_50_times(partition_function):
    print(partition_function)
    residues,updates,indices=[],[],[]
    for filename in [f"test{i}.txt" for i in range(1,51)]:
        #print(filename)
        arr = load_int_array(filename)
        if partition_function==karmarkar_karp:
            residue,num_updates,index_of_last_update=partition_function(arr),-1,-1
        else:
            residue,num_updates,index_of_last_update=partition_function(arr)
        residue=float(residue)
        residues.append(residue)
        updates.append(num_updates)
        indices.append(index_of_last_update)
    # Return residues,updates,indices arrays of 50 values
    return residues,updates,indices


def get_tests_data():
    alg_names=["K-Karp","Rep Rand","Hill Climb","Sim Anneal", "Prepart Rep Rand","Prepart Hill Climb","Prepart Sim Anneal"]
    alg_functions=[karmarkar_karp,repeated_random_std,hill_climbing_standard,simulated_annealing_standard,repeated_random_prepart,hill_climbing_prepart,simulated_annealing_prepart]
    # Each list contains 50 values, 1 for each trial
    # residues: residue values
    # updates: number of updates of S
    # indices: index of iteration of last update
    d = {"residues":{an:[] for an in alg_names},"updates":{an:[] for an in alg_names},"indices":{an:[] for an in alg_names}}

    for i in range(len(alg_names)):
        residues,updates,indices=run_alg_50_times(alg_functions[i])
        d['residues'][alg_names[i]]=residues
        d['updates'][alg_names[i]]=updates
        d['indices'][alg_names[i]]=indices
    print(d)
    with open('tests_data.json', 'w') as fp:
        json.dump(d, fp)
    #json.dumps(d,"tests_data.json")


if __name__ == '__main__':
    args = sys.argv
    DEBUG, c, inputfile = int(args[1]), int(args[2]), args[3]

    #get_tests_data()

    #inputfile = "test2.txt"
    arr = load_int_array(inputfile)
    #arr = [np.random.randint(N) for _ in range(100)]
    print(karmarkar_karp(arr))

# Track num total updates, index of last update
#