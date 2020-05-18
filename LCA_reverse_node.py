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


class ReverseNode:

    def __init__(self, value):
        self.data = value
        self.parent = None

NodeList = []

for i in range((np.max(np.array(df_name_to_id.iloc[:,1])))):
    NodeList.append(ReverseNode(i+1))

for i in range(len(list(df_id_to_pid.iloc[:,1]))):
    NodeList[int(df_id_to_pid.iloc[i,0])-1].parent = NodeList[int(df_id_to_pid.iloc[i,1])-1]

def find_lowest_common_ancestor(name1, name2, N):
    
    
    df1 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name1]['taxID'])]
    df2 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name2]['taxID'])]
    node1_id = int(df1['id'])
    node2_id = int(df2['id'])
    
    
    solutionID = -1
    
    
    parents_node1 = [NodeList[node1_id-1].parent.data]
    parents_node2 = [NodeList[node2_id-1].parent.data]
    
    N1 = NodeList[node1_id-1].parent
    N2 = NodeList[node2_id-1].parent
    
    
    
    while (True):

            # Finding common element in ancestor list. 
            solution_set = set(parents_node1).intersection(set(parents_node2))


            if len(solution_set) > 0:
                # found a common ancestor exit loop
                solutionID= solution_set.pop()
                break

            else:
                # no common ancestor yet, keep going to parent nodes
                
                N1 = N1.parent
                N2 = N2.parent
                parents_node1.append(N1.data)
                parents_node2.append(N2.data)

            

    final_list = list(df_name_to_id[df_name_to_id['taxID'] ==solutionID]['name'])

    # Returning the tax id of lowest common ancestors and the possible names for that tax id.

    return solutionID, final_list





## Test Case 1


# child to parent to parent
# 323097 -> 912 -> 911
# 913-> 911

node1 = 'Nitrobacter hamburgensis X14'
node2 = 'ATCC 25391'


pid, ancestor = find_lowest_common_ancestor(node1, node2, NodeList)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 2

# 1->1
# 323097 -> ... -> 1
node1 = 'root'
node2 = 'Nitrobacter hamburgensis X14'


pid, ancestor = find_lowest_common_ancestor(node1, node2, NodeList)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 3

# 65-> 64->189773 -> 189772 -> 32061
# 2720502 -> 189773

node1 = 'ATCC 23779'
node2 = 'unclassified Herpetosiphonaceae'


pid, ancestor = find_lowest_common_ancestor(node1, node2, NodeList)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)



## Test Case 4

# 65-> 64 -> 189773
# 64->189773


node1 = 'ATCC 23779'
node2 = 'Herpetosiphon'


pid, ancestor = find_lowest_common_ancestor(node1, node2, NodeList)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)
