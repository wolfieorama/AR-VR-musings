#!/usr/bin/python
import sys
import numpy as np

#############################
# Output three arrays of uint8's as an RGB image
#############################

def output_bmp(filename, picdat_r, picdat_g, picdat_b):
  try:
    fd = open(filename, 'wb')
  except:
    print ("Unable to open output file: %s" % (filename))
    sys.exit( )
    
  # Use the shape to determine the number of rows and cols
  rows = picdat_r.shape[0]
  cols = picdat_r.shape[1]

  # Determine BMP scanLineWidth (round up to a multiple of 4)
  if cols % 4 == 0:
    scanlineWidth = 3*cols
  else:
    scanlineWidth = 3*cols + (4 - (3*cols)%4)

  # Define and output the BMP header
  bfType1 = np.zeros(1, np.uint8)
  bfType2 = np.zeros(1, np.uint8)
  bfSize = np.zeros(1, np.int32)
  bfReserved1 = np.zeros(1, np.uint16)
  bfReserved2 = np.zeros(1, np.uint16)
  bfOffBits = np.zeros(1, np.int32)
  biSize = np.zeros(1, np.uint32)
  biWidth = np.zeros(1, np.int32)
  biHeight = np.zeros(1, np.int32)
  biPlanes = np.zeros(1, np.uint16)
  biBitCount = np.zeros(1, np.uint16)
  biCompression = np.zeros(1, np.uint32)
  biSizeImage = np.zeros(1, np.uint32)
  biXPelsPerMeter = np.zeros(1, np.int32)
  biYPelsPerMeter = np.zeros(1, np.int32)
  biClrUsed = np.zeros(1, np.uint32)
  biClrImportant = np.zeros(1, np.uint32)

  bfType1[0] = 0x42      # The character 'B'
  bfType2[0] = 0x4D      # The character 'M'
  bfSize[0] = 54 + rows*scanlineWidth       
                         # Total image size
  bfReserved1[0] = 0     # Always 0
  bfReserved2[0] = 0     # Always 0
  bfOffBits[0] = 54      # Bytes from start of header to pic data
  biSize[0] = 40         # Size of bmfh structure, always 40
  biWidth[0] = cols      # Cols in image
  biHeight[0] = rows     # Rows in image
  biPlanes[0] = 1        # Always 1
  biBitCount[0] = 24     # Bits per pixel
  biCompression[0] = 0   # Compression type: "none"
  biSizeImage[0] = 0     # Size of image data in bytes
  biXPelsPerMeter[0] = 0 # Desired display dimensions in x direction ( 0 )
  biYPelsPerMeter[0] = 0 # Desired display dimensions in y direction ( 0 )
  biClrUsed[0] = 0       # Number of colors in color table, 0 for 24 bpp
  biClrImportant[0] = 0  # Application dependent, usually 0
    
  bfType1.tofile(fd)
  bfType2.tofile(fd)
  bfSize.tofile(fd)
  bfReserved1.tofile(fd)
  bfReserved2.tofile(fd)
  bfOffBits.tofile(fd)
  biSize.tofile(fd)
  biWidth.tofile(fd)
  biHeight.tofile(fd)
  biPlanes.tofile(fd)
  biBitCount.tofile(fd)
  biCompression.tofile(fd)
  biSizeImage.tofile(fd)
  biXPelsPerMeter.tofile(fd)
  biYPelsPerMeter.tofile(fd)
  biClrUsed.tofile(fd)
  biClrImportant.tofile(fd)

  # Define an array to hold one line's worth of BMP data, then use it
  # to convert from our row order to BMP row order and to output the pixels
  imageData = np.zeros(scanlineWidth, np.uint8)

  for i in range(rows-1, -1, -1):
    for j in range( int(cols) ):
      r = picdat_r[i, j]
      g = picdat_g[i, j]
      b = picdat_b[i, j]

      imageData[3*j]     = b
      imageData[3*j + 1] = g
      imageData[3*j + 2] = r
    imageData.tofile(fd)
    
  fd.close()

