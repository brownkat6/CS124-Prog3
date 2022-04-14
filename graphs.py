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
"""

{
'residue' : {alg : alg_residues = []}
'updates' : {alg : alg_updates = []}
'indices' : {alg : alg_indices = []}
}

#thank you https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/

import numpy as np
import matplotlib.pyplot as plt

#Data
residues = {'K-Karp':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Rep Rand':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Hill Climb':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Sim Anneal':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Prepart Rep Rand':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Prepart Hill Climb':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5], 'Prepart Sim Anneal':[6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5]}

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
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()