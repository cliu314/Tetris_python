grid_bg = "Images/grid.png"
white_bg = "Images/white-bg.jpg"
black_b = 'Images/black.jpg'
black_b2 = 'images/black2.jpg'

i = 'Images/I_piece.png'
j = 'Images/J_piece.png'
l = 'Images/L_piece.png'
o = 'Images/O_piece.png'
s = 'Images/S_piece.png'
t = 'Images/T_piece.png'
z = 'Images/Z_piece.png'

import pygame, sys, math
import random
import copy

from pygame import *

# RGB Color definitions

black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

"""" *** """

PIX_X = 30
PIX_Y = 30
ROW = 20
COL = 10

colorI = (0, 255, 255) #light blue, 1
colorO = (255, 215, 0) #yellow, 2
colorJ = (0, 0, 255) #blue, 3
colorL = (255, 140, 0) #orange, 4
colorS = (0, 255, 0) #green, 5
colorZ = (255, 0, 0) #red, 6
colorT = (150, 110, 220) #purple, 7

""" *** """

def getRowTopLoc(rowNum, height = PIX_Y):
    pixRow = 10 + (rowNum * height)
    return pixRow

def getColLeftLoc(colNum, width = PIX_X):
    pixCol = 10 + (colNum * width)
    return pixCol

def drawGrid(screen):
    for row in range(ROW+1):
        pixRow = getRowTopLoc(row)
        pygame.display.update(pygame.draw.line(screen, black, (10, 10 + row * PIX_Y), (10 + PIX_X *COL, 10 + PIX_Y * row), 1))   
    for col in range(COL+1):
        pixCol = getColLeftLoc(col)
        pygame.display.update(pygame.draw.line(screen, black, (10 + PIX_X* col, 10), (10+PIX_X*col,10 + PIX_Y * ROW), 1))

def makePiece():
    nextPiece = random.randint(1, 7)
    if nextPiece == 1:
        p = Piece('I', colorI)
    elif nextPiece == 2:
        p = Piece('O', colorO)
    elif nextPiece == 3:
        p = Piece('J', colorJ)
    elif nextPiece == 4:
        p = Piece('L', colorL)
    elif nextPiece == 5:
        p = Piece('S', colorS)
    elif nextPiece == 6:
        p = Piece('Z', colorZ)
    else:
        p = Piece('T', colorT)
    return p
        
def displayNextPiece(piece, screen):
    i_piece = pygame.image.load(i).convert_alpha()
    j_piece = pygame.image.load(j).convert_alpha()
    l_piece = pygame.image.load(l).convert_alpha()
    o_piece = pygame.image.load(o).convert_alpha()
    s_piece = pygame.image.load(s).convert_alpha()
    t_piece = pygame.image.load(t).convert_alpha()
    z_piece = pygame.image.load(z).convert_alpha()
    black_bg = pygame.image.load(black_b).convert()
    screen.blit(black_bg, (400, 100))
    
    if piece.getType() == 'I':
        screen.blit(i_piece, (400, 100))
    elif piece.getType() == 'J':
        screen.blit(j_piece, (400, 100))
    elif piece.getType() == 'L':
        screen.blit(l_piece, (400, 100))
    elif piece.getType() == 'O':
        screen.blit(o_piece, (400, 100))
    elif piece.getType() == 'S':
        screen.blit(s_piece, (400, 100))
    elif piece.getType() == 'T':
        screen.blit(t_piece, (400, 100))
    elif piece.getType() == 'Z':
        screen.blit(z_piece, (400, 100))
    pygame.display.update()

#-----------------------------------------------------------------------------------
def newGame(): # starts game
    pygame.init()
    window_size = [ROW * PIX_X + 20, COL * PIX_Y + 350] # width, height
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Tetris") # caption sets title of Window 
    board = Board(ROW, COL)              # makes Board object
    moveCount = 0
    linesCleared = 0
    clock = pygame.time.Clock()
    mainLoop(screen, board, moveCount, linesCleared, clock, False)


