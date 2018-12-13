import numpy as np
import bmp_io_c
import math

cols = 2048
rows = 1024
layers = 3

# create a black image
black_image = np.zeros([3, rows, cols], np.uint8)
bmp_io_c.output_bmp_c("my_image.bmp", black_image)

# convert longitudes to pixels
def get_x(width, lng):
    return int(round(math.fmod((width * (180.0 + lng) / 360.0), (1.5 * width))))

# insert red
def insert_red(image):
    for i in range(cols):
        x1 = get_x(cols, -135)
        x2 = get_x(cols, -45)
        for lat in range(x1, x2):
            image[0,:,lat] = 255

    return image

new_image = insert_red(black_image)
bmp_io_c.output_bmp_c("image1.bmp", new_image)

# insert green
def insert_green(image):
    for i in range(cols):
        x1 = get_x(cols, -45)
        x2 = get_x(cols, 45)
        for lat in range(x1, x2):
            image[1,:,lat] = 255

    return image

new_image2 = insert_green(new_image)
bmp_io_c.output_bmp_c("image2.bmp", new_image2)

# insert blue
def insert_blue(image):
    for i in range(cols):
        x1 = get_x(cols, 45)
        x2 = get_x(cols, 135)
        for lat in range(x1, x2):
            image[2,:,lat] = 255

    return image

new_image3 = insert_blue(new_image2)
bmp_io_c.output_bmp_c("image3.bmp", new_image3)

# insert yellow
def insert_yellow(image):
    for i in range(cols):
        x1 = get_x(cols, -180)
        x2 = get_x(cols, -135)
        for lat in range(x1, x2):
            image[1,:,lat] = 255
            image[0,:,lat] = 255

    return image

new_image4 = insert_yellow(new_image3)
bmp_io_c.output_bmp_c("image4.bmp", new_image4)

# insert yellow
def insert_yellow2(image):
    for i in range(cols):
        x1 = get_x(cols, 135)
        x2 = get_x(cols, 180)
        for lat in range(x1, x2):
            image[1,:,lat] = 255
            image[0,:,lat] = 255

    return image

new_image5 = insert_yellow2(new_image4)
bmp_io_c.output_bmp_c("image5.bmp", new_image5)