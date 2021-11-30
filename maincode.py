from random import randint

# GAME
class Connect4Board:
    def __init__(self):
        self.board = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        # self.board = ["000000000000000000000000000000"]
        self.highest =  [0,0,0,0,0]
    
    def move(self, col, player):
        if self.highest[col]>=6:
            return 1
        else:
            self.board[5-self.highest[col]][col]=player
            self.highest[col]+=1
        return 0
    
    def isWin(self, col, player):
        row = 5-self.highest[col]+1

        # principal diag
        together=1
        if col>0:
            i=1
            while((i<=col and i<=row) and self.board[row-i][col-i]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while((col+i<=4 and row+i<=5) and self.board[row+i][col+i]==player):
                together+=1
                i+=1
        if together>=4:
            return True

        # other diagonal
        together=1
        if col>0:
            i=1
            while((i<=col and row+i<=5) and self.board[row+i][col-i]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while((col+i<=4 and i<=row) and self.board[row-i][col+i]==player):
                together+=1
                i+=1
        if together>=4:
            return True

        # horizontal
        together=1
        if col>0:
            i=1
            while(i<=col and self.board[row][col-i]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while(col+i<=4 and self.board[row][col+i]==player):
                together+=1
                i+=1
        if together>=4:
            return True

        # vertical
        together=1
        if row >=3:
            i=1
            while(row+i<=5 and self.board[row+i][col]==player):
                together+=1
                i+=1
        if together==4:
            return True
        
        return False

def encoder(decState):
    encState = ""
    for i in range(6):
        for j in range(5):
            encState+=str(decState[i][j])
    return encState

def decoder(encState):
    decState = [0,0,0,0,0] * 6
    for i in range(30):
        decState[int(i/5)][i%5] = int(encState[i])
    return decState

# MCTSNode
class MCTSNode:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.plays = 0
        self.wins = 0

# MCTS
# TODO: has to be a recursive function
class MCTS:
    def __init__(self, turn):
        self.turn = turn
        self.root = MCTSNode("000000000000000000000000000000")

    def playout(state):
        temp = Connect4Board()
        temp.board = state

        return 1
    
    def player(self, currnode):
        # start from root
        if len(currnode.children)==0:
            return self.playout(currnode.state)

        # check maxim value for each child node iteratively
        maxnode = currnode.children[0]
        for node in currnode.children:
            # if any node is not visited before that is next node
            if node.plays==0:
                maxnode = node
                break
            # else next node is the node that maximizes the value that we want maximized
            elif node.wins/node.plays > maxnode.wins/maxnode.plays: 
                maxnode = node
        
        win = self.player(maxnode)
        if win==1:
            currnode.wins+=1
        currnode.plays+=1
        return win
        
    # while curr node is not a leaf node

# Q-learning
class Qlearning:

    def __init__(self, turn):
        self.turn = turn
    # TODO: change code to accept string states
    def player():
        qtable = {"000000000000000000000000000000": [1,1,1,1,1]}
        # start from whatever state given to you
        # state will not exist so make a new row with all q values at 1
        currstate = "000000000000000000000000000000"
        gboard = Connect4Board()
        while True:
            # choose a state either exploit or explore
            prob = randint(0,9)
            newact=0
            if prob==1:
                newact = randint(0,4)
            else:
                newact = qtable[currstate].index(max(qtable[currstate]))

            # newstate = self.encoder()
            gboard.move(newact, 2)
            newstate = encoder(gboard.board)

            # if state to new action doesn't exist make a new row, assign all q value in row to 1
            if newstate not in qtable:
                qtable[newstate] = [1,1,1,1,1]
            # else:
                # qtable[currstate][newact] += lr * (reward + gamma * nmax(qtable[newstate]) — qtable[currstate][newact])
            
            # if state is terminal:
                # break