""" ***Main Loop*** """
def mainLoop(screen, board, moveCount, linesCleared, clock, stop):
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    gamefont = pygame.font.Font(None, 30)
    timefont = pygame.font.Font(None, 80)
    buttons = pygame.sprite.RenderPlain()
    quit_button = Button('quit_button.png')
    quit_button.setCoords(400,400)
    restart_button = Button('restart_button.png')
    restart_button.setCoords(400,500)
    buttons.add(quit_button)
    buttons.add(restart_button)
    buttons.draw(screen)
    restart = False
    
    black_bg = pygame.image.load(black_b).convert()
    board.cells.draw(screen) #draw Sprites (cells)
    drawGrid(screen)        #draw grid
    pygame.display.flip()   #update screen
    currentPiece = makePiece()
    nextPiece = makePiece()
    
    linestext = gamefont.render('Lines Cleared: 0', 1, [255, 255, 255])
    screen.blit(linestext, (400, 300))
    pygame.display.update()
    
    if stop == True:
        pygame.quit()
        sys.exit()
    
    while stop == False:
        if board.gameLost():
            print "GAME OVER"
            pygame.mixer.music.stop()
            pygame.mixer.music.load('lose.mp3')
            pygame.mixer.music.play()
            return
        
        displayNextPiece(nextPiece, screen)
        text = gamefont.render('NEXT PIECE', 1, [255, 255, 255])
        screen.blit(black_bg, (400, 30))
        screen.blit(text, (400, 70))
        pygame.display.update()

        board.nonOverlap = []
        board.placePiece(currentPiece)  #places Piece on the board
        board.cells.draw(screen)
        moveCount = moveCount + 1   #increments moveCount
        dirty_locs = []
        for c in board.updatedCellsReal:
            screen.blit(c.getImage(), c.getPixLoc())
            dirty_locs.append(c.rect)
        pygame.display.update(dirty_locs)
        drawGrid(screen)
        clock.tick(5)

        board.setMovingPiece(currentPiece)
        currentPiece = nextPiece
        nextPiece = makePiece()
 
        while(board.getMovingPiece().isValid(board)):
            sec = pygame.time.get_ticks()/1000 #yay integer division!
            if sec < 10:
                time = "00: 0" + str(sec)
            elif 10 <= sec <=50:
                time = "00: " + str(sec)
            else: #sec >=60
                min = sec/60 #integer division ot the rescue again!
                newsec = sec - min*60
                if newsec < 10:
                    time = "0" + str(min) + ": 0" + str(newsec)
                else:
                    time = "0" + str(min) + ":" + str(newsec)
                
            time_text = timefont.render(time, 1, [255, 255, 255])
            black_bg2 = pygame.image.load(black_b2).convert()
            screen.blit(black_bg2, (370, 225))
            screen.blit(time_text, (400, 225))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #user clicks close
                    stop = True
                    pygame.quit()
                    sys.exit()
                key_press = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    quit_button.pressed(mouse)
                    restart = restart_button.pressed(mouse)
                    if restart == True:
                        newGame()
                        break

                if event.type == pygame.KEYDOWN:                    
                    if event.key == pygame.K_LEFT: # left key 
                        board.moveLeft()
                    elif event.key == pygame.K_RIGHT: # right key
                        board.moveRight()
                    elif event.key == pygame.K_UP:
                        board.rotatePiece()
                    elif event.key == pygame.K_DOWN:
                        board.moveDown()
##                    elif event.key == pygame.K_SPACE:
##                        board.hardDrop()
                    key_press = True

                if key_press == True:
                    dirty_locs = []
                    for c in board.updatedCellsReal:
                        screen.blit(c.getImage(), c.getPixLoc())
                        dirty_locs.append(c.rect)
                    pygame.display.update(dirty_locs)
                    board.cells.draw(screen)
                    drawGrid(screen)
                    
                    clock.tick(5)
            
            board.playPiece()  # simulate gravity by dropping piece down at a steady rate
            dirty_locs = []
            for c in board.updatedCellsReal:
                screen.blit(c.getImage(), c.getPixLoc())
                dirty_locs.append(c.rect)
            pygame.display.update(dirty_locs)
            board.cells.draw(screen)
            drawGrid(screen)           
            clock.tick(5)
            board.clearCells()
  
        for r in range(ROW):   #Checks if a row has been filled
                if board.rowFilled(r):
                    board.clear(r)
                    linesCleared = linesCleared + 1
                    black_bg2 = pygame.image.load(black_b2).convert()
                    screen.blit(black_bg2, (400, 300))
                    linestext = gamefont.render('Lines Cleared: ' + str(linesCleared), 1, [255, 255, 255])
                    screen.blit(linestext, (400, 300))
                    
                    pygame.display.update()
                    dirty_locs = []
                    for c in board.updatedCellsReal:
                        screen.blit(c.getImage(), c.getPixLoc())
                        dirty_locs.append(c.rect)
                    pygame.display.update(dirty_locs)
                    board.cells.draw(screen)
                    drawGrid(screen)
                    clock.tick(5)
                    
                    
