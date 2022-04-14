import random

n = 50
m = 100
r = 10**12 #confirmed random.random() w sufficient precision, docs: https://docs.python.org/3/library/random.html

for pre in range(1, n+1):
    with open("____"+str(pre)+".txt", 'w') as f:
        for x in range(0, m):
            f.write(str(random.randint(1,10**12)))
            f.write('\n')