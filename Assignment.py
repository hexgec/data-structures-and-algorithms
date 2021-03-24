import random as r
import copy

class State:
    # initializing a state with whether it is accepting or not, its outgoing transitions and that it is not visited
    def __init__(self, nTemp):
        self.num = -1
        self.acc = r.randint(0, 1)
        self.a = r.randint(0, nTemp)
        self.b = r.randint(0, nTemp)
        self.visited = -1


# returns the position in the list of num
def find(list, num):
    for x in range(len(list)):
        if list[x].num == num:
            return x


# checking if the state is visited
def visitedCheck(toCheck, tstates):
    global queue, maxDepth
    # states are checked whether they have been visited or not
    # if not then they are added to the queue and 'visited' is changed to their depth
    numA = find(tstates, toCheck.a)
    if tstates[numA].visited == -1:
        queue.append(numA)
        tstates[numA].visited = toCheck.visited + 1
        if toCheck.visited+1 > maxDepth:
            maxDepth = toCheck.visited+1
    numB = find(tstates, toCheck.b)
    if tstates[numB].visited == -1:
        queue.append(numB)
        tstates[numB].visited = toCheck.visited + 1
        if toCheck.visited+1 > maxDepth:
            maxDepth = toCheck.visited+1


# the breadth first search
def depth(tstates):
    global currentState, queue
    if not queue == []:
        currentState = queue[0]
        visitedCheck(tstates[currentState], tstates)
        queue.pop(0)
        return depth(tstates)
    else:
        return tstates[currentState].visited


# generating the amount of states
n = r.randint(16, 64)
states = []

# creating the states and initializing them
for x in range(n):
    states.append(State(n-1))
    states[x].num = x

# generating the start state
st = r.randint(0, n-1)

# initializing all the necessary variables for the start of the breadth first search
maxDepth = 0
start = find(states, st)
queue = [start]
states[start].visited = 0

# stores the depth
finalDepth = depth(states)

print("\nThe number of states in 𝐴 is: " + str(n))
print("The depth of 𝐴 is: " + str(finalDepth))

# start of Hopcroft's algorithm

M = copy.deepcopy(states)
s = 0

# resetting all the states to be unvisited
# and gets rid of unreachable
while s < len(M):
    if not M[s].visited == -1:
        M[s].visited = -1
        s = s + 1
    else:
        M.pop(s)


# returns the inverse of the parameter
def inv(elem, ans):
    global M
    while not elem[0] == []:
        num = elem[0].pop(0).num
        if elem[1] == 'a':
            for mm in M:
                if mm.a == num:
                    if mm.num not in ans:
                        ans.append(copy.deepcopy(mm.num))
        else:
            for mm in M:
                if mm.b == num:
                    if mm.num not in ans:
                        ans.append(copy.deepcopy(mm.num))
    return ans


# splits a list and returns the 2 resultant arrays
def splitter(toSplit, split, s1):
    s = 0
    while s < len(split):
        for ts in toSplit:
            if split[s] == ts.num:
                s1.append(ts)
                toSplit.remove(ts)
                break
        else:
            s = s + 1
    return toSplit, s1


P = [[], []]

# splits the automaton into accepting and non accepting
for m in M:
    if m.acc == 1:
        P[0].append(copy.deepcopy(m))
    else:
        P[1].append(copy.deepcopy(m))

W = []


# adds 2 new elements to W
def wAdd(t1, t2):
    global W
    if len(t1) <= len(t2):
        W.append([copy.deepcopy(P[0]), 'a'])
        W.append([copy.deepcopy(P[0]), 'b'])
    else:
        W.append([copy.deepcopy(P[1]), 'a'])
        W.append([copy.deepcopy(P[1]), 'b'])


wAdd(P[0], P[1])

# main code for Hopcroft's algorithm
while not W == []:  # executes until W is empty
    temp = W.pop(0)
    split = inv(temp, [])  # inverse is found
    if not split == []:
        P2 = []
        # the elements in P are split if needed according to the inverse
        for p in P:
            tp = copy.deepcopy(p)
            t1, t2 = splitter(tp, split, [])  # the list is split according to the inverse
            if (t1 == []) or (t2 == []):
                P2.append(p)
            else:  # if it is split then values in P are split too and 2 new elements are added to W
                P2.append(t1)
                P2.append(t2)
                wAdd(t1, t2)
        P = P2
        W2 = []
        # the elements in W are also split if needed according to the inverse
        for w in W:
            tw = copy.deepcopy(w[0])
            t1, t2 = splitter(tw, split, [])
            if (t1 == []) or (t2 == []):
                W2.append(w)
            else:
                W2.append([t1, w[1]])
                W2.append([t2, w[1]])
        W = W2

print("\nThe new automaton M after using Hopcroft's algorithm is: ")
for p in P:
    for p2 in p:
        print(p2.num, end=", "),
    print("|", end=" "),

finalM = []
check = []
check2 = []

# arranging the starting element's position
for p in P:
    for p2 in range(len(p)):
        if st == p[p2].num:
            if p2 != 0:
                temp = p.pop(p2)
                p.insert(0, temp)

# if there is more then one element in a partition,
# then the other elements besides the first are noted of and removed
for p in P:
    finalM.append(copy.deepcopy(p[0]))
    if len(p) > 1:
        for p2 in p[1:]:
            check.append(copy.deepcopy(p2.num))
            check2.append(copy.deepcopy(p[0].num))

# if any element in the list leads to one of the removed elements
# then the a or b are altered to point to the correct new element
for p in finalM:
    if p.a in check:
        let = check.index(p.a)
        p.a = copy.deepcopy(check2[let])
    if p.b in check:
        let = check.index(p.b)
        p.b = copy.deepcopy(check2[let])


# Computing the new depth
maxDepth = 0
start = find(finalM, st)
queue = [start]
finalM[start].visited = 0

finalDepth = depth(finalM)

print("\n\nThe number of states in 𝑀 is: " + str(len(finalM)))
print("The depth of 𝑀 is: " + str(finalDepth) + "\n")
