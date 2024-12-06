import tkinter as tk
import random

# board class
class Board:
    # init function
    def __init__(self, root, size=8):
        # canvas
        self.size = size
        self.canvas = tk.Canvas(root, width=size*50, height=size*50)
        self.canvas.pack()

        # track current piece and player
        self.current_piece = None
        self.current_player = "blue"
        self.highlighted = []
        self.blue_score = 0
        self.red_score = 0

        # draw grid
        self.grid = [[None for _ in range(size)] for _ in range(size)]  
        self.status = tk.Label(root, text="")
        self.status.pack()
        self.score = tk.Label(root, text="Blue: 0 | Red: 0")
        self.score.pack()

        # initialize board and mouse input
        self.initializeBoard()
        self.canvas.bind("<Button-1>", self.click)

    def initializeBoard(self):
        # draw board
        for row in range(self.size):
            for col in range(self.size):
                # create checkered pattern
                if (row + col) % 2 == 0:
                    color = 'white'
                else:
                    color = 'gray'
                self.canvas.create_rectangle(col*50, row*50, (col+1)*50, (row+1)*50, fill=color)

        # create pieces
        for row in range(4):
            for col in range(4-row):
                self.addPiece(row, col, 'blue')
                self.addPiece(self.size - 1- row, self.size - 1 - col, 'red')
    
    # function that creates and adds pieces to board
    def addPiece(self, row, col, color):
        piece = self.canvas.create_oval(col*50+10, row*50+10, col*50+40, row*50+40, fill=color)
        self.grid[row][col] = (piece, color)

    # function that handles when a piece is clicked
    def click(self, event):
        row = event.y // 50
        col = event.x // 50

        # check if piece is already on board
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.current_piece:
                if self.current_piece == (row, col):
                    # remove highlight
                    self.clearHighlights()
                    # remove piece from board
                    self.current_piece = None
                else:
                    # if current piece isn't at specific space, move it
                    self.move(row, col)
            else:
                # if not already selected, select piece
                self.selectPiece(row, col)

    # function that handles when a piece is selected
    def selectPiece(self, row, col):
        # define a piece on board
        piece = self.grid[row][col]

        # if piece exists and is where the current player is
        if piece and piece[1] == self.current_player:
            # set current piece and highliight it
            self.current_piece = (row, col)
            self.highlightMoves(row, col)

    # function that handles when a piece is highlighted
    def highlightMoves(self, row, col):
        # define the moves
        moves = self.generateMoves(row, col)

        # clear previous highlights
        self.clearHighlights()

        # for each move possible
        for move in moves:
            # highlight the move
            newrow, newcol = move
            select = self.canvas.create_rectangle(newcol*50, newrow*50, (newcol+1)*50, (newrow+1)*50, outline='green', width=5)
            # add to list of highlights
            self.highlighted.append(select)
    
    # function that generates all possible moves for a piece
    def generateMoves(self, row, col):
       moves = []
       # define all directions
       directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]

       # for each direction
       for dx, dy in directions:
           # calculate new position
           newRow = row + dx
           newCol = col + dy

           # if new position is on board and is empty
           if 0 <= newRow < self.size and 0 <= newCol < self.size and not self.grid[newRow][newCol]:
               # add move to list
               moves.append((newRow, newCol))

            # check for jumps
           jumpRow, jumpCol = row + 2*dx, col + 2*dy
            # if new position is within bounds
           if 0 <= jumpRow < self.size and 0 <= jumpCol < self.size:
               if self.grid[newRow][newCol] and not self.grid[jumpRow][jumpCol]:
                    # add new position to moves
                    moves.append((jumpRow, jumpCol))

       # return moves  
       return moves          
    
    # function that handles the movement of the pieces
    def move(self, row, col):
        # define current piece
        newRow, newCol = self.current_piece

        # if current move is in possible moves
        if(row, col) in self.generateMoves(newRow, newCol):
            # set new position of current piece
            piece, color = self.grid[newRow][newCol]
            # remove piece from old position
            self.grid[newRow][newCol] = None
            # add piece to new position
            self.grid[row][col] = (piece, color)
            # update current position
            self.canvas.move(piece, (col - newCol)*50, (row - newRow)*50)
            # clear previous highlights
            self.clearHighlights()
            # clear previous position
            self.current_piece = None

            # if a blue piece reaches opponent's starting zone
            if self.current_player == 'blue' and row >= self.size - 4:
                # increment blue score
                self.blue_score += 1
            # if a red piece reaches opponent's starting zone
            elif self.current_player == 'red' and row < 4:
                # increment red score
                self.red_score += 1

            # display scores
            self.score.config(text=f"Blue: {self.blue_score} | Red: {self.red_score}")

            # switch turns
            if(self.current_player == 'blue'):
                self.current_player = 'red'
            else:
                self.current_player = 'blue'
            
            if(self.current_player == 'red'):
                self.AI_makeMove()

        # if current move is not in possible moves
        else:
            # state that it is an illegal move
            self.status.config(text="Illegal Move")
            self.status.pack
            # adjust scores
            self.score.config(text=f"Blue: {self.blue_score} | Red: {self.red_score}")
    

    # function that clears highlighted spaces
    def clearHighlights(self):
        # loop through all spaces highlights
        for select in self.highlighted:
            # remove highlight from space
            self.canvas.delete(select)

        # initialize highlighted list to empty list
        self.highlighted = []

    def checkWinner(self):
        # create lists of locations that each player has pieces on
        blue_target = []
        red_target = []

        # define blue target areas
        for row in range(self.size - 4, self.size):
            for col in range(4 - (self.size - 1 - row)):
                blue_target.append((row, col))

        # define red target areas
        for row in range(4):
            for col in range(self.size - 1 - row, self.size):
                red_target.append((row, col))

        # check if most blue pieces are in red area
        blue_wins = True
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece[1] == "blue":
                    if (row, col) not in blue_target:
                        blue_wins = False
                        break
            if not blue_wins:
                break

        # check if most red pieces are in blue area
        red_wins = True
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece[1] == "red":
                    if (row, col) not in red_target:
                        red_wins = False
                        break
            if not red_wins:
                break

        # determine if blue is winner
        if blue_wins:
            return "Blue"
        # determine if red is winner
        elif red_wins:
            return "Red"
        # if no one has won, return none
        else:
            return None

    # functions that will help the AI player make a move 

    def AI_legalMoves(self, player):
        # initialize list of legal moves
        legal_moves = []
        # for each row and column in the grid
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] and self.grid[row][col][1] == player:
                    # generate legal moves for AI
                    AI_moves = self.generateMoves(row, col)
                    # add each move to legal moves
                    for move in AI_moves:
                        legal_moves.append((row, col, move))
        # return legal moves
        return legal_moves
    
    # function that generates temp moves so that AI can analyze each possibility
    def AI_tempMove(self, player):
        # define the player's move
        startRow, startCol, (endRow, endCol) = player
        # define the piece
        piece = self.grid[startRow][startCol]
        # remove current piece from board
        self.grid[startRow][startCol] = None
        # place piece at new position
        self.grid[endRow][endCol] = piece
    
    # function that undoes the temp move
    def AI_undoTemp(self, player):
        # define the player's move
        startRow, startCol, (endRow, endCol) = player
        # define the current piece that was just moved
        piece = self.grid[endRow][endCol]
        # remove current piece from board
        self.grid[endRow][endCol] = None
        # place piece at old position
        self.grid[startRow][startCol] = piece

    # function that makes the AI agent's move permanent
    def AI_permMove(self, player):
        # define the player's move
        startRow, startCol, (endRow, endCol) = player
        # set the player's piece current position
        self.current_piece = (startRow, startCol)
        # officially move the current piece
        self.move(endRow, endCol)

    # function that helps the AI agent make a move
    def AI_makeMove(self):
        # get legal moves for red pieces
        legal_red_moves = self.AI_legalMoves("red")
        # if no legal moves, skip red players turn
        if not legal_red_moves:
            return None
        # choose a move randomly from the list of legal moves
        move = random.choice(legal_red_moves)
        # define the move coordinates
        row, col, end = move
        # define destination of piece
        end_row, end_col = end
        # define the current piece
        self.current_piece = (row, col)
        # officially move the piece
        self.move(end_row, end_col)
        # erase old current piece
        self.current_piece = None

    # function that evaluates the goodness of the board
    def boardUtils(self, player, verbose=True):
        # initialize score to 0
        score = 0
        # if player is red
        if player == "red":
            # pieces are trying to get the first row
            target_row = 0
        # otherwise 
        else:
            # pieces are trying to get the last row
            target_row = self.size - 1
        # define flag that determines if pieces are moving
        advancing = False
        # loop through rows
        for row in range(self.size):
            # loop through columns
            for col in range(self.size):
                # determine where piece is on the board
                piece = self.grid[row][col]
                # if piece is on the board
                if piece and piece[1] == player:
                    # check distance  to goal
                    distance = abs(row - target_row)
                    #score -= h_score * 0.5
                    # lower the score by distance
                    # low score == good move
                    score -= distance
                    # set the advance flag to true
                    advancing = True
                    # print action if verbose is true
                    if verbose:
                        print(f"Piece at ({row}, {col}) has a score of {score} with distance {distance}")
        # if the piece hasn't moved
        if not advancing:
            # print statement that shows the player is not moving
            print(f"Red player is not advancing")
        # return the full score
        return score

    # function that implements the minmax algorithm
    def minimax(self, depth, max_player, player):
        # base case -> depth is 0 or game is over
        if depth == 0 or self.checkWinner():
            # return the board score
            return self.boardUtils(player)
        # find legal moves
        legal_moves = self.AI_legalMoves(player)
        # determine if max or min player
        if player == "blue":
            # blue is maxplayer
            enemy = "red"
        # otherwise
        else:
            # red is maxplayer
            enemy = "blue"
        # as long as maxplayer exists
        if max_player:
            # initialize best score (blue is definitely max)
            best_score = float('-inf')
            # for each move
            for move in legal_moves:
                # make temp move for checking
                self.AI_tempMove(move)
                # determine if best move
                score = self.minimax(depth - 1, False, enemy)
                # undo move
                self.AI_undoTemp(move)
                # calculate best score
                best_score = max(best_score, score)

        # otherwise red is max
        else:
            # initialize best score
            best_score = float('inf')
            # for each move
            for move in legal_moves:
                # make temp move for checking
                self.AI_tempMove(move)
                # determine if best move
                score = self.minimax(depth - 1, True, enemy)
                # undo move
                self.AI_undoTemp(move)
                # calculate best score according to the min
                best_score = min(best_score, score)

        # return ultimate best score
        return best_score

    # function that implements the alpha-beta pruning algorithm
    def alphaBeta(self, depth, alpha, beta, max_player, player):
        # base case:
        if depth == 0 or self.checkWinner():
            return self.boardUtils(player)
        
        # find legal moves
        legal_moves = self.AI_legalMoves(player)

        # determine if max or min player
        if player == "blue":
            # max player is blue
            enemy = "red"
        else:
            # red is maxplayer
            enemy = "blue"

        # if max player exists
        if max_player:
            # initialize best score
            best_score = float('-inf')
            #print(f"Evaluating move {move} for player {max_player}: score = {score}")
            # for each move
            for move in legal_moves:
                # make temp move for checking
                self.AI_tempMove(move)
                # determine if best move
                score = self.minimax(depth - 1, False, enemy)
                # undo move
                self.AI_undoTemp(move)
                # calculate best score according to the max
                best_score = max(best_score, score)
                # calculate the alpha
                alpha = max(alpha, best_score)
                # prune if beta <= alpha
                if beta <= alpha:
                    # break
                    break
        # otherwise red is max
        else:
            # initialize best score
            best_score = float('inf')
            #print(f"Evaluating move {move} for player {player}: score = {score}")
            # for each move
            for move in legal_moves:
                # make temp move for checking
                self.AI_tempMove(move)
                # determine if best move
                score = self.minimax(depth - 1, True, enemy)
                # undo move
                self.AI_undoTemp(move)
                # calculate best score according to the min
                best_score = min(best_score, score)
                # calculate the beta
                beta = min(beta, best_score)
                # prune if beta <= alpha
                if beta <= alpha:
                    # break
                    break
        # return utimate best score
        return best_score

    # function that uses the alpha-beta function to determine the best move ->-> call when switching turns
    def AI_chooseMove(self, player, depth=8, use_alpha_beta_pruning = True):
        # find legal moves
        legal_moves = self.AI_legalMoves(player)
        # initialize best move
        best_move = None
        # determine if max or min player
        if player == "blue":
            # max player
            best_score = float("-inf")
        else:
            # min player
            best_score = float("inf")
        
        # for each move
        for move in legal_moves:
            # make temp move
            self.AI_tempMove(move)
            # if alpha beta is being used
            if use_alpha_beta_pruning:
                # call alpha beta function
                score = self.alphaBeta(depth - 1, float("-inf"), float("inf"), player == "blue", player)
                print(f"Currently overpowering beta with my alpha: {score}")
            # otherwise
            else:
                # call minimax function
                score = self.minimax(depth - 1, player == "blue", player)
                print(f"Calling the minimax function.... {score}")
            # undo temp move
            self.AI_undoTemp(move)

            # determine blue best move and score
            if player == "blue" and score > best_score:
                best_score = score
                best_move = move
                # print results
                print(f"Blue best move: {best_move} and best score: {best_score}")
            # determine red best move and scores
            elif player == "red" and score < best_score:
                best_score = score
                best_move = move
                # print resultss
                print(f"Red best move: {best_move} and best score: {best_score}")

        # if the best move is possible
        if best_move is not None:
            # make the best move
            self.AI_permMove(best_move)

# game class
class Game:
    # init functionn
    def __init__(self):
        self.root = tk.Tk()
        self.board = Board(self.root)
        self.status = tk.Label(self.root, text="Blue's Turn")
        self.status.pack()

    # function that runs the game and checks status
    def run(self):
        self.checkStatus()           
        if self.board.current_player == "red":
            self.board.AI_chooseMove("red", depth=8, use_alpha_beta_pruning=True)
        self.root.mainloop()

    # function that checks the status of the game
    def checkStatus(self):
        # check if game is over
        winner = self.board.checkWinner()
        
        # if game is over
        if winner:
            # display winner
            self.status.config(text=f"{winner} wins!")
            self.board.canvas.unbind("<Button-1>")
        else:
            # otherwise, display which turn it is
            self.status.config(text=f"{self.board.current_player}'s Turn")
        # refresh status every 100 ms
        self.root.after(100, self.checkStatus)

# main function
if __name__ == "__main__":
    game = Game()
    game.run()