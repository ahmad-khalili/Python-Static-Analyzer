import Checkers

messages = []
line_number = 1

warnings_parameters = Checkers.parameter_check()
warnings_arguments = Checkers.argument_check()
unreachable_code = Checkers.unreachable_code()
Checkers.magic_operator(messages, line_number)
Checkers.magic_operation(messages, line_number)
Checkers.magic_call(messages, line_number)

for warning in warnings_parameters:
    print(warning)

for warning in warnings_arguments:
    print(warning)

for code in unreachable_code:
    print(code)


messages_list = Checkers.print_messages(messages)

for message in messages_list:
    message[0] = message[0].strip()
    print(message)



