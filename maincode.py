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

# MCTS
# start from root
# check maxim value for each child node iteratively
    # if any node is not visited before that is next node
    # else next node is the node that maximizes the value that we want maximized
# while curr node is not a leaf node


# Q-learning
qtable = {"000000000000000000000000000000": [1,1,1,1,1]}
# start from whatever state given to you
# state will not exist so make a new row with all q values at 5
currstate = "000000000000000000000000000000"
while True:
    # choose a state either exploit or explore
    prob = randint(0,10)
    newact=0
    if prob==1:
        newact = randint(0,5)
    else:
        newact = qtable[currstate].index(max(qtable[currstate]))

    # newstate = 

    # if state to new action doesn't exist make a new row, assign all q value in row to 5
    # Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])
# till state is terminal