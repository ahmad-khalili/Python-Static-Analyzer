import Checkers

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
