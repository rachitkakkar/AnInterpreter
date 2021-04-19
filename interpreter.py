from time import sleep
from sys import stdout, argv

class Variable:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class Function:
    def __init__(self, identifier, args, expression):
        self.identifier = identifier
        self.args = args
        self.expression = expression

    def run(self, passed_args):
        re_expression = self.expression
        for i in range(len(passed_args)):
            re_expression = re_expression.replace(self.args[i], passed_args[i])

        return eval(re_expression)

def evaluate(expression, functions):
    sections = expression.split(":")
    new_sections = []

    for section in sections:
        if "&" in section:
            for function in functions:
                if function.identifier in section:
                    new_sections.append(str(function.run(section[section.find("(")+1 : section.find(")")].split(","))))

        else:
            new_sections.append(section)

    new_expression = ""

    for sub_expression in new_sections:
        new_expression += sub_expression

    return eval(new_expression)

def replace_variables(line, variables):
    for variable in variables:
        line = line.replace(variable.identifier, str(variable.value))

    return line

def interpret_code(lines, debug=False, color=False):
    line_number = 0
    skip_if = False
    variables = []
    functions = []

    while line_number < len(lines):
        # Remove Spaces/Semicolons/Newline And Replace Variables
        line = lines[line_number]
        line = line.replace(" ", "")
        line = line.replace(";", "")

        if "let" not in line and "reassign" not in line and "print_str_ln" not in line and "print_str" not in line:
            line = replace_variables(line, variables)

        # Add Spaces
        line = line.replace("<s>", " ")
        if "$" not in line: # Comment
            if not skip_if:
                if debug:
                    if color: stdout.write("\033[1;34m")
                    print("---")
                    print(lines[line_number])
                    print("---")
                    sleep(0.1)

                if "let" in line: # Variable Assignment
                    line = line.replace("let", "")
                    
                    identifier, value = line.split("=")
                    variables.append(Variable(identifier, evaluate(replace_variables(value, variables), functions)))

                if "reassign" in line: #Variable Reassignment
                    line = line.replace("reassign", "")

                    identifier, value = line.split("=")

                    for variable in variables:
                        if variable.identifier == identifier:
                            variable.value = evaluate(replace_variables(value, variables), functions)

                if "jump" in line: # Jump Statment
                    line = line.replace("jump", "")
                    line_number = evaluate(line, functions)-1
                    continue

                if "if" in line:
                    line = line.replace("if", "")
                    line = line.replace("{", "")

                    if "==" in line: # Comparison Equal
                        value1, value2 = line.split("==")

                        if evaluate(value1, functions) != evaluate(value2, functions):
                            skip_if = True

                    elif "!=" in line: # Comparison Not Equal
                        value1, value2 = line.split("!=")

                        if evaluate(value1, functions) == evaluate(value2, functions):
                            skip_if = True

                    elif "<=" in line: # Comparison Less Than Or Equal Too
                        value1, value2 = line.split("<=")

                        if evaluate(value1, functions) > evaluate(value2, functions):
                            skip_if = True

                    elif ">=" in line: # Comparison Greater Than Or Equal Too
                            value1, value2 = line.split(">=")

                            if evaluate(value1, functions) < evaluate(value2, functions):
                                skip_if = True

                    elif "<" in line: # Comparison Less Than
                            value1, value2 = line.split("<")

                            if evaluate(value1, functions) >= evaluate(value2, functions):
                                skip_if = True

                    elif ">" in line: # Comparison Greater Than
                            value1, value2 = line.split(">")

                            if evaluate(value1, functions) <= evaluate(value2, functions):
                                skip_if = True

                    else:
                        print("Error in if...")

                if "func" in line:
                    line = line.replace("func", "")
                    line = line.replace("return", "")
                    in_parenthesis = line[line.find("(")+1 : line.find(")")]
                    line = line.replace(in_parenthesis, "")

                    identifier, expression = line.split(":")
                    identifier = identifier.replace("()", "")
                    args = in_parenthesis.split(",")

                    functions.append(Function(identifier, args, expression))

                if "halt" in line:
                    exit()
                
                # Built in functions
                if "print_str_ln" in line:
                    line = line.replace("print_str_ln", "")
                    if debug and color: 
                        stdout.write("\033[1;31m")
                    
                    print(line)

                if "print_str" in line:
                    line = line.replace("print_str", "")
                    if debug and color: 
                        stdout.write("\033[1;31m")
                    print(line, end ="")

                if "print_expr_ln" in line:
                    line = line.replace("print_expr_ln", "")
                    if debug and color: 
                        stdout.write("\033[1;31m")
                    print(evaluate(line, functions))

                if "print_expr" in line:
                    line = line.replace("print_expr", "")
                    if debug and color: 
                        stdout.write("\033[1;31m")
                    print(evaluate(line, functions), end="")

            else:
                if "}" in line:
                    skip_if = False
        
        line_number += 1

if __name__ == "__main__":
    lines = []
    for line in open(argv[2]):
        line = line.replace("\n", "")
        lines.append(line)

    if argv[1] == "d":  interpret_code(lines, debug=True, color=False)
    if argv[1] == "dc":  interpret_code(lines, debug=True, color=True)
    elif argv[1] == "r":  interpret_code(lines, debug=False)