import sys

outFile = open("D:\Classes\CS 535\Binary files\exchangeAssembly.txt", 'w')

arr = [87, 98, 83, 11, 27, 95, 23, 60, 92, 93, 57, 64, 73, 63, 66, 51, 7, 28, 81, 13, 10, 49, 47, 53, 9, 55, 3, 34, 99, 37, 46, 38, 76, 70, 67, 56, 16, 43, 35, 32, 18, 88, 25, 58, 82, 22, 4, 96, 26,
       97, 54, 14, 59, 29, 77, 61, 52, 100, 42, 20, 62, 33, 89, 94, 80, 48, 84, 39, 31, 65, 78, 75, 41, 72, 19, 21, 12, 71, 2, 5, 91, 17, 79, 8, 1, 15, 40, 85, 74, 30, 36, 50, 45, 44, 24, 6, 86, 90, 69, 68]

addr = 0
for elem in arr:
    outFile.write("addi r19, r0, " + str(elem) + " \n")
    outFile.write("sh r0, r19, " + str(addr) + " \n")
    addr += 1

# r0 = len(arr)
outFile.write("addi r19, r0, " + str(100) + " \n")

# r1 = 0
outFile.write("addi r20, r0, " + str(0) + " \n")

# r2 = r1
# Jump here each outer loop
outFile.write("addi r21, r20, " + str(0) + " \n")

# set current pair to compare
# r3 = arr[r1]
# Jump here each inner loop
outFile.write("lh r20, r22, " + str(0) + " \n")
# r4 = arr[r2]
outFile.write("lh r21, r23, " + str(0) + " \n")

# if first is NOT less than 2nd we skip the next few lines, otherwise swap them and store
# if r3 > r4:
outFile.write("blt r22, r23, " + str(2) + " \n")
# r5 = r3 (temp)
outFile.write("addi r24, r22, " + str(0) + " \n")
# r3 = r4
outFile.write("addi r22, r23, " + str(0) + " \n")
outFile.write("sh r20, r22, " + str(0) + " \n")
# r4 = r5
outFile.write("addi r23, r24, " + str(0) + " \n")
# Jump after here each if skip
outFile.write("sh r21, r23, " + str(0) + " \n")

# r2 = r2 + 1
outFile.write("addi r21, r21, " + str(1) + " \n")
# while r2 < r0:
outFile.write("blt r21, r19, " + str(-11) + " \n")  # inner loop
# r1 = r1 + 1
outFile.write("addi r20, r20, " + str(1) + " \n")
# while r1 < r0:
outFile.write("blt r20, r19, " + str(-14) + " \n")  # outer loop


outFile.write("addi r0, r0, " + str(0))  # no op
outFile.close()
