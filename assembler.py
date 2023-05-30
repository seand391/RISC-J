import sys
assemblyFileName = "./"
binaryFileName = "./"
assemblyFileName += sys.argv[1]
binaryFileName += sys.argv[2]
assemblyFile = open(assemblyFileName, 'r')
binaryFile = open(binaryFileName, 'w')
for line in assemblyFile.readlines():
    binStr = '00000000000000000000000000000000'
    tokens = line.strip().replace(',', '').split()
    tokens[0] = tokens[0].lower()
    if tokens[0] in ["add", "sub", "mul", "div", "mod", "xor", "or", "and", "sll", "srl"]:
        print("R-Format")
        fun = str(bin(["add", "sub", "mul", "div", "mod", "xor",
                  "or", "and", "sll", "srl"].index(tokens[0]))[2:].zfill(4))
        opcode = '0000'
        rd = str(bin(int(tokens[1][1:]))[2:].zfill(5))
        r1 = str(bin(int(tokens[2][1:]))[2:].zfill(5))
        r2 = str(bin(int(tokens[3][1:]))[2:].zfill(5))
        noop = '000000000'
        binStr = noop + r2 + r1 + fun + rd + opcode
        binaryFile.write(binStr + '\n')
    elif tokens[0] in ["addi", "xori", "ori", "andi", "slli", "srli"]:
        print("I-Format")
        fun = str(bin(["addi", "xori", "ori", "andi", "slli",
                  "srli"].index(tokens[0]))[2:].zfill(4))
        opcode = '0001'
        rd = str(bin(int(tokens[1][1:]))[2:].zfill(5))
        r1 = str(bin(int(tokens[2][1:]))[2:].zfill(5))
        imm = str(bin(int(tokens[3]))[2:].zfill(14))
        binStr = imm + r1 + fun + rd + opcode
        binaryFile.write(binStr + '\n')
    elif tokens[0] in ["sb", "sh", "sw", "lb", "lh", "lw"]:
        print("S-Format")
        fun = str(bin(["sb", "sh", "sw", "lb", "lh",
                  "lw"].index(tokens[0]))[2:].zfill(4))
        opcode = '0011'
        r1 = str(bin(int(tokens[1][1:]))[2:].zfill(5))
        r2 = str(bin(int(tokens[2][1:]))[2:].zfill(5))
        imm = str(bin(int(tokens[3]))[2:].zfill(14))
        binStr = imm + r2 + r1 + fun + opcode
        binaryFile.write(binStr + '\n')
    elif tokens[0] in ["beq", "bne", "blt", "bge"]:
        print("C-Format")
        fun = str(
            bin(["beq", "bne", "blt", "bge"].index(tokens[0]))[2:].zfill(4))
        opcode = '0100'
        r1 = str(bin(int(tokens[1][1:]))[2:].zfill(5))
        r2 = str(bin(int(tokens[2][1:]))[2:].zfill(5))
        sign = '0'
        if int(tokens[3]) < 0:
            sign = '1'
            tokens[3] = str(int(tokens[3]) * -1)
        imm = str(bin(int(tokens[3]))[2:].zfill(13))
        binStr = sign + imm + r2 + r1 + fun + opcode
        binaryFile.write(binStr + '\n')
    elif tokens[0] in ["jal", "jalr"]:
        print("J-Format")
        fun = str(
            bin(["jal", "jalr"].index(tokens[0]))[2:])
        opcode = '0101'
        rd = str(bin(int(tokens[1][1:]))[2:].zfill(5))
        sign = '0'
        if int(tokens[2]) < 0:
            sign = '1'
            tokens[2] = str(int(tokens[2]) * -1)
        imm = str(bin(int(tokens[2]))[2:].zfill(21))
        binStr = sign + imm + rd + fun + opcode
        binaryFile.write(binStr + '\n')
    elif tokens[0] == "#":
        print("comment")
    else:
        print("Unable to recognize instruction: ", tokens[0])

assemblyFile.close()
binaryFile.close()
