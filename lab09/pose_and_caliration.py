import numpy as np
import bmp_io_c
import math
from numpy.linalg import inv
from scipy import linalg as spl

# building a matrix
points = np.loadtxt("913.csv", delimiter=',')
print(len(points))

main_mat = []
ab_mat = []
for i in range(len(points)):
    x = points[i][0]
    y = points[i][1]
    z = points[i][2]
    a = points[i][3]
    b = points[i][4]

    mat1 = [x,y,z,1,0,0,0,0,(-a*x),(-a*y),(-a*z)]
    mat2 = [0,0,0,0,x,y,z,1,(-b*x),(-b*y),(-b*z)]

    main_mat.append(mat1)
    main_mat.append(mat2)

    ab_mat.append(a)
    ab_mat.append(b)

# print(np.array(main_mat))
# print(np.array(ab_mat))
main_mat = np.array(main_mat)
ab_mat = np.array(ab_mat)

pinv_of_main_mat = np.linalg.pinv(main_mat)
H_matrix = np.matmul(pinv_of_main_mat, ab_mat)

H_matrix2 = H_matrix.tolist()
H_matrix2.append(1)
H_matrix2 = np.array(H_matrix2)
H_matrix2 = H_matrix2.reshape(3,4)

print(H_matrix2)
A = H_matrix2[np.ix_([0,1,2],[0,1,2])]
C = H_matrix2[np.ix_([0,1,2],[3])]

print(C.shape)
print(A.shape)

R,Q = spl.rq(A)

K = np.copy(R)
R_compo = Q.T

print("----------------")
print(K)
print("----------------")
print(R_compo)

tb = np.matmul(-R_compo, np.matmul(np.linalg.inv(K),C))
print(tb)
