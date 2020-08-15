# -*- coding: utf-8 -*-

import sys
import math
from collections import deque

import argparse

p = argparse.ArgumentParser()

p.add_argument('n', type=int)
p.add_argument('k', type=int)
args = p.parse_args()

# See https://www.geeksforgeeks.org/deque-in-python/ for details on Deques
Towers = deque()

# Global variable that keeps track of the number of steps in our solution 
number_of_steps = 0

# It is always a good idea to set a limit on the depth-of-the-recursion-tree in Python
sys.setrecursionlimit(3000)

def initialize(n, k) :
    for i in range(k) :
        X = deque()
        if (i == 0) :
            for j in range(n) :
                X.append(j+1)
        Towers.append(X)

def is_everything_legal() :
    result = True
    for i in range(args.k) :
        for j in range(len(Towers[i])) :
            for a in range(j,len(Towers[i])) :
                if (Towers[i][a] < Towers[i][j]) :
                    result = False
    return(result)

def move_top_disk(source, dest):
    global number_of_steps 
    number_of_steps = number_of_steps + 1
    x = Towers[source].popleft()
    Towers[dest].appendleft(x)
    if (True == is_everything_legal()) :
        y = " (Legal)"
    else :
        y = " (Illegal)"
    
    print ("Move disk " + str(x) + " from Peg " + str(source+1) + " to Peg " + str(dest+1) + y)

def move_using_three_pegs(number_of_disks, source, dest, intermediate) :
    if (1 == number_of_disks) :
        move_top_disk (source, dest)
    else :
        move_using_three_pegs (number_of_disks-1, source, intermediate, dest);
        move_top_disk(source, dest)
        move_using_three_pegs (number_of_disks-1, intermediate, dest, source)

def move(number_of_disks, source, dest, list_of_interm) :
    if (number_of_disks > 0):
      empty_inter = [x for x in list_of_interm if len(Towers[x]) ==0]

      if(len(empty_inter) < 2):
        move_using_three_pegs(number_of_disks, source, dest, empty_inter[-1])
      else:
        p = math.floor(number_of_disks/2)

        middle = empty_inter[-1]
        empty_inter.pop()
        empty_inter.append(dest)
        move(p, source, middle,empty_inter)

        empty_inter.pop()
        move(number_of_disks - p, source, dest, empty_inter)

        empty_inter.append(source)
        move(p, middle, dest, empty_inter)

def print_peg_state(m) :
    global number_of_steps
    print ("-----------------------------")
    print ("State of Peg " + str(m+1) + " (Top to Bottom): " + str(Towers[m]))
    print ("Number of Steps = " + str(number_of_steps))
    print ("-----------------------------")


initialize(args.n,args.k)
print_peg_state(0)
inter = [x for x in range(args.k)]; 
source = inter.pop(0); 
dest = inter.pop(-1)
move(args.n, source, dest, inter)
print_peg_state(args.k-1)