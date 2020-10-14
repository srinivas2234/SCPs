"""The main program that runs gSpan."""
# -*- coding=utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

from .config import parser
from .gspan import gSpan
from .gspan import flat_trans
import codecs
import collections
import copy
import itertools
import time
global min_sup
graph_cnt=0
mins=sys.argv[2]

# print(min_no_vertices)
def read_graphs(FLAGS=None):
    global graph_cnt
    if FLAGS is None:
        FLAGS, _ = parser.parse_known_args(args=sys.argv[1:])

    database_file_name=FLAGS.database_file_name
    with codecs.open(database_file_name, 'r', 'utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        for i, line in enumerate(lines):
            cols = line.split(' ')
            if cols[0] == 't':
                graph_cnt += 1
    return graph_cnt

def main(FLAGS=None):
    """Run gSpan."""
    graph_cnt=read_graphs()

    min_sup=int(graph_cnt)*float(mins)

    if FLAGS is None:
        FLAGS, _ = parser.parse_known_args(args=sys.argv[1:])

    if not os.path.exists(FLAGS.database_file_name):
        print('{} does not exist.'.format(FLAGS.database_file_name))
        sys.exit()

    gs = gSpan(
        database_file_name=FLAGS.database_file_name,
        min_support=int(min_sup),
        min_num_vertices=FLAGS.lower_bound_of_num_vertices,
        max_num_vertices=FLAGS.upper_bound_of_num_vertices,
        max_ngraphs=FLAGS.num_graphs,
        is_undirected=(not FLAGS.directed),
        verbose=FLAGS.verbose,
        visualize=FLAGS.plot,
        where=FLAGS.where
    )
    graph_cnt=read_graphs()
    gs.run()
    from .gspan import arr
    # print(arr)
    gs.time_stats()
    from .gspan import total_time
    # print(flat_trans)
    min_sup=sys.argv[2]
    s=sys.argv[3]
    s=s.split('/')
    
    s=s[2].split('.')
    s=s[0]
    p=sorted(flat_trans)
    # print("aa",graph_cnt)
    sum_all=0
    for i in range(graph_cnt):
        sum_all =sum_all+len(flat_trans[i])
    # print(sum_all/graph_cnt)
    avg=sum_all/graph_cnt
    fg=open(str(min_sup)+"_"+str(s)+"_stats.txt",'a+')
    fg.write("minsup : " )
    fg.write(str(min_sup))
    fg.write("\n")
    fg.write("no_of_subgraphs : ")
    fg.write(str(arr))
    fg.write("\n")
    fg.write("total execution time : ")
    fg.write(str(total_time))
    fg.write("\n")
    fg.write("Avg number of transactions : ")
    fg.write(str(avg))
    fg.write("\n")
    fg.write("\n")
    fg.close()

    # print(flat_trans)

    # for i in range(0,graph_cnt):
    #     # print(len(flat_trans[i]))
    #     if(len(flat_trans[i])==0):
    #         flat_trans[i].append(-1)
        # print(i,flat_trans[i])
    f=open(str(min_sup)+"_"+str(s)+" flat_trans.txt",'w')
    for i in range(0,graph_cnt):
        # print(i,flat_trans[i])
        for j in flat_trans[i]:
            f.write(str(j))
            f.write(" ")
        f.write("\n")
    f.close()
    return gs
    

if __name__ == '__main__':
    main()
