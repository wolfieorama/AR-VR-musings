import numpy as np
import bmp_io_c
import math
from numpy.linalg import inv

# reading the left phone camera image
rows_left_image, cols_left_image, pixels_left_image = bmp_io_c.input_bmp_c("imageLeft.bmp")
print(rows_left_image, cols_left_image)
# print(pixels_left_image)

# reading the right phone camera image
rows_right_image, cols_right_image, pixels_right_image = bmp_io_c.input_bmp_c("imageRight.bmp")
print(rows_right_image, cols_right_image)
# print(pixels_right_image)

# creating a 4096 by 2048 black images
black_left = np.zeros([3, 2048, 4096], np.uint8)
bmp_io_c.output_bmp_c("black_left.bmp", black_left)

black_right = np.zeros([3, 2048, 4096], np.uint8)
bmp_io_c.output_bmp_c("black_right.bmp", black_left)

# padding the left and right images with the black frame
 
padded_left1 = np.pad(pixels_left_image[0], ((513, 513), (1367, 1366)), 'constant')
padded_left2 = np.pad(pixels_left_image[1], ((513, 513), (1367, 1366)), 'constant')
padded_left3 = np.pad(pixels_left_image[2], ((513, 513), (1367, 1366)), 'constant')

padded_left = np.array([padded_left1, padded_left2, padded_left3], np.uint8)
bmp_io_c.output_bmp_c("padded_left.bmp", padded_left)

padded_right1 = np.pad(pixels_right_image[0], ((513, 513), (1367, 1366)), 'constant')
padded_right2 = np.pad(pixels_right_image[1], ((513, 513), (1367, 1366)), 'constant')
padded_right3 = np.pad(pixels_right_image[2], ((513, 513), (1367, 1366)), 'constant')

padded_right = np.array([padded_right1, padded_right2, padded_right3], np.uint8)
bmp_io_c.output_bmp_c("padded_righ.bmp", padded_right)

#stacking the 2 images
stacked_image = np.concatenate((padded_left, padded_right), 1)
print(stacked_image.shape)
bmp_io_c.output_bmp_c("stackedImage.bmp", stacked_image)