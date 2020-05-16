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



def find_lowest_common_ancestor(name1, name2, df_name_to_id, df_id_to_pid):

    name1 = name1.strip()
    name2 = name2.strip()

    # Find the id to parent id row for corresponding nodes   
    df1 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name1]['taxID'])]
    df2 = df_id_to_pid[df_id_to_pid['id']==int(df_name_to_id.loc[df_name_to_id['name'] == name2]['taxID'])]


    solutionID = -1
    
    
    parents_node1 = [int(df1['pid'])]
    parents_node2 = [int(df2['pid'])]
    
    # Keep left joining child parent table with child parent on left_table.pid = right_table.cid
    # till a common parent has been found.
    
    while (True):
        
        # Finding common element in ancestor list. 
        solution_set = set(parents_node1).intersection(set(parents_node2))


        if len(solution_set) > 0:
            # found a common ancestor exit loop
            solutionID= solution_set.pop()
            break

        else:
            # no common ancestor yet, keep joining tables

            df1 = df1.merge(df_id_to_pid, left_on=['pid'], right_on=['id'], how='left').iloc[:, [0,3]]
            df1.columns = ['id', 'pid']

            df2 = df2.merge(df_id_to_pid, left_on=['pid'], right_on=['id'], how='left').iloc[:, [0,3]]
            df2.columns = ['id', 'pid']
            
            parents_node1.append(int(df1['pid']))
            parents_node2.append(int(df2['pid']))

            

    final_list = list(df_name_to_id[df_name_to_id['taxID'] ==solutionID]['name'])

    # Returning the tax id of lowest common ancestors and the possible names for that tax id.

    return solutionID, final_list



## Test Case 1


# child to parent to parent
# 323097 -> 912 -> 911
# 913-> 911

node1 = 'Nitrobacter hamburgensis X14'
node2 = 'ATCC 25391'


pid, ancestor = find_lowest_common_ancestor(node1, node2, df_name_to_id, df_id_to_pid)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 2

# 1->1
# 323097 -> ... -> 1
node1 = 'root'
node2 = 'Nitrobacter hamburgensis X14'


pid, ancestor = find_lowest_common_ancestor(node1, node2, df_name_to_id, df_id_to_pid)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)


## Test Case 3

# 65-> 64->189773 -> 189772 -> 32061
# 2720502 -> 189773

node1 = 'ATCC 23779'
node2 = 'unclassified Herpetosiphonaceae'


pid, ancestor = find_lowest_common_ancestor(node1, node2, df_name_to_id, df_id_to_pid)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)



## Test Case 4

# 65-> 64 -> 189773
# 64->189773


node1 = 'ATCC 23779'
node2 = 'Herpetosiphon'


pid, ancestor = find_lowest_common_ancestor(node1, node2, df_name_to_id, df_id_to_pid)
print("Lowest common ancestor of node1 =", node1, " and node2 = ", node2      , " is a node with taxid = ", pid, "and the corresponding names can be = ", ancestor)




