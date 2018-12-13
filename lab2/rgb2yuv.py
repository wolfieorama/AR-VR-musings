import numpy as np
import sys
import bmp_io_c

if len(sys.argv) != 4:
    print("the usage is: python this_file_name input_image plane_to_edit output_file")
    sys.exit()

color_planes = 3
constant_matrix = np.array([[0.299, 0.587, 0.114],
                            [-0.147, - 0.289, 0.436],
                            [0.615, - 0.515, - 0.100]])
# input the image
print(str(sys.argv[1]))
rows, cols, pixels = bmp_io_c.input_bmp_c(str(sys.argv[1]))
print("Input Image dimensions are: ", rows, cols)

# np array to hold newly edited pic
yuv = np.zeros((color_planes, rows, cols), np.uint8)
print("shape is =========", constant_matrix.shape)

for i in range(rows):
    for j in range(cols):
        yuv[:, i, j] = np.dot(constant_matrix, np.array(
            pixels[:, i, j])) + np.array([0, 128, 128])


# printing the max and min in RGB
print("The max and min of R plane are: respectively",
      pixels[0].max(), pixels[0].min())
print("The max and min of G plane are: respectively",
      pixels[1].max(), pixels[1].min())
print("The max and min of B plane are: respectively",
      pixels[2].max(), pixels[2].min())

# printing the max and min in YUV
print("The max and min of y plane are: respectively",
      yuv[0].max(), yuv[0].min())
print("The max and min of u plane are: respectively",
      yuv[1].max(), yuv[1].min())
print("The max and min of v plane are: respectively",
      yuv[2].max(), yuv[2].min())


# converting to yuv depending on user plane selection
for i in range(rows):
    for j in range(cols):
        if str(sys.argv[2]) == 'y':
            yuv[1] = yuv[0]
            yuv[2] = yuv[0]
        elif str(sys.argv[2]) == 'u':
            yuv[0] = yuv[1]
            yuv[2] = yuv[1]
        else:
            yuv[0] = yuv[2]
            yuv[1] = yuv[2]

# output the image
bmp_io_c.output_bmp_c(str(sys.argv[3]), yuv)
