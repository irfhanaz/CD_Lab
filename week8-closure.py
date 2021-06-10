num = int(input("Number of production rules: "))
start_symbol = input("Enter the Start Symbol: ")
augmented_rule = "S'->"+start_symbol
print("Enter the production rules:")
rules = []
rules.append(augmented_rule)
for _ in range(num):
    rule = input()
    rules.append(rule)

def add_dot(state):
    st = state.replace("->", "->.")
    return st
def closure(state):
    op = []
    op.append(state)
    for item in op:
        i = item[item.index(".")+1]
        if i != len(item) - 1:
            for rule in rules:
                if rule[0][0] == i and (add_dot(rule)) not in op:
                    op.append(add_dot(rule))
        else:
            for rule in rules:
                if rule[0][0] == i and item not in op:
                    op.append(item)
    return op
def swap(new, pos):
    new = list(new)
    temp = new[pos]
    if pos != len(new):
        new[pos]=new[pos+1]
        new[pos+1]=temp
        new1="".join(new)
        return new1
    else:
        return "".join(new)

def goto(rhs):
    op = []
    pos = rhs.index(".")
    if pos != len(rhs) - 1:
        states = list(rhs)
        new = swap(states, pos)
        if new.index(".") != len(states)-1:
            next_item_set = closure(new)
            return next_item_set
        else:
            op.append(new)
            return op
    else:
        return rhs

item0 = closure("S'->."+start_symbol)
collection = []
collection.append(item0)
print(collection)
lr0 = []

while True:
    if len(collection) == 0:
        break
    item_set = collection.pop(0)
    temp = item_set
    lr0.append(item_set)
    if len(item_set) > 1:
        for it in item_set:
            nextt = goto(it)
            print(temp, collection)
            if nextt not in collection and temp != nextt:
                collection.append(goto(it))
#print(collection)
#print(lr0)

for it in lr0:
    for i in range(len(it)):
        if goto(it[i]) not in lr0:
            if it[i].index(".") != (len(it[i])-1):
                lr0.append(goto(it[i]))
print("\n\nFinal Canonical Collection of LR(0) Items:\n", lr0)










