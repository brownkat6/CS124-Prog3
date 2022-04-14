import argparse
import sys
import numpy as np
import random
import time
# ./rr inputfile

#inputfile = 100 (unsorted) integers, one per line
#output = residue returned by Repeated-Random

#rep1 =  +1, -1
#rep2 = pre-partition (determinative residue assuming +kk)

max_iter = 2500

def load_int_array(inputfile):
    with open(inputfile) as f:
        lst = [int(x) for x in f.read().split()]
        return lst

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
    S = [np.random.randint(2)*2-1 for _ in range(len(arr))]
    for x in range(1, max_iter):
        S_prime = [np.random.randint(2)*2-1 for _ in range(len(arr))]
        if (residue_std(arr, S_prime) < residue_std(arr, S)):
            if DEBUG:
                print("updated S: ", S_prime)
                print("residue: ", residue_std(arr, S_prime))
            S = S_prime
    return S

def residue_std(arr, S):
    s1 = sum(arr[i] for i in range(len(arr)) if S[i] == 1)
    s2 = sum(arr[i] for i in range(len(arr)) if S[i] == -1)
    return abs(s1-s2)

def repeated_random_prepart(arr):
    S = [random.randint(1, len(arr)) for _ in range(len(arr))]
    p = prepart_to_arr(arr, S)
    for x in range(1, max_iter):
        S_prime = [random.randint(1, len(arr)) for _ in range(len(arr))]
        p2 = prepart_to_arr(arr, S_prime)
        if (karmarkar_karp(p2) < karmarkar_karp(p)):
            if DEBUG:
                print("updated S: ", S_prime)
                print("updated array: ", p2)
                print("residue: ", karmarkar_karp(p2))
            S = S_prime
            p = p2
    return S

def prepart_to_arr(arr, S):
    p = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        p[S[i]-1] += arr[i]
    return p 

def karmarkar_karp(arr):
    k=2
    while np.count_nonzero(arr)>1:
        indices = np.argpartition(arr, len(arr) - k)[-k:]
        arr[indices[1]]-=arr[indices[0]]
        arr[indices[0]]=0
    #print("karmarker output:",np.sum(arr))
    return np.sum(arr)

def get_inputfile_from_command_line():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('text', action='store', type=str, help='The text to parse.')
    args = parser.parse_args()
    inputfile = args.text
    print(inputfile)

if __name__ == '__main__':
    global DEBUG
    args = sys.argv
    DEBUG, c, inputfile = int(args[1]), int(args[2]), args[3]
    arr = load_int_array(inputfile)

    #arr = [np.random.randint(10) for _ in range(5)]

    t1 = time.time()
    repeated_random(arr, c) #UPDATE c
    print('iterations, time: ', max_iter, time.time()-t1)