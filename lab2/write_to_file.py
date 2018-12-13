import sys
if len(sys.argv) != 3:
    print(" Usage is : %s file_to_open num_lines_to_write" % (sys.argv[0]))
    sys.exit()

fd = open(sys.argv[1], 'w')
lines2write = int(sys.argv[2])
for i in range(lines2write):
    print(" Enter a line of data for the file ")
    print(" each line should be two words followed by a floating point number ")
    line = input()
    words = line.split()
    fd.write('%s %s %f %8.2f\n' %
             (words[0], words[1], float(words[2]), float(words[2])))
fd . close()
