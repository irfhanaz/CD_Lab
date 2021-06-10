from copy import deepcopy

#Validating the expression
def is_it_valid(expression):
    return check_brackets(expression) and check_operations(expression)
def check_brackets(regex):
    open_brack = 0
    for b in regex:
        if b == '(':
            open_brack += 1
        if b == ')':
            open_brack -= 1
        if open_brack < 0:
            print("ERROR: Missing Bracket ----> Invalid Expression")
            return False
    if open_brack == 0:
        return True
    print("ERROR: Unclosed Bracket ----> Incomplete Expression")
    return False
def check_operations(regex):
    for i, op in enumerate(regex):
        if op == '*':
            if i == 0:
                print('ERROR: There is no argument for "*" at', i)
                return False
            if regex[i - 1] in '(|':
                print('ERROR: There is no argument for "*" at', i)
                return False
        if op == '|':
            if i == 0 or i == len(regex) - 1:
                print('ERROR: There is a missing argument for "|" at', i)
                return False
            if regex[i-1] in '(|':
                print('ERROR: There is a missing argument for "|" at', i)
                return False
            if regex[i+1] in ')|':
                print('ERROR: There is a missing argument for "|" at', i)
                return False
    return True
class Node:
    @staticmethod
    def valid_char(c):
        return c in alpha

    @staticmethod
    def is_concat(c):
        return c == '(' or Node.valid_char(c)

    @staticmethod
    def remove_brackets(ex):
        while ex[0] == '(' and ex[-1] == ')' and is_it_valid(ex[1:-1]):
            ex = ex[1:-1]
        return ex

    def __init__(self, ex):
        self.null = None
        self.beg_pos = []
        self.end_pos = []
        self.item = None
        self.pos = None
        self.leaves = []

        #Check if it is a child
        if len(ex) == 1 and self.valid_char(ex):
            #Child
            self.item = ex
            #Lambda checking
            if use_lambda:
                if self.item == lambda_symbol:
                    self.null = True
                else:
                    self.null = False
            else:
                self.null = False
            return
        
        #If it is a child node
        #Finding the leftmost operators in all three
        star = -1
        orr = -1
        concat = -1

        i = 0

        while i < len(ex):
            if ex[i] == '(':
                bracket_level = 1
                i+=1
                while bracket_level != 0 and i < len(ex):
                    if ex[i] == '(':
                        bracket_level += 1
                    if ex[i] == ')':
                        bracket_level -= 1
                    i+=1
            else:
                i+=1
            if i == len(ex):
                break
            #print(ex[i])
            if self.is_concat(ex[i]):
                if concat == -1:
                    concat = i
                continue
            if ex[i] == '*':
                if star == -1:
                    star = i
                continue
            if ex[i] == '|':
                if orr == -1:
                    orr = i

        if orr != -1:
            #Found an or operation
            self.item = '|'
            self.leaves.append(Node(self.remove_brackets(ex[:orr])))
            self.leaves.append(Node(self.remove_brackets(ex[(orr+1):])))
        elif concat != -1:
            #Found a concatenation
            self.item = '.'
            self.leaves.append(Node(self.remove_brackets(ex[:concat])))
            self.leaves.append(Node(self.remove_brackets(ex[concat:])))
        elif star != -1:
            #Found a star
            self.item = '*'
            self.leaves.append(Node(self.remove_brackets(ex[:star])))

    def parse_into_tree(self, pos, nextpos):
        if self.valid_char(self.item):
            self.beg_pos = [pos]
            self.end_pos = [pos]
            self.pos = pos
            nextpos.append([self.item, []])
            return pos+1
        for leaf in self.leaves:
            pos = leaf.parse_into_tree(pos, nextpos)
        
        if self.item == '.': #concatenation
            if self.leaves[0].null:
                self.beg_pos = sorted(list(set(self.leaves[0].beg_pos + self.leaves[1].beg_pos)))
            else:
                self.beg_pos = deepcopy(self.leaves[0].beg_pos)
            if self.leaves[1].null:
                self.end_pos = sorted(list(set(self.leaves[0].end_pos + self.leaves[1].end_pos)))
            else:
                self.end_pos = deepcopy(self.leaves[1].end_pos)
        
            self.null = self.leaves[0].null and self.leaves[1].null

            for i in self.leaves[0].end_pos:
                for j in self.leaves[1].beg_pos:
                    if j not in nextpos[i][1]:
                        nextpos[i][1] = sorted(nextpos[i][1] + [j])

        elif self.item == '*': #star
            self.beg_pos = deepcopy(self.leaves[0].beg_pos)
            self.end_pos = deepcopy(self.leaves[0].end_pos)
            self.null = True

            for i in self.leaves[0].end_pos:
                for j in self.leaves[0].beg_pos:
                    if j not in nextpos[i][1]:
                        nextpos[i][1] = sorted(nextpos[i][1] + [j])
            
        elif self.item == '|': #or 
            self.beg_pos = sorted(list(set(self.leaves[0].beg_pos + self.leaves[1].beg_pos)))
            self.end_pos = sorted(list(set(self.leaves[0].end_pos + self.leaves[1].end_pos)))
            self.null = self.leaves[0].null and self.leaves[1].null
        
        return pos

    def set_level(self, level):
        print(str(level) + ' ' + self.item, self.beg_pos, self.end_pos, self.null, '' if self.pos == None else self.pos)
        for leaf in self.leaves:
            leaf.set_level(level+1)