#----------BUTTON CLASS----------
        
class Button(pygame.sprite.Sprite):
    def __init__(self, button_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(button_type).convert_alpha()
        self.rect = self.image.get_rect()
        self.type = button_type
        
    def pressed(self, mouse):
        if self.type == 'quit_button.png':
            if((mouse[0] >= 400) and (mouse[0] <=520) and (mouse[1] >= 400) and (mouse[1] <= 457)):
                print 'quit'
                pygame.quit()
                sys.exit()  
        if self.type == 'restart_button.png':
            if((mouse[0]>=400) and (mouse[0]<=520) and (mouse[1]>=500) and (mouse[1]<=555)):
                print 'restart'
                return True
            
    def setCoords(self, x, y):
        self.rect.topleft = x,y
        
#----------CELL CLASS----------

class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([PIX_X, PIX_Y])
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = getColLeftLoc(col)
        self.rect.y = getRowTopLoc(row)
        self.color = color
        self.image.fill(color)      
            
    def getLocation(self):
        return (self.row, self.col)

    def getImage(self):
        return self.image

    def getPixLoc(self):
        return (self.rect.x, self.rect.y)
    
    def getColor(self):
        return self.color
    
    def changeColor(self, color):
        self.color = color
        self.image.fill(color)
        if color == white:
            self.occupied = False
        else:
            self.occupied = True
    
    def setRow(self, row):
        self.row = row
        
    def setCol(self, col):
        self.col = col
        
    def isOccupied(self):   #returns True if cell is occupied
        if self.color == white:
            return False
        else:
            return True

#----------BOARD CLASS----------

class Board:
    def __init__(self, row, col):
        self.row = ROW
        self.col = COL
        self.cells = pygame.sprite.RenderPlain()
        self.updatedCells = pygame.sprite.RenderPlain()
        self.updatedCellsReal = []
        self.createBoard() # creates a row x col board filled with Cells
        self.movingPiece = None
        self.nonOverlap = []
        self.gameOverRowNum = 50

    def createBoard(self):        
        self.boardCells = {}
        for row in range(self.row):
            for col in range(self.col):
                c = Cell(row, col, white)
                self.boardCells[(row, col)] = c
                self.cells.add(c) 

    def clearCells(self):
        self.updatedCellsReal = []
    
    def restart(self):
        self.cells = pygame.sprite.RenderPlain()
        self.updatedCells = pygame.sprite.RenderPlain()
        self.updatedCellsReal = []
        self.createBoard() # creates a row x col board filled with Cells
        self.movingPiece = None
        self.nonOverlap = []
        self.gameOverRowNum = 50        
        self.createBoard()
        
    def getCell(self, row, col):
        return self.boardCells[(row,col)]
    
    def placePiece(self, piece):
        cell_locs = piece.getLocation()
        for loc in cell_locs:
            c = self.boardCells[loc]
            c.changeColor(piece.getColor())
            self.updatedCellsReal.append(c)

    def setMovingPiece(self, piece):
        self.movingPiece = piece

    def getMovingPiece(self):
        return self.movingPiece

    def findNonOverlap(self, loc_old, loc_new):
        for loc in copy.deepcopy(loc_old):
            if loc in loc_new:
                loc_old.pop(loc_old.index(loc))
                loc_new.pop(loc_new.index(loc))
        self.nonOverlap = loc_new

    def playPiece(self):
        old_locs = self.movingPiece.getLocation() #return list of tuples current location of the piece
        self.movingPiece.softDrop()               #calls softDrop, which shifts the piece down one row
        new_locs = self.movingPiece.getLocation() # return list of tuples of new location of the piece
        self.findNonOverlap(old_locs, new_locs)
        
        for loc2 in old_locs:                 #changes the color of the previous position of the piece so that it is white
            c = self.boardCells[loc2]
            c.changeColor(white)
            self.updatedCellsReal.append(c)
        for loc in new_locs:               #changes the color of the newly occupied cells
            c = self.boardCells[loc]
            c.changeColor(self.movingPiece.getColor())
            self.updatedCellsReal.append(c)

    def rotatePiece(self):
        old_locs = self.movingPiece.getLocation() #return list of tuples current location of the piece
        self.movingPiece.rotate()
        new_locs = self.movingPiece.getLocation() # return list of tuples of new location of the piece
        self.findNonOverlap(old_locs, new_locs)
        
        for loc2 in old_locs:                 #changes the color of the previous position of the piece so that it is white
            c = self.boardCells[loc2]
            c.changeColor(white)
            self.updatedCellsReal.append(c)
        for loc in new_locs:               #changes the color of the newly occupied cells
            c = self.boardCells[loc]
            c.changeColor(self.movingPiece.getColor())
            self.updatedCellsReal.append(c)

    def moveLeft(self):
        old_locs = self.movingPiece.getLocation() #return list of tuples current location of the piece
        self.movingPiece.shiftLeft()
        new_locs = self.movingPiece.getLocation() # return list of tuples of new location of the piece
        self.findNonOverlap(old_locs, new_locs)
        
        for loc2 in old_locs:                 #changes the color of the previous position of the piece so that it is white
            c = self.boardCells[loc2]
            c.changeColor(white)
            self.updatedCellsReal.append(c)
        for loc in new_locs:               #changes the color of the newly occupied cells
            c = self.boardCells[loc]
            c.changeColor(self.movingPiece.getColor())
            self.updatedCellsReal.append(c)
            
    def moveRight(self):
        old_locs = self.movingPiece.getLocation() #return list of tuples current location of the piece
        self.movingPiece.shiftRight()
        new_locs = self.movingPiece.getLocation() # return list of tuples of new location of the piece
        self.findNonOverlap(old_locs, new_locs)
        
        for loc2 in old_locs:                 #changes the color of the previous position of the piece so that it is white
            c = self.boardCells[loc2]
            c.changeColor(white)
            self.updatedCellsReal.append(c)
        for loc in new_locs:               #changes the color of the newly occupied cells
            c = self.boardCells[loc]
            c.changeColor(self.movingPiece.getColor())
            self.updatedCellsReal.append(c)
            
    def moveDown(self):
        old_locs = self.movingPiece.getLocation() #return list of tuples current location of the piece
        if(self.movingPiece.isValid(self)):
            self.movingPiece.softDrop()               #calls softDrop, which shifts the piece down one row
            new_locs = self.movingPiece.getLocation() # return list of tuples of new location of the piece
            self.findNonOverlap(old_locs, new_locs)
            
            for loc2 in old_locs:                 #changes the color of the previous position of the piece so that it is white
                c = self.boardCells[loc2]
                c.changeColor(white)
                self.updatedCellsReal.append(c)
            for loc in new_locs:               #changes the color of the newly occupied cells
                c = self.boardCells[loc]
                c.changeColor(self.movingPiece.getColor())
                self.updatedCellsReal.append(c)

    def hardDrop(self):
        pass
    
    def findTopRow(self, cells):
        top_row = 50
        for c in cells:
            if c.row < top_row:
                top_row = c.row
        return top_row
            
    def rowFilled(self, rownum): #checks if there are rows that are filled; returns True or False
        for c in range(COL):
            if self.boardCells[(rownum,c)].isOccupied() == False: #one of the Cells is not occupied
                return False                                # returns False --> row NOT filled
        return True
    
    def clear(self, rownum): #clears a row if it is filled by shifting all the cells above it down one
        sound = pygame.mixer.Sound('clear.ogg')
        sound.play()
        for r in range(0, rownum-1):
            for c in range(COL):
                self.boardCells[(rownum-r,c)].changeColor(self.boardCells[(rownum-r-1,c)].getColor())
                perm = copy.copy(self.boardCells[(rownum-r,c)])
                self.updatedCellsReal.append(perm)
    
    
    
    def gameLost(self): #checks if game is lost; returns True or False
        if self.gameOverRowNum <= 2:
            return True
        else:
            return False


#----------PIECE CLASS----------

class Piece(pygame.sprite.Sprite):
    def __init__(self, piecetype, color): #piece is the name of the piece
        pygame.sprite.Sprite.__init__(self)
        self.cells = []
        self.color = color
        self.piecetype = piecetype
        self.rotation = 0     #keeps track of how much the piece is rotated from its original position
        self.makeCells()

    def getColor(self):
        return self.color

    def getType(self):
        return self.piecetype

    def makeCells(self):
        if self.piecetype == 'I':      
            c1 = Cell(1, 3, self.color)
            c2 = Cell(1, 4, self.color)
            c3 = Cell(1, 5, self.color)
            c4 = Cell(1, 6, self.color)
        elif self.piecetype == 'O':
            c1 = Cell(1, 4, self.color)
            c2 = Cell(1, 5, self.color)
            c3 = Cell(2, 4, self.color)
            c4 = Cell(2, 5, self.color)
        elif self.piecetype == 'J':
            c1 = Cell(1, 3, self.color)
            c2 = Cell(1, 4, self.color)
            c3 = Cell(1, 5, self.color)
            c4 = Cell(2, 5, self.color)    
        elif self.piecetype == 'L':
            c1 = Cell(1, 3, self.color)
            c2 = Cell(1, 4, self.color)
            c3 = Cell(1, 5, self.color)
            c4 = Cell(2, 3, self.color)
        elif self.piecetype == 'S':
            c1 = Cell(1, 5, self.color)
            c2 = Cell(1, 4, self.color)
            c3 = Cell(2, 4, self.color)
            c4 = Cell(2, 3, self.color)
        elif self.piecetype == 'Z':
            c1 = Cell(1, 3, self.color)
            c2 = Cell(1, 4, self.color)
            c3 = Cell(2, 4, self.color)
            c4 = Cell(2, 5, self.color)
        else:    #self.piecetype = T
            c1 = Cell(1, 4, self.color)
            c2 = Cell(2, 3, self.color)
            c3 = Cell(2, 4, self.color)
            c4 = Cell(2, 5, self.color)

        self.cells = [c1, c2, c3, c4]

    def rotate(self):  #rotates the piece 90 degrees clockwise
        c1 = self.cells[0]
        c2 = self.cells[1]
        c3 = self.cells[2]
        c4 = self.cells[3]
        
        c1_copy = copy.copy(c1)
        c2_copy = copy.copy(c2)
        c3_copy = copy.copy(c3)
        c4_copy = copy.copy(c4)
        
        if self.piecetype == 'I':
            if self.rotation == 0:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col -= 1
                c4.row += 2
                c4.col -= 2
            elif self.rotation == 1:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col += 1
                c4.row -= 2
                c4.col += 2
            elif self.rotation == 2:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col -= 1
                c4.row += 2
                c4.col -= 2
            elif self.rotation == 3:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col += 1
                c4.row -= 2
                c4.col += 2
                
        elif self.piecetype == 'J':
            if self.rotation == 0:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col -= 1
                c4.row += 0
                c4.col -= 2
            elif self.rotation == 1:
                c1.row += 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col -= 1
                c4.row -= 2
                c4.col += 0
            elif self.rotation == 2:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col -= 0
                c3.row -= 1
                c3.col += 1
                c4.row += 0
                c4.col += 2
            elif self.rotation == 3:
                c1.row -= 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col += 1
                c4.row += 0
                c4.row += 2
        elif self.piecetype == 'L':
            if self.rotation == 0:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col -= 1
                c4.row -= 2
                c4.col += 0
            elif self.rotation == 1:
                c1.row += 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col -= 1
                c4.row +=0
                c4.col += 2
            elif self.rotation == 2:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col += 1
                c4.row += 2
                c4.col += 0
            elif self.rotation == 3:
                c1.row -= 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col += 1
                c4.row += 0
                c4.col -= 2
        elif self.piecetype == 'O':
            if self.rotation == 0:
                c1.row += 0
                c1.col += 0
                c2.row += 0
                c2.col += 0
                c3.row += 0
                c3.col += 0
                c4.row += 0
                c4.col += 0
            elif self.rotation == 1:
                c1.row += 0
                c1.col += 0
                c2.row += 0
                c2.col += 0
                c3.row += 0
                c3.col += 0
                c4.row += 0
                c4.col += 0
            elif self.rotation == 2:
                c1.row += 0
                c1.col += 0
                c2.row += 0
                c2.col += 0
                c3.row += 0
                c3.col += 0
                c4.row += 0
                c4.col += 0
            elif self.rotation == 3:
                c1.row += 0
                c1.col += 0
                c2.row += 0
                c2.col += 0
                c3.row += 0
                c3.col += 0
                c4.row += 0
                c4.col += 0
        elif self.piecetype == 'S':
            if self.rotation == 0:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col -= 1
                c4.row -= 2
                c4.col += 0
            elif self.rotation == 1:
                c1.row -= 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col += 1
                c4.row += 0
                c4.col += 2
            elif self.rotation == 2:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col += 1
                c4.row += 2
                c4.col += 0
            elif self.rotation == 3:
                c1.row += 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col -= 1
                c4.row += 0
                c4.col -= 2
        elif self.piecetype == 'T':
            if self.rotation == 0:
                c1.row += 1
                c1.col += 1
                c2.row -= 1
                c2.col += 1
                c3.row -= 0
                c3.col += 0
                c4.row += 1
                c4.col -= 1
            elif self.rotation == 1:
                c1.row += 1
                c1.col -= 1
                c2.row += 1
                c2.col += 1
                c3.row += 0
                c3.col += 0
                c4.row -= 1
                c4.col -= 1
            elif self.rotation == 2:
                c1.row -= 1
                c1.col -= 1
                c2.row += 1
                c2.col -= 1
                c3.row += 0
                c3.col -= 0
                c4.row -= 1
                c4.col += 1
            elif self.rotation == 3:
                c1.row -= 1
                c1.col += 1
                c2.row -= 1
                c2.col -= 1
                c3.row -= 0
                c3.col -= 0
                c4.row += 1
                c4.col += 1
        elif self.piecetype == 'Z':
            if self.rotation == 0:
                c1.row -= 1
                c1.col += 1
                c2.row += 0
                c2.col += 0
                c3.row -= 1
                c3.col -= 1
                c4.row += 0
                c4.col -= 2
            elif self.rotation == 1:
                c1.row += 1
                c1.col += 1
                c2.row += 0
                c2.col -= 0
                c3.row -= 1
                c3.col += 1
                c4.row -= 2
                c4.col -= 0
            elif self.rotation == 2:
                c1.row += 1
                c1.col -= 1
                c2.row += 0
                c2.col += 0
                c3.row += 1
                c3.col += 1
                c4.row += 0
                c4.col += 2
            elif self.rotation == 3:
                c1.row -= 1
                c1.col -= 1
                c2.row -= 0
                c2.col -= 0
                c3.row += 1
                c3.col -= 1
                c4.row += 2
                c4.col += 0
        # if the rotation causes the piece to go out the board, then don't rotate the piece
        if((c1.row<0) or (c1.row>=ROW) or (c1.col<0) or (c1.col>=COL) or (c2.row<0) or (c2.row>=20) or (c2.col<0) or (c2.col>=COL) or (c3.row<0) or (c3.row>=ROW) or (c3.col<0) or (c3.col>=COL) or (c4.row<0) or (c4.row>=ROW) or (c4.col<0) or (c4.col>=COL)):
            self.cells = [c1_copy, c2_copy, c3_copy, c4_copy]
        else:
            if self.rotation == 3:
                self.rotation = 0
            else:
                self.rotation += 1
                self.cells = [c1, c2, c3, c4]

    def isValid(self, board): #checks if piece can still move
        for c in self.cells:
            if c.row >= (20-1):
                return False
            
        newlocs = board.nonOverlap
        if len(newlocs)>0:
            for loc in newlocs:
                downloc = (loc[0] + 1, loc[1])
                if board.boardCells[downloc].isOccupied():
                    top_row = board.findTopRow(self.cells)
                    if top_row < board.gameOverRowNum:
                        board.gameOverRowNum = top_row
                    return False
        return True
    
    def shiftRight(self): #moves the piece to the right
        if((self.cells[0].col < (COL-1)) and (self.cells[1].col < (COL-1)) and (self.cells[2].col < (COL-1)) and (self.cells[3].col < (COL-1))):
            self.cells[0].col += 1
            self.cells[1].col += 1
            self.cells[2].col += 1
            self.cells[3].col += 1

    def shiftLeft(self): #moves the piece to the left
        if((self.cells[0].col > 0) and (self.cells[1].col > 0) and (self.cells[2].col > 0) and (self.cells[3].col > 0)):
            self.cells[0].col -= 1
            self.cells[1].col -= 1
            self.cells[2].col -= 1
            self.cells[3].col -= 1 

    def softDrop(self): #increases the speed in which the piece falls downward
        self.cells[0].row += 1
        self.cells[1].row += 1
        self.cells[2].row += 1
        self.cells[3].row += 1
        
    def hardDrop(self): #drops the piece to the very lowest it can go
        pass

    def getLocation(self): # returns list with tuples indicating location of each cell in the piece
        loc_list = []
        for c in self.cells:
            loc = c.getLocation()
            loc_list.append(loc)
        return loc_list

    def hold(self): #puts the piece on hold
        pass
    
    
newGame()
                  
    
