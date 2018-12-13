import numpy as np
import bmp_io_c
from numpy.linalg import inv
import math

# define image size
rows = 512
cols = 512
planes = 3

# create a black image
black_image = np.zeros([3, rows, cols], np.uint8)
bmp_io_c.output_bmp_c("my_image.bmp", black_image)


# insert a red square
def insert_red_sq(image):
    for i in range(255 - 64, 255 + 64):
        for j in range(255 - 64, 255 + 64):
            image[0, i, j] = 255

    return image


image_with_red = insert_red_sq(black_image)
bmp_io_c.output_bmp_c("my_image_red.bmp", image_with_red)

black_image_original = np.zeros([3, rows, cols], np.uint8)

# convert from PICS to CICS and vice versa by + 255 and -255
def change_to_CISC_PICS(image, type):
    pic = np.zeros([3, 512, 512], np.uint8)
    if type == "to_cics":
        for i in range(rows):
            for j in range(cols):
                pic[0, i, j] = image[0, i - 255, j - 255]
    else:
        for i in range(rows):
            for j in range(cols):
                pic[0, i-255, j-255] = image[0, i, j]

    return pic


black_cics = change_to_CISC_PICS(image_with_red, "to_cics")
bmp_io_c.output_bmp_c("PICS_image.bmp", black_cics)


# bi-linear interpolation
def lininterp(x, y, black_cics):
    x1 = math.floor(x)
    x2 = math.ceil(x)
    y1 = math.floor(y)
    y2 = math.ceil(y)

    my_mat = np.array(
        [[1, x1, y1, (x1*y1)], [1, x1, y2, (x1*y2)],
         [1, x2, y1, (x2*y1)], [1, x2, y2, (x2*y2)]])

    multi_mat = np.array([[1, x, y, (x*y)]]).reshape(4, 1)

    invmymat = np.linalg.inv(my_mat).T
    final_coord = np.dot(invmymat, multi_mat)

    if x1 > 511:
        x1 = 511

    if x2 > 511:
        x2 = 511

    if y1 > 511:
        y1 = 511

    if y2 > 511:
        y2 = 511

    final_value = final_coord[0] * black_cics[0, x1, y2] + final_coord[1] * black_cics[0, x1,
                                                                                       y2] + final_coord[2] * black_cics[0, x2, y1] + final_coord[3] * black_cics[0, x2, y2]

    return final_value


# fill in the formula and plug in the 6 values and generate the 6 images
def transformer_formula(black_cics, black_image_original, theta1, theta2, lambda1, lambda2, tx, ty):

    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)

    S = np.array([[lambda1, 0], [0, lambda2]])

    R1 = np.array([[np.cos(theta1), np.sin(-theta1)],
                   [np.sin(theta1), np.cos(theta1)]])

    R2 = np.array([[np.cos(theta2), np.sin(-theta2)],
                   [np.sin(theta2), np.cos(theta2)]])

    A = np.dot(np.dot(R2, S), R1)
    # print("this is A", A)

    ainv = np.linalg.inv(A)
    tytx = np.array([[tx],[ty]])

    for i in range(-255, 255):
        for j in range(-255, 255):
            imageArray = np.array([[i], [j]])

            final_points = np.dot(ainv, (imageArray - tytx))
            # print("image array", imageArray)
            # print("tytx", tytx)
            # print(final_points)

            if math.ceil(final_points[0]) != math.floor(final_points[0]) and \
                    math.ceil(final_points[1]) != math.floor(final_points[1]):
                black_image_original[0, i, j] = lininterp(
                    final_points[0], final_points[1], black_cics)
            else:
                black_image_original[0, i, j] = black_cics[0,
                                                  final_points[0].astype(int), final_points[1].astype(int)]

    return black_image_original


# transforming the image with given values
img1 = transformer_formula(black_cics, black_image_original, 45, 0, 1, 1, 0, 0)
bmp_io_c.output_bmp_c("image_test1.bmp", change_to_CISC_PICS(img1, "to_pics"))

img2 = transformer_formula(black_cics, black_image_original, 30, 0, 2, 1, 0, 0)
bmp_io_c.output_bmp_c("image_test2.bmp", change_to_CISC_PICS(img2, "to_pics"))

img3 = transformer_formula(black_cics, black_image_original,30,0,1,2,0,0)
bmp_io_c.output_bmp_c("image_test3.bmp", change_to_CISC_PICS(img3, "to_pics"))

img4 = transformer_formula(black_cics, black_image_original, 30,15,2,1, 0, 0)
bmp_io_c.output_bmp_c("image_test4.bmp", change_to_CISC_PICS(img4, "to_pics"))

img5 = transformer_formula(black_cics, black_image_original, 50, 25, 2, 0.5, 0, 0)
bmp_io_c.output_bmp_c("image_test5.bmp", change_to_CISC_PICS(img5, "to_pics"))

img6 = transformer_formula(black_cics, black_image_original, 50, 25, 2, 0.5, 80, -70)
bmp_io_c.output_bmp_c("image_test6.bmp", change_to_CISC_PICS(img5, "to_pics"))