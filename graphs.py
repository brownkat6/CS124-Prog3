"""
Graph Specs:

ideas:
avg residue (over 50 instances) / algorithm type
residue spread (over 50 instances) / algorithm type
--> size of smaller partition / algorithm type
avg number iterations before convergence & avg number updates / algorithm type (excluding kk)

input:
residue_lst (len 50)
# updates (len 50)
last update index (len 50)

json structure:
{
'residue' : {alg : alg_residues = []}
'updates' : {alg : alg_updates = []}
'indices' : {alg : alg_indices = []}
}"""

#thank you https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/

import numpy as np
import matplotlib.pyplot as plt
import json

#Data (thanks https://www.geeksforgeeks.org/read-json-file-using-python/)
f = open('tests_data.json')
data = json.load(f)
residues = data["residues"]
updates = data["updates"]
indices = data["indices"]
f.close()

# Calculate the average
means = {}
for k in residues:
    means[k] = np.mean(residues[k])

# Calculate the standard deviation
stds = {}
for k in residues:
    stds[k] = np.std(residues[k])

# Define labels, positions, bar heights and error bar heights
labels = [k for k in residues.keys()]
x_pos = np.arange(len(labels))
print(x_pos)
CTEs = [means[lab] for lab in labels]
error = [stds[lab] for lab in labels]

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       color='red',
       ecolor='black',
       capsize=10)
ax.set_ylabel('Mean Residue (Over 50 Cases)')
ax.set_xticks(x_pos)
plt.xticks(rotation = 45)
ax.set_xticklabels(labels)
ax.set_title('Number Partition Heuristics')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('number_partition_heuristics_residue.png')
plt.show()

#plt.pause(0.01)
#wait = input("Enter to continue...")

#thank you https://matplotlib.org/3.5.0/gallery/lines_bars_and_markers/categorical_variables.html

data = {}
data2 = {}
for k in updates:
    data[k] = np.mean(updates[k])
    data2[k] = np.mean(indices[k])

names = list(data.keys())
values1 = list(data.values())
values2 = list(data2.values())

plt.scatter(names, values1)
plt.tick_params(labelrotation=45)
plt.title('Number Updates')
plt.savefig('number_partition_num_updates.png')
plt.show()

plt.tick_params(labelrotation=45)
plt.title('Final Update Index')
plt.scatter(names, values2)
#fig.suptitle('Number Partition Heuristics')
plt.savefig('number_partition_last_index_update.png')
plt.show()
