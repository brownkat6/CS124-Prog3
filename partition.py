import argparse
import numpy as np
import json
import sys
import random
import os
import heapq
import math

N=100
max_iter=10000
DEBUG=False

# Referenced CLRS textbook for pseudocode on implementing a max heap
def max_heapify(A,i):
    l,r = 2*i,2*i+1 # Left(i), Right(i)
    if l < len(A) and A[l]>A[i]:
        largest=l
    else:
        largest=i
    if r < len(A) and A[r]>A[largest]:
        largest=r
    if largest != i:
        A[i],A[largest]=A[largest],A[i]
        max_heapify(A,largest)
def build_max_heap(A):
    for i in range(len(A)//2,-1,-1):
        max_heapify(A,i)
def heap_extract_max(A):
    if len(A)<1:
        print("Error: couldn't extract max because list has no elements'")
        return -1
    maxv = A[0]
    A[0] = A[-1]
    A.pop()
    max_heapify(A,0)
    return maxv
def heap_increase_key(A,i,key):
    if key<A[i]:
        print("Error: new key is smaller than current key")
    A[i]=key
    while i>0 and A[i//2]<A[i]:
        A[i],A[i//2]=A[i//2],A[i]
        i=i//2
def max_heap_insert(A,key):
    A.append(-math.inf)
    heap_increase_key(A,len(A)-1,key)

def load_int_array(inputfile):
    with open(inputfile) as f:
        lst = [int(x) for x in f.read().split()]
        return lst

def karmarkar_karp(arr):
    arr = [n for n in arr]
    build_max_heap(arr)
    v1,v2=heap_extract_max(arr),heap_extract_max(arr)
    while v2 != 0:
        max_heap_insert(arr,abs(v1-v2))
        max_heap_insert(arr,0)
        v1,v2=heap_extract_max(arr),heap_extract_max(arr)
    return v1

def get_residue(arr,signs):
    return np.abs(np.sum(np.dot(arr,signs)))

def get_random_signs():
    return [np.random.randint(2)*2-1 for _ in range(N)]

def get_neighbor_std(arr):
    arr = [n for n in arr] # Copy array in place
    idx = np.random.randint(N)
    idx2 = np.random.randint(N)
    while (idx2 == idx):
        idx2 = np.random.randint(N)
    arr[idx]*=-1
    if random.randint(0, 1) == 1:
        arr[idx2]*=-1
    return arr

#A random move on this state space can be defined as follows. Choose two random indices i and j from [1, n] with i ??= j. Set si to ???si and with probability 1/2, set sj to ???sj .

def get_neighbor_prepart(arr):
    arr = [n for n in arr] # Copy array in place
    idx = np.random.randint(N)
    arr[idx] = random.randint(1, N)
    return arr
"""A random solution can be obtained by generating a sequence of n values in the range [1, n] and using
this for P . Thinking of all possible solutions as a state space, a natural way to define neighbors of a
solution P is as the set of all solutions that differ from P in just one place. The interpretation is that we
change the prepartitioning by changing the partition of one element. A random move on this state space
can be defined as follows. Choose two random indices i and j from [1, n] with pi ??= j and set pi to j."""

def hill_climbing_standard(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    for i in range(max_iter):
        signs_prime = get_neighbor_std(signs)
        if get_residue(arr,signs_prime)<get_residue(arr,signs):
            signs=signs_prime
            num_updates+=1
            index_of_last_update=i
    residue=get_residue(arr,signs)
    return residue,num_updates,index_of_last_update

def prepart_to_arr(arr, S):
    p = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        p[S[i]-1] += arr[i]
    return p

def hill_climbing_prepart(arr):
    num_updates,index_of_last_update=0,-1
    signs = [random.randint(1, len(arr)) for _ in range(len(arr))]
    p = prepart_to_arr(arr, signs)
    for i in range(max_iter):
        signs_prime = get_neighbor_prepart(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        if (karmarkar_karp(p2) < karmarkar_karp(p)):
            signs = signs_prime
            p = p2
            num_updates+=1
            index_of_last_update=i
    residue=karmarkar_karp(p)
    return residue,num_updates,index_of_last_update

def T(iter):
    return 10**10 * 0.8**(int(iter/300))

def simulated_annealing_standard(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    signs_pp=signs
    for iter in range(max_iter):
        signs_prime = get_neighbor_std(signs)
        residue,residue_prime=get_residue(arr,signs),get_residue(arr,signs_prime)
        exp_prob = np.exp(-(residue_prime-residue)/T(iter))
        if residue_prime<residue or np.random.rand() < exp_prob:
            signs=signs_prime
        if residue<get_residue(arr,signs_pp):
            signs_pp=signs
            num_updates+=1
            index_of_last_update=iter
    residue=get_residue(arr,signs_pp)
    return residue,num_updates,index_of_last_update

def simulated_annealing_prepart(arr):
    num_updates,index_of_last_update=0,-1
    signs = get_random_signs()
    signs_pp=signs
    p = prepart_to_arr(arr, signs)
    p3 = prepart_to_arr(arr, signs_pp)
    for iter in range(max_iter):
        signs_prime = get_neighbor_prepart(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        residue,residue_prime=karmarkar_karp(p),karmarkar_karp(p2)
        exp_prob = np.exp(-(residue_prime-residue)/T(iter))
        if residue_prime<residue or np.random.rand() < exp_prob:
            signs=signs_prime
            p=p2
        if residue<karmarkar_karp(p3):
            signs_pp=signs
            p3=p
            num_updates+=1
            index_of_last_update=iter
    residue=karmarkar_karp(p3)
    return residue,num_updates,index_of_last_update

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
    S = get_random_signs()
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
    residue=karmarkar_karp(p)#get_residue(arr,S)
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
    #print(partition_function)
    residues,updates,indices=[],[],[]
    for i,filename in enumerate([f"test{i}.txt" for i in range(1,51)]):
        if i%10==0 or i==1 or i==2:
            print(partition_function,i)
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
    with open('tests_data.json', 'w') as fp:
        json.dump(d, fp)

def main():
    args = sys.argv
    DEBUG, c, inputfile = int(args[1]), int(args[2]), args[3]

    partition_functions = {0:karmarkar_karp,1:repeated_random_std,2:hill_climbing_standard,3:simulated_annealing_standard,11:repeated_random_prepart,12:hill_climbing_prepart,13:simulated_annealing_prepart}
    partition_function = partition_functions[c]

    arr = load_int_array(inputfile)
    if c==0:
        print(karmarkar_karp(arr))
    else:
        print(partition_function(arr)[0])

if __name__ == '__main__':
    main()