#############################
# Input an RGB BMP image and create 3 2-D arrays of uint8's
#############################

def input_bmp(filename):
  try:
    fd = open(filename, 'rb')
  except:
    print ("Unable to open input file: %s" % (filename))
    sys.exit( )
    
  # Read 28-bytes of the BMP file header and determine the number of rows, 
  # cols, and the offset to the pixel data
  hdr = bytearray( fd.read(28) )
  reverse_order = 0

  cols = hdr[18] + 256 * hdr[19] + 256**2 * hdr[20] + 256**3 * hdr[21]
  rows = hdr[22] + 256 * hdr[23] + 256**2 * hdr[24] + 256**3 * hdr[25]

  # Detect the order in which rows are stored in this bmp picture.  If
  # the order is reversed, a negative number is stored, i.e., a very large
  # unsigned int.  We subttract it from 2^32 to get the positive number
  # of rows
  if rows > 2**16:
    reverse_order = 1
    rows = 2**32 - rows

  offset = hdr[10] + 256 * hdr[11] + 256**2 * hdr[12] + 256**3 * hdr[13]

  # Declare the pixel arrays and determine the extra bytes needed
  # to get up to the scanline width (round up to a multiple of 4)
  pixels_r = np.zeros( (rows, cols), np.uint8)
  pixels_g = np.zeros( (rows, cols), np.uint8)
  pixels_b = np.zeros( (rows, cols), np.uint8)
  extra_bytes = (4-(3*cols)%4) % 4

  # Read the bmp header bytes up to the start of the raw pixel data
  fd.read(offset - 28)

  for i in range(rows):
    if reverse_order==1: store_row = i
    else: store_row = (rows - 1 - i)
    for j in range(cols):
      pixdat = bytearray(fd.read(3))
      pixels_b[store_row, j] = pixdat[0]
      pixels_g[store_row, j] = pixdat[1]
      pixels_r[store_row, j] = pixdat[2]
    fd.read(extra_bytes)

  fd.close()
  return rows, cols, pixels_r, pixels_g, pixels_b


#############################
# Input an RGB BMP image and create 1 3-D array of uint8's
#############################
def input_bmp_c(filename):
  try:
    fd = open(filename, 'rb')
  except:
    print ("Unable to open input file: %s" % (filename))
    sys.exit( )
    
  # Read 28-bytes of the BMP file header and determine the number of rows, 
  # cols, and the offset to the pixel data
  hdr = bytearray( fd.read(28) )
  reverse_order = 0

  cols = hdr[18] + 256 * hdr[19] + 256**2 * hdr[20] + 256**3 * hdr[21]
  rows = hdr[22] + 256 * hdr[23] + 256**2 * hdr[24] + 256**3 * hdr[25]

  # Detect the order in which rows are stored in this bmp picture.  If
  # the order is reversed, a negative number is stored, i.e., a very large
  # unsigned int.  We subttract it from 2^32 to get the positive number
  # of rows
  if rows > 2**16:
    reverse_order = 1
    rows = 2**32 - rows

  offset = hdr[10] + 256 * hdr[11] + 256**2 * hdr[12] + 256**3 * hdr[13]

  # Declare the pixel arrays and determine the extra bytes needed
  # to get up to the scanline width (round up to a multiple of 4)
  pixels = np.zeros( (3, rows, cols), np.uint8)
  extra_bytes = (4-(3*cols)%4) % 4

  # Read the bmp header bytes up to the start of the raw pixel data
  fd.read(offset - 28)

  for i in range(rows):
    if reverse_order==1: store_row = i
    else: store_row = (rows - 1 - i)
    for j in range(cols):
      pixdat = bytearray(fd.read(3))
      pixels[0, store_row, j] = pixdat[2]  # Red
      pixels[1, store_row, j] = pixdat[1]  # Green
      pixels[2, store_row, j] = pixdat[0]  # Blue
    fd.read(extra_bytes)

  fd.close()
  return rows, cols, pixels

