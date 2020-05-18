# Tejas Mane

import numpy as np
import pylab as pl
import pandas as pd


# Reading from the dumps file and preparing the required pandas database
# Change path of dmp files if required

df_name_to_id = pd.read_table('names.dmp', delimiter='|',header=None)
df_name_to_id = df_name_to_id.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_name_to_id = df_name_to_id[[1,0]]
df_name_to_id.columns = ['name','taxID' ]

df_id_to_pid = pd.read_table('nodes.dmp', delimiter='|',header=None)
df_id_to_pid = df_id_to_pid.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df_id_to_pid = df_id_to_pid[[0,1]]
df_id_to_pid.columns = ['id', 'pid']


import networkx as nx

G = nx.DiGraph() 
G.add_nodes_from(np.arange(np.max(np.array(list(df_name_to_id.iloc[:,1])))) +1)

G.add_edges_from([(int(df_id_to_pid.iloc[i,1]), int(df_id_to_pid.iloc[i,0])) for i in range(1, len(list(df_id_to_pid.iloc[:,1])))])

def find_lowest_common_ancestor(name1, name2, G):
    
    
    df1 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name1]['taxID'])]
    df2 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name2]['taxID'])]
    node1_id = int(df1['id'])
    node2_id = int(df2['id'])

    T = nx.algorithms.lowest_common_ancestors.tree_all_pairs_lowest_common_ancestor(G, root=1, pairs=[(node1_id, node2_id)])

    for (pair,solutionID) in T:

        try:

            if solutionID ==pair[0]:
                solutionID = [i for i in G.predecessors(pair[0])][0]

            if solutionID ==pair[1]:
                solutionID = [i for i in G.predecessors(pair[1])][0]


        except:
            print("")

        break


    ancestor = list(df_name_to_id[df_name_to_id['taxID'] ==solutionID]['name'])
    
    return solutionID, ancestor


## Test Case 1


# child to parent to parent
# 323097 -> 912 -> 911
# 913-> 911

node1 = 'Nitrobacter hamburgensis X14'
node2 = 'ATCC 25391'


pid, ancestor = find_lowest_common_ancestor(node1, node2, G)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 2

# 1->1
# 323097 -> ... -> 1
node1 = 'root'
node2 = 'Nitrobacter hamburgensis X14'


pid, ancestor = find_lowest_common_ancestor(node1, node2, G)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 3

# 65-> 64->189773 -> 189772 -> 32061
# 2720502 -> 189773

node1 = 'ATCC 23779'
node2 = 'unclassified Herpetosiphonaceae'


pid, ancestor = find_lowest_common_ancestor(node1, node2, G)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)



## Test Case 4

# 65-> 64 -> 189773
# 64->189773


node1 = 'ATCC 23779'
node2 = 'Herpetosiphon'


pid, ancestor = find_lowest_common_ancestor(node1, node2, G)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)
