import tkinter as tk

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
        blue_wins = False
        for row, col in red_target:
            if (self.grid[row][col] and self.grid[row][col][1] == "blue"):
                blue_wins = True
                break

        # check if most red pieces are in blue area
        red_wins = False
        for row, col in blue_target:
            if (self.grid[row][col] and self.grid[row][col][1] == "red"):
                red_wins = True
                break  

        # determine if blue is winner
        if blue_wins:
            return "Blue"
        # determine if red is winner
        elif red_wins:
            return "Red"
        # if no one has won, return None
        else:
            return None

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