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

class gameNode:
    def __init__(self, state, turn) -> None:
        self.state = state
        self.turn = turn
        self.plays = 0
        self.wins = 0
        self.losses = 0

def move(state, col, player):
        if state[col]!='0':
            return state
        else:
            for i in range(5,-1,-1):
                if state[5*i + col]=='0':
                    state[5*i + col]=chr(player+ord('0'))
                    break
        return state

qtable = {"000000000000000000000000000000": [1,1,1,1,1]}

def traverse(root):
    while True:
        if (not root.children):
            # create 5 empty nodes
            # choose one of them at random
            # simulate it
            pass
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
