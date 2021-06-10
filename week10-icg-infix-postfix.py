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

def postfix_to_prefix(formula):
    stack = []
    output = ''
    n = len(formula)
    for i in range(n):
        if formula[i] in OPERATORS:
            op1 = stack[-1]
            stack.pop()
            op2 = ''
            if stack:
                op2 = stack[-1]
                stack.pop()
            temp = formula[i] + op2 + op1
            stack.append(temp)
        else:
            stack.append(formula[i])
    for i in stack:
        output += i
    print("PREFIX: ", output)
    return output    

 
exp = input('Enter the expression in infix form: ')
postfix = infix_to_postfix(exp)  
prefix = postfix_to_prefix(postfix)