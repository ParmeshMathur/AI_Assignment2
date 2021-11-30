from random import randint
from math import gamma, sqrt, log2

class MCTSNode:
    def __init__(self, state, turn, parent) -> None:
        self.state = state
        self.turn = turn
        self.plays = 0
        self.wins = 0
        self.losses = 0
        self.parent = parent
        self.children = []

# class gameNode:
#     def __init__(self, state, turn) -> None:
#         self.state = state
#         self.turn = turn
#         self.plays = 0
#         self.wins = 0
#         self.losses = 0

def move(state, col, player):
        if state[col]!='0':
            return state
        else:
            temp = []
            temp[:0] = state
            for i in range(5,-1,-1):
                if temp[5*i + col]=='0':
                    temp[5*i + col]=chr(player+ord('0'))
                    break
            state=""
            for i in temp:
                state += i
        return state

def isWin(state, col, player):
    row=5
    for row in range(5,-1,-1):
        if state[5*row + col]=='0':
            break

    # principal diag
    together=1
    if col>0:
        i=1
        while((i<=col and i<=row) and state[(row-i)*5 + col-i]==player):
            together+=1
            i+=1
    if col<4:
        i=1
        while((col+i<=4 and row+i<=5) and state[(row+i)*5 + col+i]==player):
            together+=1
            i+=1
    if together>=4:
        return True

    # other diagonal
    together=1
    if col>0:
        i=1
        while((i<=col and row+i<=5) and state[(row+i)*5 + col-i]==player):
            together+=1
            i+=1
    if col<4:
        i=1
        while((col+i<=4 and i<=row) and state[(row-i)*5 + col+i]==player):
            together+=1
            i+=1
    if together>=4:
        return True

    # horizontal
    together=1
    if col>0:
        i=1
        while(i<=col and state[row*5 + col-i]==player):
            together+=1
            i+=1
    if col<4:
        i=1
        while(col+i<=4 and state[row*5 + col+i]==player):
            together+=1
            i+=1
    if together>=4:
        return True

    # vertical
    together=1
    if row >=3:
        i=1
        while(row+i<=5 and state[(row+i)*5 + col]==player):
            together+=1
            i+=1
    if together==4:
        return True
    
    return False

qtable = {"000000000000000000000000000000": [1,1,1,1,1]}

def simulate(node, player):
    curr = node.state
    highest = [0,0,0,0,0]
    for i in range(5):
        for j in range(5,-1,-1):
            if curr[j*5 + i]=='0':
                highest[i]=j
                break
    if max(highest)==0:
        return 0

    turn = player
    new = curr
    while True:
        act = randint(0,4)
        new = move(curr, act, turn^3)
        while new==curr:
            act = randint
            new = move(curr, act, turn^3)
        highest[new]-=1
        if isWin(new, act, turn):
            if turn==player:
                return 1
            else:
                return -1
        elif max(highest)==0:
            break
    return 0
        

def traverse(root):
    while True:
        if (not root.children):
            # create 5 empty nodes
            for i in range(5):
                root.children[i] = MCTSNode(move(state=root.state, col=i, player=root.turn), root.turn ^ 3, root)
            # choose one of them at random
            next = randint(0,4)
            nextNode = root.children[next]
            # simulate it
            retval = simulate(nextNode, root.turn)
        else:
            # keep selecting nodes based on UCT
            # UCB(node) = wins/plays + C*sqrt(log2(Parent(node))/plays)
            pass

def mcts():
    root = MCTSNode("000000000000000000000000000000")

    for i in range(40):
        # traverse
        pass

def qlearning(currstate):
    # choose a state either exploit or explore
    lr=0.8
    gamma = 1.5
    reward = -10
    prob = randint(0,9)
    newact=0
    if prob==1:
        newact = randint(0,4)
    else:
        newact = qtable[currstate].index(max(qtable[currstate]))

    # newstate = self.encoder()
    newstate = move(state=currstate, col=newact, player=2)

    # if state to new action doesn't exist make a new row, assign all q value in row to 1
    if newstate not in qtable:
        qtable[newstate] = [5,5,5,5,5]
    else:
        qtable[currstate][newact] += lr * (reward + gamma * max(qtable[newstate]) - qtable[currstate][newact])
    
    return newact
