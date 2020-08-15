# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np 
from numpy import matrix
from numpy import linalg
from numpy.linalg import matrix_rank
import time
import math
import matplotlib.pyplot as plt
import cv2
import os

def frobenious_norm(input):
    A = np.matmul(input,input.T)
    norm = 0
    
    for i in range (0, A.shape[0]):
      for j in range(0, A.shape[1]):
        norm += A[i,j]*A[i,j]

    return math.sqrt(norm)

def matrix_sketch(input, e):
    length = math.ceil(2.0/e);

    B = np.zeros((input.shape[0], length))

    for i in range(1, input.shape[1]):
      for j in range(1, length):
        if (B[:, j].sum() == 0):
          B[:, j] = input[:, i]
          break;

      U, sigma, V = np.linalg.svd(B, full_matrices=False)
      delta = sigma[-1]*sigma[-1]

      I = np.identity(sigma.shape[0])
      sigma = np.sqrt(np.max((np.matmul(np.diag(sigma), np.diag(sigma).T) - delta*I), 0))

      B = np.matmul(U, np.diag(sigma))

    return B

num_of_rows = int(sys.argv[1])
num_of_col = int(sys.argv[2])
e = float(sys.argv[3])
input = sys.argv[4]
output = sys.argv[5]

print("Edo Liberty's Matrix Sketching Algorithm")
print("Original Data-Matrix has ", num_of_rows, "-rows & ", num_of_col, "-cols")
print("Epsilon = ", e, " (i.e. max. of ", 100*e, "% reduction of  Frobenius-Norm of the Sketch Matrix)")
print("Input File = ", input)

input = np.loadtxt(input)

input_frob_norm = frobenious_norm(input)
print("Frobenius Norm of the (", input.shape[0], " x ", input.shape[1], ") Data Matrix = ", input_frob_norm)
result = matrix_sketch(input, e);
res_frob_norm = frobenious_norm(result);
print("Frobenius Norm of the (", result.shape[0], " x ", result.shape[1], ") Sketch Matrix = ", res_frob_norm)
print("Change in Frobenius-Norm between Sketch & Original  = ", 100*(res_frob_norm - input_frob_norm)/input_frob_norm, "%")

np.savetxt(output,result,fmt='%.2f')

print("File `", output, "' contains a (", result.shape[0], " x ", result.shape[1], ") Matrix-Sketch")