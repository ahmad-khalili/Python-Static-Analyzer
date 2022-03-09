# Python Static Analyzer
### Part 1: Reading (.py) the file as text
- Using "with open", we select the file's path and pass on the "r" (which is read) value, then name the opened file as file. Then we exported each line from the now "text file", and added each line to a list of lines. Then, using the indentation, we performed the above mentioned operation while the file was open, and closed when the operations within the indentation were done
```ruby
with open("File/Test.py", "r") as file:
    lines = [line.rstrip() for line in file]
```
### Part 2: Coding the Checkers
#### 1- Checking for Invalid arguments in Function calls
- The "argument_check" function iterates through each line in the list of lines and checks every line for a function definition keyword (which is "def") with a regular expression using the re library and appends that function along with its parameters to a list called "functions"
- Then it takes all the defined functions from "functions list" and appends their only the function names to a new list called "functions_names"
- Then the function reiterates through the lines of code to search for the functions' names along with their first paranthesis "(" to check for function calls and appends them to the "function_calls" list if found
- Finally the function iterates through the called functions lists and all the defined functions list, where it checks if the called's function's name is in the functions' definitions. And if it's true, it takes the function's required parameters from the definition, and function call's passed arguments. Then it checks for the length of the passed arguments in comparison to the required parameters' length. After that, it checks every argument's value if it's found in any of the function's parameters (since Python allows to pass the needed arguments without the right order)
```ruby
def argument_check():
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
                    warning_calls.append(f"Invalid arguments for {called_function} at line {(FileReader.lines.index(called_function)) + 1}")
                for argument in arguments:
                    if not argument.isdigit() and not is_float(argument) and "string" in parameters:
                        continue
                    if argument.isdigit and "int" in parameters:
                        continue
                    if is_float(argument) and "float" in parameters:
                        continue
                    else:
                        warning_calls.append(f"Invalid arguments for {called_function} at line {(FileReader.lines.index(called_function)) + 1}")
    return warning_calls
```
###
### 2- Checking for Functions with more than 3 parameters
- This function, similar to the "argument_check" function, iterates through each line in the list of lines. Then it looks for function definitions, and checks for the number of commas. If they were more than 2 (which are more than 3 parameters), then it appends that function definition to a list called warnings.
```ruby
def parameter_check():
    warnings = []
    for line in FileReader.lines:
        if "def" in line:
            functions = re.findall(r'def (.+?)\:', line)
            counter = functions[0].count(',')
            if counter > 2:
                warnings.append(f'"{functions[0]}" has more than 3 parameters')
    return warnings
```
#### 3- Checking for Unreachable Code
- The function "unreachable_code" iterates through each line in the list of line (but first, it filters the "lines" list from empty lines, since we need to capture every executable line after the stop statements such as "return", "break", "continue") 
- Then it checks if there is a line of code after the stop statement (couldn't figure out how to take all the lines of code after the stop statement because of indentations) and adds it to the "unreachable_lines"
```ruby
def unreachable_code():
    lines = list(filter(None, FileReader.lines))
    unreachable_lines = []
    for line in lines:
        if "return" in line or "break" in line or "continue" in line:
            spaces_count = len(line) - len(line.strip())
            if lines[lines.index(line) + 1].startswith(" " * spaces_count):
                unreachable_lines.append(lines[lines.index(line) + 1].strip() + " is unreachable")
    return unreachable_lines 
```
#### 4- Checking for Magic Numbers
- This checker, consists of 3 main function (one to check for magic numbers in function calls, one for after operators, and one for after statements and conditions)
- The first, reads through lines to check if they have paranthesis and checks if the inside of the paranthesis contains the numbers 0 through 9.
- The second, looks for condition statement or loops and checks to see if after every operator within that operation contains a number 0 through 9
- The third, checks for arithmetic operators in each line and then checks the two ends of those operators if they contain the numbers 0 through 9
```ruby
def magic_call(masseges, linenumber):
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
    
def magic_operation(masseges, linenumber):
    result = []
    statements = ["while", "for", "if"]
    for line in FileReader.lines:
        for operation in statements:
            if operation in line:
                result = re.findall(rf"{operation}.*<|>|=.*", line)
                result += ['contain magic number', 'in line', linenumber]
                masseges += [result]
        linenumber = linenumber + 1

def magic_operator(masseges, linenumber):
    result = []
    operators = ['+', '-', '*', '/', '%']
    for line in FileReader.lines:
        for operator in operators:
            if operator in line:
                result = re.findall(".*[0-9]", line)
                result += ['contain magic number', 'in line', linenumber]
                masseges += [result]
        linenumber = linenumber + 1
```
### Part 3: Outputting the Results
- The "Reporters.py" file takes every returned value from every function in the "Checkers.py" file and outputs them to the console
```ruby
warnings_parameters = Checkers.parameter_check()
warnings_arguments = Checkers.argument_check()
unreachable_code = Checkers.unreachable_code()
magic_after_operator = Checkers.magic_operator([], 1)
magic_after_operation = Checkers.magic_operation([], 1)
magic_in_function_call = Checkers.magic_call([], 1)

for warning in warnings_parameters:
    print(warning)

for warning in warnings_arguments:
    print(warning)

for code in unreachable_code:
    print(code)
```
