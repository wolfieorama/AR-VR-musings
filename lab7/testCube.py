import H_builders
import VRCube as VRCube
import bmp_io_c
import numpy as np
import csv
import sys


image1 = np.zeros((3, 10, 10), np.uint8)
image1[0] = 255

image2 = np.zeros((3, 10, 10), np.uint8)
image2[1] = 255

image3 = np.zeros((3, 10, 10), np.uint8)
image3[2] = 255

image4 = np.zeros((3, 10, 10), np.uint8)
image4[0] = 255
image4[1] = 255

image5 = np.zeros((3, 10, 10), np.uint8)
image5[1] = 255
image5[2] = 255

image6 = np.zeros((3, 10, 10), np.uint8)
image6[0] = 128
image6[2] = 128

bmp_io_c.output_bmp_c('image1.bmp', image1)
bmp_io_c.output_bmp_c('image2.bmp', image2)
bmp_io_c.output_bmp_c('image3.bmp', image3)
bmp_io_c.output_bmp_c('image4.bmp', image4)
bmp_io_c.output_bmp_c('image5.bmp', image5)
bmp_io_c.output_bmp_c('image6.bmp', image6)

p = VRCube([0, 0, 0], [0, 0, 0], ['image1.bmp', 'image2.bmp', 'image3.bmp', 'image4.bmp', 'image5.bmp', 'image6.bmp'], 1)
cord = p.get_cube()

# # Open files and create csv readers and writers
# fd_r = open("points_file.csv", 'r')
# fd_w = open("points_file.csv", 'w')
# datareader = csv.reader(fd_r, dialect='excel')
# datawriter = csv.writer(fd_w, dialect='excel')

fd = open("points_file.csv", 'w')
for i in range(len(cord)):
    fd. write('%s, %s, %s, %s, %s, %s, %s\n' % (cord[i][0], cord[i][1],  cord[i][2], cord[i][3], cord[i][4], cord[i][5], cord[i][6]))
fd.close()


