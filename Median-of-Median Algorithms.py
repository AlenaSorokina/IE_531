# -*- coding: utf-8 -*-
"""Deterministic Select.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qMF79tAyusxF4fEDRytACgA9aNpjMCXf
"""

import sys
import argparse
import random
import numpy as np 
import time
import math
import pandas as pd
sys.setrecursionlimit(3000)

# sort the array and pick the k-th smallest element from the sorted-array
def sort_and_select(current_array, k) :
    # sort the array
    sorted_current_array = np.sort(current_array)
    return sorted_current_array[k]

def deterministic_select(current_array, k, m) :
    
    if (len(current_array) <= m) :
        # just use any method to pick the k-th smallest element in the array
        # I am using the sort-and-select method here
        return sort_and_select(current_array, k)
    else : 
        # I need this array to compute the median-of-medians...
        medians_of_smaller_arrays_of_size_m = []
        
        for i in range(0,len(current_array),m):
            smaller_array_of_size_m = []
            smaller_array_of_size_m.extend(current_array[i:i+m])
            
            if (len(smaller_array_of_size_m) == 1) :
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m,0,m)])
            elif (len(smaller_array_of_size_m)%2 == 1) :
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m, int((len(smaller_array_of_size_m) +1)/2), m)])
            else: 
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m, int(len(smaller_array_of_size_m)/2), m)])
            
        # compute the meadian of the medians_of_smaller_arrays_of_size_five array by recursion
        p = deterministic_select(medians_of_smaller_arrays_of_size_m, int(len(medians_of_smaller_arrays_of_size_m)/2), m)
        
        # split the current_array into three sub-arrays: Less_than_p, Equal_to_p and Greater_than_p
        Less_than_p = []
        Equal_to_p = []
        Greater_than_p = []
        for x in current_array : 
            if (x < p) : 
                Less_than_p.extend([x])
            if (x == p) : 
                Equal_to_p.extend([x])
            if (x > p) : 
                Greater_than_p.extend([x])
                
        if (k < len(Less_than_p)) :
            return deterministic_select(Less_than_p, k, m)
        elif (k >= len(Less_than_p) + len(Equal_to_p)) : 
            return deterministic_select(Greater_than_p, k - len(Less_than_p) - len(Equal_to_p), m)
        else :
            return p

df_ = pd.DataFrame(index=[i for i in range(1000,10000,1000)], columns=[5, 7, 9, 11, 13])
df_ = df_.fillna(0)
t = []
for n in range(1000,10000,1000):
  for m in [5, 7, 9, 11, 13] :
    t = []
    for i in range(100):
      my_array = [random.randint(1,100*n) for _ in range(n)]
      k = int((n+1)/2)
      t0 = time.time()
      kth = deterministic_select(my_array, k, m)
      t1 = time.time()
      t.append(t1-t0)
    df_.loc[[n], [m]] = sum(t)/len(t)
    minValues = df_.min(axis=1)

df_ = df_.T
axes = df_.plot.line(figsize = (10,40), subplots = True)
print(minValues)
fig = axes[0].get_figure()
fig.savefig("myplot.pdf")
