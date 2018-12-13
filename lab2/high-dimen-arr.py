import numpy as np
import sys
import bmp_io_c

color_planes = 3
rows = 300
cols = 255

mypic = np.zeros((color_planes, rows, cols), np.uint8)
print(" color_planes = ", color_planes, " mypic.shape [0] = ",
      mypic . shape[0])
print(" rows = ", rows, " mypic.shape [1] = ", mypic.shape[1])
print(" cols = ", cols, " mypic.shape [2] = ", mypic.shape[2])
print(" mypic.shape = ", mypic.shape)

print(mypic)

# create an image form ramp by looping over 3 image planes

for k in range(color_planes):
    for i in range(rows):
        for j in range(cols):
            mypic[k, i, j] = j

print(mypic)

# output the image
bmp_io_c.output_bmp_c("ramp.bmp", mypic)
rows, columns, mypic1 = bmp_io_c.input_bmp_c("ramp.bmp")

# change one pixel
for k in range(color_planes):
    mypic[k, 100, 25] = 0

for k in range(color_planes):
    for i in range(rows):
        for j in range(cols):
            if mypic[k, i, j] != mypic[k, i, j]:
                print(
                    "pixel values differ at location [%d, %d, %d ]" % (k, i, j))

print(mypic)
