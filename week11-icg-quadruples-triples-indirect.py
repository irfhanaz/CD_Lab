OPERATORS = set(['+', '-', '*', '/', '(', ')'])
PRIORITY = {'+':1, '-':1, '*':2, '/':2}

def infix_to_postfix(formula):
    stack = [] # only pop when the coming op has priority 
    output = ''
    for ch in formula:
        if ch not in OPERATORS:
            output += ch
        elif ch == '(':
            stack.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop() # pop '('
        else:
            while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(ch)
    # leftover
    while stack: output += stack.pop()
    print("POSTFIX: ", output)
    return output

def generate_three_address_code(exp):
    stack = []
    post = infix_to_postfix(exp)
    num = 1
    for i in post:
        if i not in OPERATORS:
            stack.append(i)
        else:
            print(f't{num} := {stack[-2]} {i} {stack[-1]}')
            stack = stack[:-2]
            stack.append(f't{num}')
            num+=1

def quad(exp):
    print("\nThe Quadruple Representation:")
    print(" OP  | ARG 1| ARG 2| RESULT ")
    stack = []
    num = 1
    for i in exp:
        if i not in OPERATORS:
            stack.append(i)
        else:
            print("{:^4} | {:^4} | {:^4} | t{}".format(i, stack[-2], stack[-1], num))
            stack = stack[:-2]
            stack.append(f"t{num}")
            num+=1

def trip(exp):
    print("\nThe Triple Representation:")
    print("LOC | OP   | ARG 1| ARG 2   ")
    stack = []
    num = 1
    for i in exp:
        if i not in OPERATORS:
            stack.append(i)
        else:
            print("({}) | {:^4} | {:^4} | {}".format(num, i, stack[-2], stack[-1]))
            stack = stack[:-2]
            stack.append(f"({num})")
            num+=1

def ind(exp):
    pt = {}
    print("\nThe Indirect Triple Representation:")
    print("LOC |  OP  | ARG 1| ARG 2   ")
    stack = []
    num = 1
    for i in exp:
        if i not in OPERATORS:
            stack.append(i)
        else:
            print("({}) | {:^4} | {:^4} | {}".format(num, i, stack[-2], stack[-1]))
            stack = stack[:-2]
            stack.append(f"({num})")
            pt[num+15] = num
            num+=1
    print("\nPointer Array:")
    print("Pointer To: | Statement ")
    for k, v in pt.items():
        print("{:^12}| {:^4} ".format('('+str(k)+')', '('+str(v)+')'))
           
exp = input('Enter the expression in infix form: ')
generate_three_address_code(exp)
postfix = infix_to_postfix(exp) 
quad(postfix)
trip(postfix)
ind(postfix)
