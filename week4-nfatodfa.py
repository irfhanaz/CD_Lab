from collections import deque 
import pandas as pd 

"""def getallpossibleDFAstates(states):
    perms = [] 
    for i in range(2**(len(states))):
        subset = ""
        for j in range(len(states)):
            if (i & (1 << j)) != 0:
                subset += str(states[j]) + ""
        if subset not in perms and len(subset) > 0:
            perms.append(subset)
    dfa_perms = []
    for subset in perms:
        perm = subset.split()
        dfa_perms.append(perm)
    return dfa_perms"""

def reachablestates(nfa, states, alpha):
    dfa_states = states
    dq = deque(states)
    for i in range(len(states)):
        #print(dq)
        for alpha_input, next_states in nfa[i].items():
            if len(next_states) > 1:
                new_state = "".join(next_states)
                if new_state not in dfa_states:
                    dq.append(next_states)
                    dfa_states.append(new_state)
        dq.popleft()
    
    while dq:
        state = dq[0]
        for k in alpha:
            next_states = []
            for i in state:
                index = int(i.strip("q"))
                l = nfa[index][k]
                for r in l:
                    next_states.append(r)
            next_states = sorted(set(next_states))
            #print(next_states)
            new_state = "".join(next_states)
            if new_state not in dfa_states:
                dq.append(next_states)
                dfa_states.append(new_state)
        dq.popleft()
    
    return dfa_states

num_of_states = int(input("Enter the number of states in the NFA: "))
states = [("q" + str(x)) for x in range(num_of_states)]
alphabet = [a for a in input("Enter the alphabet of the NFA: ").strip() if not a.isspace()]
print("The States of the NFA: ", states)
print("The Alphabet of the NFA: ", alphabet)
print("\nEnter NFA transitions: \n")
delta = []
for i in states:
    transitions = {}
    for k in alphabet:
        next_state = [x for x in input("delta(" + i + "," + k + ") ---> ").split()]
        transitions[k] = next_state
    delta.append(transitions)

initial_state = 'q0'
final_states = input("Enter the final state(s) of the NFA: ").split()
#print(final_states)

print("\nNFA Delta Function:\n ", delta, "\n")

dfa_states = reachablestates(delta, states, alphabet)
dfa_final_states = []
dfa = {}
for i in dfa_states:
    dfa[i] = {}
    for k in alphabet:
        index = [int(x) for x in i.split('q') if x.isdigit()]
        next_states = []
        for n in index:
            l = delta[n][k]
            for r in l:
                next_states.append(r)
        next_states = sorted(set(next_states))
        new_state = "".join(next_states)
        if not set(next_states).isdisjoint(final_states):
            dfa_final_states.append(new_state)
        dfa[i][k] = new_state
print("DFA Constructed!")
print("DFA States: ", dfa_states)
print("\nDFA Transition Table:\n")
dfa_table = pd.DataFrame(dfa)
dfa_table = dfa_table.transpose()
print(dfa_table)
print("\nDFA Inital State: ", initial_state)
print("\nDFA Final States: ", sorted(set(dfa_final_states)))
print()












