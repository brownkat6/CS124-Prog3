import argparse
import numpy as np
import json
#json.loads("myjson.json")
#json.dumps(mydictionary)
# ./kk inputfile

# where you may assume inputfile is a list of 100 (unsorted) integers, one per line, and the
# desired output is the residue obtained by running Karmarkar-Karp with these 100 numbers
# as input
arr=[1,3,7,9]
signs=[1,1,1,1]
N=len(arr)
max_iter=25000
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
    #print("karmarker output:",np.sum(arr))
    return np.sum(arr)

def get_residue(arr,signs):
    return np.sum(np.dot(arr,signs))

def get_random_signs():
    return [np.random.randint(2)*2-1 for _ in range(N)]

def get_neighbor(arr):
    idx = np.random.randint(N)
    arr[idx]*=-1
    return arr

def hill_climbing_standard(arr,max_iter=10):
    signs = get_random_signs()
    for _ in range(max_iter):
        signs_prime = get_neighbor(signs)
        if get_residue(arr,signs_prime)<get_residue(arr,signs):
            signs=signs_prime
    print(f"Residue of final arr: {get_residue(arr,signs)}")
    return signs

def prepart_to_arr(arr, S):
    p = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        p[S[i]-1] += arr[i]
    return p

def hill_climbing_prepart(arr,max_iter=10):
    signs = get_random_signs()
    p = prepart_to_arr(arr, signs)
    for _ in range(max_iter):
        signs_prime = get_neighbor(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        if (karmarkar_karp(p2) < karmarkar_karp(p)):
            signs = signs_prime
            p = p2
    print(f"Residue of Hill Climbing Prepart: {get_residue(arr,signs)}")
    return signs

def T(iter):
    return 10**10 * 0.8**(int(iter/300))

def simulated_annealing_standard(arr,max_iter=10):
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
    print(f"Residue of final arr: {get_residue(arr,signs_pp)}")
    return signs_pp

def simulated_annealing_prepart(arr,max_iter=10):
    signs = get_random_signs()
    signs_pp=signs
    p = prepart_to_arr(arr, signs)
    p3 = prepart_to_arr(arr, signs_pp)
    for iter in range(max_iter):
        signs_prime = get_neighbor(signs)
        p2 = prepart_to_arr(arr, signs_prime)
        residue,residue_prime=karmarkar_karp(signs),karmarkar_karp(signs_prime)
        exp_prob = np.exp(-(residue_prime-residue)/T(iter))
        if residue_prime<residue or np.random.rand() < exp_prob:
            signs=signs_prime
            p=p2
        if residue<karmarkar_karp(p3):
            signs_pp=signs
            p3=p
    print(f"Residue of final arr: {get_residue(arr,signs_pp)}")
    return signs_pp

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
        if (get_residue(arr, S_prime) < get_residue(arr, S)):
            if DEBUG:
                print("updated S: ", S_prime)
                print("residue: ", get_residue(arr, S_prime))
            S = S_prime
    return S

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

def get_inputfile_from_command_line():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('text', action='store', type=str, help='The text to parse.')
    args = parser.parse_args()
    inputfile = args.text
    print(inputfile)

if __name__ == '__main__':
    args = sys.argv
    DEBUG, c, inputfile = int(args[1]), int(args[2]), args[3]

    inputfile = "test2.txt"
    arr = load_int_array(inputfile)

    arr = [np.random.randint(N) for _ in range(100)]

    karmarkar_karp(arr)

# Track num total updates, index of last update
#