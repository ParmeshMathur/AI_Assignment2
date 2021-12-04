from os import close
from random import randint
from math import sqrt, log2
from pickle import dump, load


# GAME BOARD #
class GameNode:
    def __init__(self, state, turn, parent) -> None:
        self.state = state
        self.turn = turn
        self.plays = 0
        self.wins = 0
        self.losses = 0
        self.parent = parent
        self.children = [None]*5
        self.highest = [5,5,5,5,5]


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


def printState(state):
    print("Board:")
    for i in range(6):
        for j in range (4):
            print(state[i*5 + j], end=", ")
        print (state[i*5 + 4])



# MCTS #
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
        new = move(curr, act, turn)
        while new==curr:
            # act = randint(0,4)
            act=(act+1)%5
            new = move(curr, act, turn)
        highest[act]-=1
        if isWin(new, act, turn):
            if turn==player:
                return 1
            else:
                return -1
        elif max(highest)==0:
            break
        turn = turn^3
        curr=new
    return 0
        

def traverse(root):
    retval=0
    # exploration factor
    c = 2.1
    
    if (not root.children[0]):
        # create 5 empty nodes
        for i in range(5):
            if root.highest[i]<0:
                continue
            root.children[i] = GameNode(move(state=root.state, col=i, player=root.turn), root.turn ^ 3, root)
            root.children[i].highest[i]-=1
        # choose one of them at random
        next = randint(0,4)
        nextNode = root.children[next]
        # simulate it
        retval = simulate(nextNode, root.turn^3)
    else:
        # keep selecting nodes based on UCT
        nextNode = root.children[0]
        for node in root.children:
            if not node:
                continue
            elif not nextNode:
                nextNode = node
            elif node.plays == 0:
                nextNode = node
                break
            # UCB(node) = wins/plays + C*sqrt(log2(Parent(node))/plays)
            elif node.wins/node.plays + c*sqrt(log2(root.plays/node.plays)) > nextNode.wins/nextNode.plays + c*sqrt(log2(root.plays/nextNode.plays)):
                nextNode = node
        retval = traverse(nextNode) * -1
    if retval==-1:
        root.wins += 1
    elif retval==1:
        root.losses += 1
    root.plays+=1
    return -retval


def mcts(root, n):
    # n = 10
    for i in range(n):
        ret = traverse(root)
        while root.parent:
            if ret==1:
                root.parent.losses += 1
            elif ret==-1:
                root.parent.wins += 1
            root.parent.plays += 1
            root = root.parent
            ret*=-1
    
    # newact = root.children.index(max(root.children, key=lambda node: node.plays))
    newact=0
    temp = newact
    flag = True
    if root.highest[newact]<0:
        newact = (newact+1)%5
        flag = False
    while root.highest[newact]<0 and newact!=temp:
        newact = (newact+1)%5
    if newact==temp and not flag:
        return -1
    for i in range(5):
        if root.children[i].plays==0:
            newact=i
            break
        if root.highest[i]>=0 and root.children[i].plays > root.children[newact].plays:
            newact=i
    return newact



# Q LEARNING #
def qlearning(node, prevstate, prevact):
    # choose a state either exploit or explore
    currstate = node.state
    if currstate not in qtable:
        qtable[currstate] = [5,5,5,5,5]

    lr=0.1
    gamma = 1.5
    reward = -1
    prob = randint(0,9)
    newact=0
    if prob==1:
        newact = randint(0,4)
    else:
        newact = qtable[currstate].index(max(qtable[currstate]))

    newstate = move(state=currstate, col=newact, player=2)

    # if state to new action doesn't exist make a new row, assign all q value in row to 5
    # update qtable for the move q learning made in the last move (because now we know reward)
    if prevstate!="000000000000000000000000000000":
        if isWin(newstate, newact, 2):
            qtable[newstate] = [0]*5
            reward = 100
            qtable[currstate][newact] += lr * (reward - qtable[currstate][newact])
        elif max(node.highest)<0:
            qtable[newstate] = [0]*5
            qtable[currstate][newact] += lr * (reward - qtable[currstate][newact])
        else:
            qtable[prevstate][prevact] += lr * (reward + gamma * max(qtable[currstate]) - qtable[prevstate][prevact])

    prevstate = currstate
    prevact = newact
    
    return [newact, prevstate, prevact]

def main():
    global mctsroot1
    global mctsroot2
    global mctscurr1
    global mctscurr2
    global prevstate
    global prevact
    global qtable

    part = input("Enter which part's answer is to be shown (a or c): ")

    turn = 1
    action = 0
    

    if part=="a" or part=="A":
        mctsroot1 = GameNode("000000000000000000000000000000", 1, None)
        mctsroot2 = GameNode("000000000000000000000000000000", 2, None)
        mctscurr1 = mctsroot1
        mctscurr2 = mctsroot2
        print(mctscurr2.state)
        while True:
            print()
            if turn==1:
                action = mcts(mctscurr1, 200)
                if action == -1:
                    break
                mctscurr1 = mctscurr1.children[action]
                if (not mctscurr2.children[0]):
                    # create 5 empty nodes
                    for i in range(5):
                        mctscurr2.children[i] = GameNode(move(state=mctscurr2.state, col=i, player=turn), turn ^ 3, mctscurr2)
                        mctscurr2.children[i].highest[i]-=1
                mctscurr2 = mctscurr2.children[action]
                printState(mctscurr1.state)
            else:
                action = mcts(mctscurr2, 40)
                if action == -1:
                    break
                mctscurr2 = mctscurr2.children[action]
                if (not mctscurr1.children[0]):
                    # create 5 empty nodes
                    for i in range(5):
                        mctscurr1.children[i] = GameNode(move(state=mctscurr1.state, col=i, player=turn), turn ^ 3, mctscurr1)
                        mctscurr1.children[i].highest[i]-=1
                mctscurr1 = mctscurr1.children[action]
                printState(mctscurr2.state)
            if isWin(mctscurr1.state, action, turn):
                if turn==1:
                    print("MCTS200 has won")
                else:
                    print("MCTS40 has won")
                break
            turn = turn^3

    else:
        mctsroot1 = GameNode("000000000000000000000000000000", 1, None)
        mctscurr1 = mctsroot1
        a_file = open("2018A7PS0133G_PARMESH.dat", "rb")
        qtable = load(a_file)
        prevstate = "000000000000000000000000000000"
        prevact = -1

        while True:
            print()
            if turn==1:
                action = mcts(mctscurr1, 200)
                if action == -1:
                    print("Draw")
                    break
                mctscurr1 = mctscurr1.children[action]
                printState(mctscurr1.state)
            else:
                [action, prevstate, prevact] = qlearning(mctscurr1, prevstate, prevact)
                if action == -1:
                    print("Draw")
                    break
                if (not mctscurr1.children[0]):
                    # create 5 empty nodes
                    for i in range(5):
                        mctscurr1.children[i] = GameNode(move(state=mctscurr1.state, col=i, player=turn), turn ^ 3, mctscurr1)
                        mctscurr1.children[i].highest[i]-=1
                mctscurr1 = mctscurr1.children[action]
                printState(mctscurr1.state)
            if isWin(mctscurr1.state, action, turn):
                if turn==1:
                    print("MCTS has won")
                else:
                    print("Q-Learning has won")
                break
            turn = turn^3
        close(a_file)
    
    print("game over \n")
    print()

main()