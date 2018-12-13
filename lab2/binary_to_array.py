import sys
import numpy as np

if len(sys.argv) != 2:
    print("Usage is: %s file_to_read" % (sys.argv[0]))
    sys.exit()

fd = open(sys.argv[1], 'rb')

myData = np.fromfile(fd, np.uint8, 256)

for i in range(256):
    if myData[i] != i:
        print("Error occured on uint8 value %d" % (i))

myCuint = np.fromfile(fd, np.uint32, 1)
print("this is myCuint", myCuint)

if myCuint[0] != 82 * 35:
    print("Opps an error occured on the uint32")

mycDouble = np.fromfile(fd, np.float64, 1)
print("this is mycDouble", mycDouble)

if mycDouble[0] != 25.87 / 34.76:
    print("oooops, an error occured in float64")

fd.close()
