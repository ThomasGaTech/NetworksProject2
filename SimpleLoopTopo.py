# Simple Single Loop Topology:
# 1 --- 2
# |     |
# |     |
# 3 --- 4

topo = { 1 : [3, 2], 
         3 : [1, 4],
         2 : [1, 4], 
         4 : [3, 2] }
