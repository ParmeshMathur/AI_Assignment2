from _typeshed import Self
import numpy as np

# GAME
class Connect4Board:
    numrows = 5
    numcols = 4

    def __init__(self):
        self.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.highest = [0,0,0,0,0]
    
    def move(self, col, player):
        if self.board[col][self.highest[col]]==5:
            return 1
        else:
            self.board[col][(self.highest)[col]]=player
            self.highest[col]+=1
    
    def isWin(self, col, player):
        row = self.highest[col]

        # principal diag
        together=1
        if col>1:
            i=1
            while((i<=col and row+i<= 5) and self.board[col-i][row+i]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while((col+i<=4 and i<=row) and self.board[col+i][row-i]==player):
                together+=1
                i+=1
        if together==4:
            return True

        # other diagonal
        together=1
        if col>1:
            i=1
            while((i<=col and row+i<= 5) and self.board[col-i][row-i]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while((col+1<=4 and i<=row) and self.board[col+i][row+i]==player):
                together+=1
                i+=1
        if together==4:
            return True

        # horizontal
        together=1
        if col>1:
            i=1
            while(i<=col and self.board[col-i][row]==player):
                together+=1
                i+=1
        if col<4:
            i=1
            while(col+1<=4 and self.board[col+i][row]==player):
                together+=1
                i+=1
        if together==4:
            return True

        # vertical
        together=1
        if row >=3:
            i=1
            while(i<=row and self.board[col][row-i]==player):
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
