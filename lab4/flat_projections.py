import numpy as np
import bmp_io_c
import math
from numpy.linalg import inv

# read the sample image
rows, cols, pixels = bmp_io_c.input_bmp_c("image_test02.bmp")
print(rows, cols)
print(pixels)

def lininterp (lions_image, x, y):

    if x < 0 or x > (cols - 1):
        return 0, 0, 0

    if y < 0 or y > (rows - 1):
        return 0, 0, 0

    x1 = math.floor(x)
    x2 = math.ceil(x)
    y1 = math.floor(y)
    y2 = math.ceil(y)

    
    if x1 == x2 or y1 == y2:
        return lions_image[0, y1, x1]

    mat = np.asarray([[1, x1, y1, x1*y1], [1, x1, y2, x1*y2], [1, x2, y1, x2*y1], [1, x2, y2, x2*y2]])

    mat = np.transpose(np.linalg.inv(mat))

    coordinates = np.dot(mat, np.asarray([[1], [x], [y], [x * y]]))

    R = (float(coordinates[0]) * lions_image[0, y1, x1]) + (float(coordinates[1]) * lions_image[0, y1, x2]) \
    + (float(coordinates[2]) * lions_image[0, y2, x1]) + (float(coordinates[3]) * lions_image[0,y2, x2])

    G = (float(coordinates[0]) * lions_image[1, y1, x1]) + (float(coordinates[1]) * lions_image[1, y1, x2]) \
    + (float(coordinates[2]) * lions_image[1, y2, x1]) + (float(coordinates[3]) * lions_image[1, y2, x2])

    B = (float(coordinates[0]) * lions_image[2, y1, x1]) + (float(coordinates[1]) * lions_image[2, y1, x2]) \
    + (float(coordinates[2]) * lions_image[2, y2, x1]) + (float(coordinates[3]) * lions_image[2, y2, x2])

    return R, G, B

# convert from CICS to PICS 
def cicsToPics(x,y,r,c):
    return (x + (math.floor(c/2))), (y + math.floor((r/2)))

def compute_cone(d, rows, cols, lions_image, black_image):
    # theta = inv_of_tan(c/2d) and phi = inv_of_tan(R/2d)

    thetaM = np.arctan(cols/(2 * d))
    phiM = np.arctan(rows/(2 * d))

    deg_to_pix = 2048/180

    delta = np.pi/2048

    # Loop from -π/2 to π/2 in Longitude and -π/2 to π/2 in Latitude in increments of Δ.
    for i in np.arange((-np.pi/2), (np.pi/2), delta):
        for j in np.arange((-np.pi/2), (np.pi/2), delta):

            if abs(i) > thetaM:
                continue

            if abs(j) > phiM:
                continue

            # for the formulas we know x = r * cos phi * sin theta and y = r * sine phi and
            # z = r cos phi * cos theta and z = d so using the 3 d values given, lets compute r
            # Let z = d, the viewing distance compute r, then x, then y

            z = d
            r = z / (np.cos(j) * np.cos(i))
            x = r * np.cos(j) * np.sin(i)
            y = r * np.sin(j)

            print(r, x, y)
            # (x, y) are in CICS. Convert to PICS
            pics_x, pics_y = cicsToPics(x, y, rows, cols)

            r,g,b = lininterp(lions_image, pics_x, pics_y)

            theta_deg = np.rad2deg(i)
            phi_deg = np.rad2deg(j)

            imageCX = theta_deg * deg_to_pix
            imageCY = phi_deg * deg_to_pix

            # print(imageCX,imageCY)

            imagePX, imagePY = cicsToPics(imageCX, imageCY, 2048, 2048)

            black_image[0, int(imagePY), int(imagePX)] = r
            black_image[1, int(imagePY), int(imagePX)] = g
            black_image[2, int(imagePY), int(imagePX)] = b
            
if cols > rows:
    d = cols
else:
    d = rows


dist_1 = 0.5 * d
dist_2 = 1.0 * d
dist_3 = 1.5 * d 

myimage11 = np.zeros([3, 2048, 2048], np.uint8)
compute_cone(dist_1, rows, cols, pixels, myimage11)
bmp_io_c.output_bmp_c("myimage0.5.bmp", myimage11)

myimage22 = np.zeros([3, 2048, 2048], np.uint8)
compute_cone(dist_2, rows, cols, pixels, myimage22)
bmp_io_c.output_bmp_c("myimage1.0.bmp", myimage22)

myimage33 = np.zeros([3, 2048, 2048], np.uint8)
compute_cone(dist_3, rows, cols, pixels, myimage33)
bmp_io_c.output_bmp_c("myimage1.5.bmp", myimage33)