#############################
# Output three arrays of uint8's as an RGB image
#############################

def output_bmp_c(filename, picdat) :
  try:
    fd = open(filename, 'wb')
  except:
    print ("Unable to open output file: %s" % (filename))
    sys.exit( )
    
  # Use the shape to determine the number of rows and cols
  rows = picdat.shape[1]
  cols = picdat.shape[2]

  # Determine BMP scanLineWidth (round up to a multiple of 4)
  if cols % 4 == 0:
    scanlineWidth = 3*cols
  else:
    scanlineWidth = 3*cols + (4 - (3*cols)%4)

  # Define and output the BMP header
  bfType1 = np.zeros(1, np.uint8)
  bfType2 = np.zeros(1, np.uint8)
  bfSize = np.zeros(1, np.int32)
  bfReserved1 = np.zeros(1, np.uint16)
  bfReserved2 = np.zeros(1, np.uint16)
  bfOffBits = np.zeros(1, np.int32)
  biSize = np.zeros(1, np.uint32)
  biWidth = np.zeros(1, np.int32)
  biHeight = np.zeros(1, np.int32)
  biPlanes = np.zeros(1, np.uint16)
  biBitCount = np.zeros(1, np.uint16)
  biCompression = np.zeros(1, np.uint32)
  biSizeImage = np.zeros(1, np.uint32)
  biXPelsPerMeter = np.zeros(1, np.int32)
  biYPelsPerMeter = np.zeros(1, np.int32)
  biClrUsed = np.zeros(1, np.uint32)
  biClrImportant = np.zeros(1, np.uint32)

  bfType1[0] = 0x42      # The character 'B'
  bfType2[0] = 0x4D      # The character 'M'
  bfSize[0] = 54 + rows*scanlineWidth       
                         # Total image size
  bfReserved1[0] = 0     # Always 0
  bfReserved2[0] = 0     # Always 0
  bfOffBits[0] = 54      # Bytes from start of header to pic data
  biSize[0] = 40         # Size of bmfh structure, always 40
  biWidth[0] = cols      # Cols in image
  biHeight[0] = rows     # Rows in image
  biPlanes[0] = 1        # Always 1
  biBitCount[0] = 24     # Bits per pixel
  biCompression[0] = 0   # Compression type: "none"
  biSizeImage[0] = 0     # Size of image data in bytes
  biXPelsPerMeter[0] = 0 # Desired display dimensions in x direction ( 0 )
  biYPelsPerMeter[0] = 0 # Desired display dimensions in y direction ( 0 )
  biClrUsed[0] = 0       # Number of colors in color table, 0 for 24 bpp
  biClrImportant[0] = 0  # Application dependent, usually 0
    
  bfType1.tofile(fd)
  bfType2.tofile(fd)
  bfSize.tofile(fd)
  bfReserved1.tofile(fd)
  bfReserved2.tofile(fd)
  bfOffBits.tofile(fd)
  biSize.tofile(fd)
  biWidth.tofile(fd)
  biHeight.tofile(fd)
  biPlanes.tofile(fd)
  biBitCount.tofile(fd)
  biCompression.tofile(fd)
  biSizeImage.tofile(fd)
  biXPelsPerMeter.tofile(fd)
  biYPelsPerMeter.tofile(fd)
  biClrUsed.tofile(fd)
  biClrImportant.tofile(fd)

  # Define an array to hold one line's worth of BMP data, then use it
  # to convert from our row order to BMP row order and to output the pixels
  imageData = np.zeros(scanlineWidth, np.uint8)

  for i in range(rows-1, -1, -1):
    for j in range( int(cols) ):
      r = picdat[0, i, j]
      g = picdat[1, i, j]
      b = picdat[2, i, j]

      imageData[3*j]     = b
      imageData[3*j + 1] = g
      imageData[3*j + 2] = r
    imageData.tofile(fd)
    
  fd.close()
