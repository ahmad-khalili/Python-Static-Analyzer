with open("File/Test.py", "r") as file:
    lines = [line.rstrip() for line in file]

lines = list(filter(None, lines))

