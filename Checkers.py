import FileReader
import re

masseges = []
linenumber = 1


def magicNumberAfterOperator(masseges, linenumber):

    result = []
    operators = ['+', '-', '*', '/', '%']
    for line in FileReader.lines:
        for operator in operators:
            if operator in line:
                result = re.findall(".*[0-9]", line)
                result += ['contain magic number', 'in line', linenumber]
                masseges += [result]
        linenumber = linenumber + 1
        

def magicNumberAfterOperation(masseges, linenumber):

    result = []
    statements = ["while", "for", "if"]
    for line in FileReader.lines:
        for operation in statements:
            if operation in line:
                result = re.findall(rf"{operation}.*<|>|=.*", line)
                result += ['contain magic number', 'in line', linenumber]
                masseges += [result]
        linenumber = linenumber + 1




