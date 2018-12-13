import sys
import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    print(" Usage is : %s file_to_write " % (sys.argv[0]))
    sys . exit()

fd = open(sys.argv[1], 'wb')

# Declare , initialize , and output a byte array
# myData = np.zeros(256, np.uint8)

# for i in range(256):
#     myData[i] = i

# myData.tofile(fd, " ")

myCuint = np.zeros(1, np.uint32)
myCuint[0] = 82 * 45
myCuint.tofile(fd)
print(myCuint)

myCdouble = np.zeros(1, np.float64)
myCdouble[0] = 25.87 / 34.76
myCdouble.tofile(fd)
print(myCdouble)
