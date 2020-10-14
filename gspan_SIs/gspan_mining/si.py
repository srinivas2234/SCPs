
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import codecs
import collections
import copy
import itertools
import time


def read_si():

    with codecs.open('si.data', 'r', 'utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        si_count=0
        si_vert=collections.defaultdict(dict)
        si_degree=collections.defaultdict(list)
        si_ne=collections.defaultdict()
        no_of_edges=collections.Counter()
        for i, line in enumerate(lines):
            # si_degree=collections.defaultdict(list)
            cols=line.split(' ')
            # print(cols)
           
            if cols[0] == 't':
                if(si_count > 0):
                    si_ne[si_count] = si_degree.copy()
                    si_degree.clear()
                si_count += 1
            elif cols[-1] == '-1':
                break    
            elif cols[0] == 'v':
                si_vert[si_count][int(cols[1])]=int(cols[2])
            elif cols[0] == 'e':
                no_of_edges[si_count] += 1
                si_degree[int(cols[1])].append(si_vert[si_count][int(cols[2])])
                si_degree[int(cols[2])].append(si_vert[si_count][int(cols[1])])
  

    print(len(si_vert))
    print(si_vert[1])
    # print("no",no_of_edges)
    
read_si()



 # si_neighbor_degree1=collections.defaultdict()
        # si_degree1=[3,1,1,1]
        # si_neighbor_degree1[si_degree1[0]]=[1, 1, 1]
        # si_neighbor_degree1[si_degree1[1]]=[3]
        # si_neighbor_degree1[si_degree1[2]]=[3]
        # si_neighbor_degree1[si_degree1[3]]=[3]

        # flag=0
        # if(no_of_edges==3):
        #     k=0
        #     for i,j in deg:
        #         # print(i,k)
        #         # print(neighbor_degree[i],si_neighbor_degree1[si_degree1[k]])
        #         # print(degree[i],si_degree1[k])
        #         if(degree[i]==si_degree1[k] and neighbor_degree[i]==si_neighbor_degree1[si_degree1[k]]):
        #             # print("aa",flag)
        #             flag=flag+1
        #             k=k+1
        #         else:
        #             print("no star")
        #             break
        # if(flag==4):
        #     print("Yes star")
        # else:
        #     print("ammo")
        
# si_degree=[2,2,2]
#         # si_neighbor_degree=[[2 2]]
#         # print(sorted_vertices)
#         flag=0
#         if(no_of_edges==3):
#             for i in range(len(si_degree)):
#                 if(degree[i]==si_degree[i] and neighbor_degree[i] == [2, 2] ): 
#                     flag+=1
#                     i=i+1
#                 else:
#                     print("not traingle")
#                     break
#         if(flag==3):
#             print("yes traingle")
        
