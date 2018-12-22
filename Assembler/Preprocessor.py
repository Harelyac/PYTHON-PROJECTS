import re
import sys
import os


def ConvertToBinary(value):
    binary_value = ""
    digits_count = 0
    new_value = int(value)
    while new_value > 0:
        binary_digit = new_value % 2
        new_value //= 2
        binary_value = str(binary_digit) + binary_value
        digits_count += 1

    binary_value = (15 - digits_count) * "0" + binary_value
    return binary_value


A_INSTRUCTION = "0"
C_INSTRUCTION = "1"
EQUAL_SIGN = "="
SEMI_COLON_SIGN = ";"

SymbolTable = {'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3',
               'R4': '4', 'R5': '5', 'R6': '6', 'R7': '7',
               'R8': '8', 'R9': '9', 'R10': '10', 'R11': '11',
               'R12': '12', 'R13': '13', 'R14': '14', 'R15': '15',
               'SCREEN': '16384', 'KBD': '24576', 'SP': '0',
               'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4'}

dest = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111",
        "#": "111"}

jump = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
        "?": "111"}

comp = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010",
        "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000",
        "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011",
        "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"}


def assemblingProcess():
    # First Pass
    object = sys.argv[1]
    my_path = os.path.abspath(os.path.dirname(__file__))
    new_object = os.path.join(my_path, object)
    if os.path.isdir(new_object):
        files_name = os.listdir(new_object)
        files = []
        for f in files_name:
            files.append(new_object + f)
    else:
        files = []
        files.append(os.path.abspath(object))
    for file_name in files:
        with open(file_name, "r") as AsmFile:
            Row = -1
            for command in AsmFile:
                if command != "\n" and command[0:2] != "//":
                    command = command.strip()
                if command == "":
                    continue
                if command[0] == "(":
                    label = command[1:-1]
                    SymbolTable[label] = Row + 1
                elif command[0] != " " and command[0] != "/" and command[0] != "\n":
                    Row += 1
                    # Second Pass
        with open(file_name, "r") as AsmFile:
            # new_file_name = file_name.split(".")[0] + ".hack"
            new_file_name = file_name.replace(".asm", ".hack")
            with open(new_file_name, "a") as HackFile:
                StartVarAddr = 16
                for command in AsmFile:
                    BinaryValue = ""
                    if command != "\n" and command[0:2] != "//":
                        command = command.strip()
                        command = re.split("\s*?\/+", command)
                        if command != "":
                            command = command[0]
                    if command == "":
                        continue
                    if command[0] == "@":
                        object = command[1:]
                        # if object is a symbol
                        if object in SymbolTable.keys():
                            value = SymbolTable[object]
                            BinaryValue = ConvertToBinary(value)
                            # Sending to file
                            # if object is an A instruction or new symbol
                        else:
                            # New symbol
                            if not object.isdigit():
                                SymbolTable[object] = StartVarAddr
                                BinaryValue = ConvertToBinary(StartVarAddr)
                                StartVarAddr += 1
                            else:
                                BinaryValue = ConvertToBinary(object)
                        final_value = A_INSTRUCTION + str(BinaryValue)
                        HackFile.write(final_value + "\n")
                        # If we deal with a C instruction/Command.
                    elif command[0] != "/" and command[0] != "\n" and command[0] != "(":
                        if EQUAL_SIGN in command:
                            key3 = "null"
                            key1 = command.split(EQUAL_SIGN)[1]
                            key1 = key1.rstrip()
                            key1 = re.split("\s*?\/+", key1)
                            key1 = key1[0]
                            key2 = command.split(EQUAL_SIGN)[0]
                            if ('>>' in key1 or '<<' in key1):
                                if ('>>' in key1):
                                    BinaryOfCompPart = comp[key1[:-2]] >> 1
                                else:
                                    BinaryOfCompPart = comp[key1[:-2]] << 1
                                key1 = BinaryOfCompPart

                        # if its a c instruction with semi-colon
                        else:
                            key2 = "null"
                            key3 = command.split(SEMI_COLON_SIGN)[1]
                            key1 = command.split(SEMI_COLON_SIGN)[0]
                            key3 = key3.rstrip()
                            key3 = re.split("\s*?\/+", key3)
                            key3 = key3[0]
                        BinaryValue = "".join(["11", comp[key1], dest[key2], jump[key3]])
                        final_value = C_INSTRUCTION + str(BinaryValue)
                        HackFile.write(final_value + "\n")


if __name__ == '__main__':
    assemblingProcess()
