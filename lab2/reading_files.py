print(" input the file name ")
filename = input()

print(" you entered the name ", filename)
fd = open(filename, 'r')
num_words = 0
first_words = []
for line in fd:
    words = line . split()
    num_words += len(words)
    first_words . append(words[0])
    print(num_words)
    print(first_words)

fd . close()