class Tree:
    def __init__(self, ex):
        self.root = Node(ex)
        self.nextpos = []
        self.funct()

    def write(self):
        self.root.set_level(0)
    
    def funct(self):
        poss = self.root.parse_into_tree(0, self.nextpos)
    
    def convert_to_NFA(self):
        def contains_hashtag(q):
            for i in q:
                if self.nextpos[i][0] == '#':
                    return True
            return False

        M = [] #Marked states
        Q = [] #States list 
        V = alpha - {'#', lambda_symbol if use_lambda else ''} #alphabet
        d = [] #Delta function, an array of dictionaries d[q] = {x1:q1, x2:q2 ..} where d(q,x1) = q1, d(q,x2) = q2..
        A = [] #Accept states list in the form of indexes (int)
        q0 = self.root.beg_pos

        Q.append(q0)
        if contains_hashtag(q0):
            A.append(Q.index(q0))
        
        while len(Q) - len(M) > 0:
            q = [i for i in Q if i not in M][0]
            d.append({})
            M.append(q)
            for v in V:
                U = []
                for i in q:
                    if self.nextpos[i][0] == v:
                        U = self.nextpos[i][1] + U
                U = sorted(list(set(U)))
                if len(U) == 0:
                    continue
                if U not in Q:
                    Q.append(U)
                    if contains_hashtag(U):
                        A.append(Q.index(U))
                d[Q.index(q)][v] = Q.index(U)
        return NFA(Q, V, d, Q.index(q0), A)
class NFA:
    def __init__(self,Q,V,d,q0,A):
        self.Q = Q
        self.V = V
        self.d = d
        self.q0 = q0
        self.A = A
    def accepts_or_not(self, string):
        if len(set(string) - self.V) != 0:
            print("ERROR: ", set(string) - self.V)
            exit(o)
        q = self.q0
        for i in string:
            if q >= len(self.d):
                print("Message is NOT ACCEPTED. Given state has no transistions.")
                exit(0)
            if i not in self.d[q].keys():
                print("Message is NOT ACCEPTED. Given state has no transistions at this input.")
                exit(0)
            q = self.d[q][i]
        if q in self.A:
            print("Message Accepted! [*/]")
        else:
            print("Message is NOT ACCEPTED. Did not reach an accept state.")
    def finalS(self):
        for i in range(len(self.Q)):
            print(i, self.d[i], '[*/]' if i in self.A else '')
def clean_star(ex):
    for i in range(0, len(ex) - 1):
        while i < len(ex) - 1 and ex[i+1] == ex[i] and ex[i] == '*':
            ex = ex[:i] + regex[i+1:]
    return ex
def determine_alpha(ex):
    return set(ex) - set('()|*')
def preprocess(ex):
    ex = clean_star(ex)
    ex = ex.replace(' ', '')
    ex = '(' + ex + ')' + '#'
    while '()' in ex:
        ex = ex.replace('()','')
    return ex
use_lambda = False
lambda_symb = '_'
ex = input("Please enter the regular expression: ")
if not is_it_valid(ex):
    exit(0)
regex = preprocess(ex)
#print(regex)
alpha = determine_alpha(regex)
t = ''
alpha = alpha.union(set(t))

tree = Tree(regex)
nfa = tree.convert_to_NFA()

print("NFA constructed!")
print('Regular Expression: ' + regex)
print('Alphabet: ' + ''.join(sorted(alpha)))
print('Transition Table: \n')
nfa.finalS()

