import argparse
import numpy as np
# ./kk inputfile

# where you may assume inputfile is a list of 100 (unsorted) integers, one per line, and the
# desired output is the residue obtained by running Karmarkar-Karp with these 100 numbers
# as input

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

def get_inputfile_from_command_line():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('text', action='store', type=str, help='The text to parse.')
    args = parser.parse_args()
    inputfile = args.text
    print(inputfile)

if __name__ == '__main__':

    inputfile = "test2.txt"
    arr = load_int_array(inputfile)

    arr = [np.random.randint(100) for _ in range(50)]

    karmarkar_karp(arr)