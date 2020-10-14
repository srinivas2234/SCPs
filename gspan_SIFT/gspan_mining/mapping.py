
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import codecs
import collections
import copy
import itertools
import time
mapping=collections.defaultdict(dict)

def read_si():
    with codecs.open('mappingH.txt', 'r', 'utf-8') as f:
        global mapping
        lines = [line.strip() for line in f.readlines()]
        for i, line in enumerate(lines):
            cols=line.split(' ')    
            mapping[cols[1]]=cols[0]
            
    return mapping
read_si()
# print(mapping)
