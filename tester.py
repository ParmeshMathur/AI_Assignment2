from random import randint
from math import sqrt, log2

class GameNode:
    def __init__(self, state, turn, parent) -> None:
        self.state = state
        self.turn = turn
        self.plays = 0
        self.wins = 0
        self.losses = 0
        self.parent = parent
        self.children = [None]*5


def move(state, col, player):
    # print("move col:", col)
    if state[col]!='0':
        return state
    else:
        temp = []
        temp[:0] = state
        # print(state)
        for i in range(5,-1,-1):
            if temp[5*i + col]=='0':
                temp[5*i + col]=chr(player+ord('0'))
                break
        state=""
        for i in temp:
            state += i
    # print(state)
    return state

def isWin(state, col, play):
    player = chr(play+ord('0'))
    row=5
    for row in range(5,-1,-1):
        if state[5*row + col]=='0':
            break
    row+=1

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
    if row <=2:
        i=1
        while(row+i<=5 and state[(row+i)*5 + col]==player):
            together+=1
            i+=1
    if together==4:
        return True
    
    return False

def simulate(node, player):
    # print("sim: player =", player)
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
        new = move(curr, act, turn)
        while new==curr:
            act = randint(0,4)
            # new = move(curr, act, turn)
            act+=1
        highest[act]-=1
        if isWin(new, act, turn):
            if turn==player:
                # print("retval=1")
                return 1
            else:
                # print("retval=-1")
                return -1
        elif max(highest)==0:
            break
        turn = turn^3
        curr=new
    # print("retval=0")
    return 0
        

def traverse(root):
    retval=0
    # exploration factor
    c = 1.1
    # print(root.state)
    
    if (not root.children[0]):
        # create 5 empty nodes
        # print("extension")
        for i in range(5):
            root.children[i] = GameNode(move(state=root.state, col=i, player=root.turn), root.turn ^ 3, root)
        # choose one of them at random
        next = randint(0,4)
        # print("next:", next)
        nextNode = root.children[next]
        # simulate it
        retval = simulate(nextNode, root.turn^3)
    else:
        # keep selecting nodes based on UCT
        nextNode = root.children[0]
        for node in root.children:
            # UCB(node) = wins/plays + C*sqrt(log2(Parent(node))/plays)
            if node.plays == 0:
                nextNode = node
                break
            elif node.wins/node.plays + c*sqrt(log2(root.plays/node.plays)) > nextNode.wins/nextNode.plays + c*sqrt(log2(root.plays/nextNode.plays)):
                nextNode = node
        retval = traverse(nextNode) * -1
    # print("back to trav")
    if retval==-1:
        root.wins += 1
    elif retval==1:
        root.losses += 1
    root.plays+=1
    return -retval

def mcts(root, n):
    # n = 10
    for i in range(n):
        traverse(root)
    
    newact = root.children.index(max(root.children, key=lambda node: node.plays))
    return newact

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

    # if state to new action doesn't exist make a new row, assign all q value in row to 5
    if newstate not in qtable:
        qtable[newstate] = [5,5,5,5,5]
    else:
        qtable[currstate][newact] += lr * (reward + gamma * max(qtable[newstate]) - qtable[currstate][newact])
    
    return newact

def main():
    # TODO: make sure game does not stall
    turn = 1
    action = 0
    global mctsroot1
    global mctsroot2 
    mctsroot1 = GameNode("000000000000000000000000000000", 1, None)
    mctsroot2 = GameNode("000000000000000000000000000000", 2, None)
    global mctscurr1
    global mctscurr2
    mctscurr1 = mctsroot1
    mctscurr2 = mctsroot2
    winTally1 = [0,0]
    # winTally2 = [0,0]

    global qtable
    qtable = {"000000000000000000000000000000": [1,1,1,1,1]}

    for j in range(10):
        while True:
            print()
            print(mctscurr2.state)
            if turn==1:
                action = mcts(mctscurr1, 40)
                mctscurr1 = mctscurr1.children[action]
                if (not mctscurr2.children[0]):
                    # create 5 empty nodes
                    for i in range(5):
                        mctscurr2.children[i] = GameNode(move(state=mctscurr2.state, col=i, player=mctscurr2.turn), mctscurr2.turn ^ 3, mctscurr2)
                mctscurr2 = mctscurr2.children[action]
            else:
                action = mcts(mctscurr2, 200)
                mctscurr2 = mctscurr2.children[action]
                if (not mctscurr1.children[0]):
                    # create 5 empty nodes
                    for i in range(5):
                        mctscurr1.children[i] = GameNode(move(state=mctscurr1.state, col=i, player=mctscurr1.turn), mctscurr1.turn ^ 3, mctscurr1)
                mctscurr1 = mctscurr1.children[action]
            if isWin(mctscurr1.state, action, turn):
                if turn==1:
                    print("MCTS40 has won")
                    winTally1[0]+=1
                else:
                    print("MCTS200 has won")
                    winTally1[1]+=1
                break
            turn = turn^3          
        print("game over")
    print("MCTS40:",winTally1[0])
    print("MCTS200:",winTally1[1])

main()