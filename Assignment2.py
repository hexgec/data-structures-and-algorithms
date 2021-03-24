import random as r
import sys
from Assignment import finalM, find, start

strings = []


# the 100 random strings are generated and returned
def genStr(tstrings):
    for num in range(100):
        length = 0
        tstrings.append("")
        while length <= 128:
            letter = r.randint(0, 2)
            if letter == 0:
                 tstrings[num] = strings[num] + "a"
            elif letter == 1:
                 tstrings[num] = strings[num] + "b"
            else:
                 break
    return strings


# checks if each string is accepting or not
def strCheck(tstrings, finalM):
    for string in tstrings:
        state = start
        for char in string:
            if char == 'a':
                state = find(finalM, finalM[state].a)
            else:
                state = find(finalM, finalM[state].b)
        # after the entire string is traversed,
        # the state is checked whether it is accepting or not
        if finalM[state].acc == 0:
            print(string + " :: Rejecting")
        else:
            print(string + " :: Accepting")


strings = genStr(strings)
print("The string parser:")
strCheck(strings, finalM)  # displays the answers

# resets all states to be unvisited
for state in finalM:
    state.visited = -1

# initiation of the necessary variables needed for tarjan's algorithm
idNo = 0
idLows = []  # stores relation between id and low of each state
related = []  # stores relation between states and id
sccCount = 0
largest = 0
smallest = sys.maxsize


# returns the id of a state
def findRel(state):
    for rel in related:
        if rel[0] == state:
            return rel[1]


# returns the position of the id in the list
def idPos(id):
    for elem in range(len(idLows)):
        if idLows[elem][0] == id:
            return elem


def dfs(finalM, state, stack):
    global idNo, sccCount, largest, smallest, idLows
    idLows.append([idNo, idNo])  # id, low
    stack.append(idNo)
    related.append([state, idNo])
    idNo = idNo + 1
    thisId = findRel(state)

    finalM[state].visited = 0

    # if a of the  current state is unvisited,
    # then the dfs is recursively called on this element
    num = find(finalM, finalM[state].a)
    if finalM[num].visited == -1:
        dfs(finalM, num, stack)
    checkid = findRel(num)
    # if the id of a is already in the stack,
    # then the current low is changed to be the min of the current low and the low of a
    if checkid in stack:
        position = idPos(thisId)
        position2 = idPos(checkid)
        idLows[position][1] = min(idLows[position][1], idLows[position2][1])

    # code is repeated for b
    num = find(finalM, finalM[state].b)
    if finalM[num].visited == -1:
        dfs(finalM, num, stack)
    checkid = findRel(num)
    if checkid in stack:
        position = idPos(thisId)
        position2 = idPos(checkid)
        idLows[position][1] = min(idLows[position][1], idLows[position2][1])

    # if the id is equal to the low
    if idLows[checkid][0] == idLows[checkid][1]:
        size = 0
        # remove the items in the scc from the stack
        for item in reversed(range(len(stack))):
            pos = idPos(stack[item])
            idLows[pos][1] = thisId
            temp = stack[item]
            stack.pop(item)
            size = size + 1
            if temp == thisId:
                break
        # only add as an scc if there is a connection between the elements
        if (size > 1) or (finalM[state].num == finalM[state].a) or (finalM[state].num == finalM[state].b):
            sccCount = sccCount + 1
            # change the smallest or largest if needed
            if size > largest:
                largest = size
            if size < smallest:
                smallest = size

    return stack


def tarjan():
    stack = []
    for state in range(len(finalM)):
        if finalM[state].visited == -1:  # calls the dfs on every unvisited state
            stack = dfs(finalM, state, stack)


tarjan()

print("\nThe number of strongly connected components in 𝑀 are: " + str(sccCount))

if largest == 0:
    print("There is no largest SCC in 𝑀 ")
else:
    print("The size of the largest SCC in 𝑀 is: " + str(largest))

if smallest == sys.maxsize:
    print("There is no smallest SCC in 𝑀 ")
else:
    print("The size of the smallest SCC in 𝑀 is: " + str(smallest))

print("rip")