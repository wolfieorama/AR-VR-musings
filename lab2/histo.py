import numpy as np
import matplotlib.pyplot as plt
import sys
import bmp_io_c

if len(sys.argv) != 3:
    print("the usage is: python this_file_name input_image plane_to_edit")
    sys.exit()

# input the image
print(str(sys.argv[1]))
rows, cols, pixels = bmp_io_c.input_bmp_c(str(sys.argv[1]))
print("Input Image dimensions are: ", rows, cols)
print("Pixels shape: ", pixels.shape)

# create an array of 256 different ,color intensities
plane = np.zeros((256), np.uint8)

# passing the plane to edit
if sys.argv[2] == 'R':
    currentPlane = pixels[0].astype(int).flatten()
elif sys.argv[2] == 'G':
    currentPlane = pixels[1].astype(int).flatten()
else:
    currentPlane = pixels[2].astype(int).flatten()

print("current plane shape", currentPlane.shape)

plane = np.bincount(currentPlane)
print("Sum============", sum(plane))

norm_plane = []
print(plane.dtype)

for i in range(256):
    x = plane[i] / sum(plane)
    norm_plane.append(x)

print("The Normalized plane sum is: ", sum(norm_plane))

# variance and Mean
print("The mean of the normalized plane", np.mean(norm_plane))
print("The variance  of the normalized plane", np.var(norm_plane))

# plotting
plt.plot(norm_plane, color='g')
plt.title("Normalized graph for color intesities")
plt.xlabel("Pixels Intensity")
plt.ylabel("Normalized values")
plt.show()
