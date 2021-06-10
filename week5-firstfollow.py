import sys
sys.setrecursionlimit(60)

def first(string):
    #print("first({})".format(string))
    f = set()
    if string in nonterm:
        other = pdict[string]

        for i in other:
            f2 = first(i)
            f = f |f2

    elif string in term:
        f = {string}

    elif string=='' or string=='@':
        f = {'@'}

    else:
        f2 = first(string[0])
        if '@' in f2:
            i = 1
            while '@' in f2:
                f = f | (f2 - {'@'})
                if string[i:] in term:
                    f = f | {string[i:]}
                    break
                elif string[i:] == '':
                    f = f | {'@'}
                    break
                f2 = first(string[i:])
                f = f | f2 - {'@'}
                i += 1
        else:
            f = f | f2
    return  f


"""def follow(nT):
    #print("inside follow({})".format(nT))
    follow_ = set()
    #print("FOLLOW", FOLLOW)
    prods = pdict.items()
    if nT==start_s:
        follow_ = follow_ | {'$'}
    for nt,rhs in prods:
        #print("nt to rhs", nt,rhs)
        for alt in rhs:
            for char in alt:
                if char==nT:
                    following_str = alt[alt.index(char) + 1:]
                    if following_str=='':
                        if nt==nT:
                            continue
                        else:
                            follow_ = follow_ | follow(nt)
                    else:
                        follow_2 = first(following_str)
                        if '@' in follow_2:
                            follow_ = follow_ | follow_2-{'@'}
                            follow_ = follow_ | follow(nt)
                        else:
                            follow_ = follow_ | follow_2
    #print("returning for follow({})".format(nT),follow_)
    return follow_"""





tcount=int(input("Enter the number of terminals: "))

term = []

print("Enter the terminals: ")
for i in range(tcount):
    term.append(input())

ncount=int(input("Enter the number of nonterminals: "))

nonterm = []

print("Enter the nonterminals: ")
for i in range(ncount):
    nonterm.append(input())

start_s = input("Enter the start symbol: ")

prod_count = int(input("Enter the number of productions: "))

prods = []

print("Enter the productions: ")
for i in range(prod_count):
    prods.append(input())


#print("terminals", terminals)

#print("non terminals", non_terminals)

#print("productions",productions)


pdict = {}

pdict[nonterm[0]] = []


#print("productions_dict",productions_dict)

for prod in prods:
    nonterm_to_prod = prod.split("->")
    others = nonterm_to_prod[1].split("/")
    for other in others:
        pdict[nonterm_to_prod[0]].append(other)

#print("productions_dict",productions_dict)

#print("nonterm_to_prod",nonterm_to_prod)
#print("alternatives",alternatives)


FIRST = {}
#FOLLOW = {}

"""for non_terminal in nonterm:
    FIRST[non_terminal] = set()"""

"""for non_terminal in nonterm:
    FOLLOW[non_terminal] = set()"""

#print("FIRST",FIRST)

FIRST[nonterm[0]] = set()
FIRST[nonterm[0]] = FIRST[nonterm[0]] | first(nonterm[0])

#print("FIRST",FIRST)


"""FOLLOW[start_s] = FOLLOW[start_s] | {'$'}
for non_terminal in nonterm:
    FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)"""

#print("FOLLOW", FOLLOW)

print("{: ^20}{: ^20}".format('Non Terminals','First'))
#for non_terminal in nonterm:
print("{: ^20}{: ^20}".format(nonterm[0],str(FIRST[nonterm[0]])))
