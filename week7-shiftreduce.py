
def choose_action(stack, ib, rules):
    action = 'Shift'
    count = 0
    reduce_rule = []
    for rule in rules:
        if rule[1] in stack:
            action = 'Reduce'
            count += 1
            reduce_rule.append(rule)
    return action, reduce_rule

num = int(input("Number of production rules: "))
print("Enter the production rules:")
rules = []
for _ in range(num):
    rule = input()
    rule = rule.split('->')
    rules.append(rule)
#print(rules)
start_symbol = input("Enter the Start Symbol: ")
string = input("Enter the input string: ")
print("\n\nShift Reduce Parsing:\n\n ")
stack = '$'
ib = string+'$'
accept_state = '$'+start_symbol
print("{: ^20}{: ^20}{: ^20}".format("|Stack", "|Input Buffer", "|Parsing Action"))
print("-------------------------------------------------------------------------------------")
while True:
    action, reduce_rule = choose_action(stack, ib, rules)
    if stack == accept_state and ib == '$' and action == "Shift":
        action = "ACCEPTED"
        break
    elif ib == '$' and action == "Shift":
        action = "REJECTED"
        break
    if action == "Shift":
        stack = stack + ib[0]
        ib = ib[1:]
        print("{: ^20}{: ^20}{: ^20}".format(stack, ib, action))
    if action == "Reduce":
        if len(reduce_rule) > 1:
            print("Reduce-reduce conflict.")
            break
        change = len(reduce_rule[0][1])
        stack_size = len(stack)
        stack = stack[:(stack_size - change)]
        stack = stack + reduce_rule[0][0]
        print("{: ^20}{: ^20}{: ^20}".format(stack, ib, (action + " by " + reduce_rule[0][0] + "->" + reduce_rule[0][1])))
    
print("{: ^20}{: ^20}{: ^20}".format(stack, ib, action))

