#The structure has an array with which it has a state, the next move

class game():

    def term(self,state,p):
        if ((state[0] == state[1] == state[2])
            or (state[3] == state[4] == state[5] == p)
            or (state[6] == state[7] == state[8] == p)
            or (state[0] == state[3] == state[6] == p)
            or (state[1] == state[4] == state[7] == p)
            or (state[2] == state[5] == state[8] == p)
            or (state[0] == state[4] == state[8] == p)
            or (state[2] == state[4] == state[6] == p)):
            return True
        return False

    def blanks(self,state):
        blank=[]
        for b in state:
            if b != "X" and b != "O":
                blank.append(b)
        return blank

    def utility(self,state):
        if self.term(state,"X"):
            return 1
        elif self.term(state,"O"):
            return -1
        elif len(self.blanks(state)) == 0:
            return 0
        else:
            return None


    def minimax(self,board,p):
        currentblanks = self.blanks(board)
        if self.term(board,"X"):
            return 1
        elif self.term(board,"O"):
            return -1
        elif (len(currentblanks) ==0):
            return 0

        currentmoves = []
        for i in currentblanks:
            board[i] = p
            if p == "X":
                result = self.minimax(board,"O")
            else:
                result = self.minimax(board,"X")
            board[i] = i
            currentmoves.append((i,result))

        bmove = -1
        if p == "X":
            bscore = -1000
            for i in range(0,len(currentmoves)):
                if currentmoves[i][1] > bscore:
                    bscore = currentmoves[i][1]
                    bmove = i
        else:
            bscore = 1000
            for i in range(0,len(currentmoves)):
                if currentmoves[i][1] < bscore:
                    bscore = currentmoves[i][1]
                    bmove = i
        print "Move for: %s"%p
        print currentmoves
        return currentmoves[bmove][1]



if __name__ == '__main__':
    newgame = game()
    board_state =   (["O","O","X","X",4,"O",6,7,"X"]) #Question d, consistent with the tree in the assignment also show utility as 1 for question e
    print board_state
    print newgame.minimax(board_state,"X")
    #board_state =   [i for i in range (0,9)] #Intial state
    #board_state =   ([0,1,2,3,4,5,6,7,"X"]) # question e, draw
    #print board_state
    #print newgame.minimax(board_state,"O")
    #board_state =   (["O",1,2,3,4,5,6,7,"X"]) # question e, Max
    #print board_state
    #print newgame.minimax(board_state,"X")
    #board_state =   (["O",1,2,"X",4,5,6,7,"X"]) # question e, draw
    #print board_state
    #print newgame.minimax(board_state,"O")
    #board_state =   (["O","O",2,"X",4,5,6,7,"X"]) # question e, max
    #print board_state
    #print newgame.minimax(board_state,"X")
    #board_state =   (["O","O","X","X",4,5,6,7,"X"]) # question e, max
    #print board_state
    #print newgame.minimax(board_state,"O")
    #board_state =   (["O","O","X","X",4,5,6,7,"X"]) # question e, none utility
    #print board_state
    #print newgame.utility(board_state)
