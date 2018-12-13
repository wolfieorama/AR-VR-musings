import numpy as np
import bmp_io_c
import math
from numpy.linalg import inv

Ry = np.array([[np.cos(30),0,np.sin(30)], [0, 1, 0], [-np.sin(30), 0, np.cos(30)]])
Rx = np.array([[1,0,0], [0, np.cos(10), -np.sin(10)], [0, np.sin(10), np.cos(10)]])
Rz = np.array([[np.cos(-15),-np.sin(-15),0], [np.sin(-15), np.cos(-15), 0], [0, 0,1]])

# print(Rx)
# print(Ry)
# print(Rz)


composite = np.matmul(Ry, np.matmul(Rx, Rz))

print(composite)

print("=====================================================")

a = np.array([1,0,0])
for001 = np.matmul(composite, a)

print(for001)

print("=====================================================")

b = np.array([0,1,0])
for010 = np.matmul(composite, b)

print(for010)

print("=====================================================")

c = np.array([0,0,1])
for001 = np.matmul(composite, c)

print(for001)

print("=====================================================")

bodypoint = np.array([2.2, 3.8, -4.2])
forbdp = np.matmul(composite, bodypoint)

print(forbdp)

print("=====================================================")

invcom = np.linalg.inv(composite)

realw = np.matmul(invcom, bodypoint)

print(realw)

