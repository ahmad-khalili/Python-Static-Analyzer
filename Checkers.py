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


def printMasseges(masseges):
    mass_range = list(masseges)
    for i in mass_range:
        print(i)


def magicNumberInFunctionCall(masseges, linenumber):
    result = []
    parenthesis = ['(']
    for line in FileReader.lines:
        for n in parenthesis:
            result = re.findall(rf".*{parenthesis}[0-9]", line)
            for x in result:
                if str(x) in line:
                    result += ['contain magic number', 'in line', linenumber]
                    masseges += [result]
    linenumber = linenumber + 1


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def argument_check():
    warnings = []
    function_calls = []
    functions_names = []
    functions = []
    used_functions = []
    for line in FileReader.lines:
        if "def" in line:
            try:
                functions.append((re.findall(r'def (.+?):', line))[0])
            except:
                break
    for function in functions:
        try:
            functions_names.append(re.findall(r'(.+?)\(', function)[0])
        except:
            break

    for line in FileReader.lines:
        for function in functions_names:
            if f'{function}(' in line:
                if "def" not in line:
                    try:
                        function_calls.append(re.findall(fr'({function}.+?\))', line)[0])
                    except:
                        break

    for called_function in function_calls:
        function_name = re.findall(r'(.+?)\(', called_function)[0]
        for function in functions:
            if function_name in function:
                try:
                    parameters = re.findall(r'\((.+?)\)', function)[0].replace(" ", "").split(',')
                except:
                    parameters = [""]
                try:
                    arguments = re.findall(r'\((.+?)\)', called_function)[0].replace(" ", "").split(',')
                except:
                    arguments = [""]
                if len(arguments) != len(parameters):
                    warnings.append(f"Invalid arguments for {called_function} at line {(FileReader.lines.index(called_function)) + 1}")
                for argument in arguments:
                    if not argument.isdigit() and not is_float(argument) and "string" in parameters:
                        continue
                    if argument.isdigit and "int" in parameters:
                        continue
                    if is_float(argument) and "float" in parameters:
                        continue
                    else:
                        warnings.append(f"Invalid arguments for {called_function} at line {(FileReader.lines.index(called_function)) + 1}")
    return warnings


def unreachable_code():
    lines = list(filter(None, FileReader.lines))
    unreachable_lines = []
    for line in lines:
        if "return" in line or "break" in line or "continue" in line:
            spaces_count = len(line) - len(line.strip())
            if lines[lines.index(line) + 1].startswith(" " * spaces_count):
                unreachable_lines.append(lines[lines.index(line) + 1].strip() + " is unreachable")

    return unreachable_lines

def parameter_check():
    warnings = []
    for line in FileReader.lines:
        if "def" in line:
            functions = re.findall(r'def (.+?)\:', line)
            counter = functions[0].count(',')
            if counter > 2:
                warnings.append(f'"{functions[0]}" has more than 3 parameters')
    return warnings
