from random import random
import pygame, math, time

from pygame import mouse
pygame.init()
global Board, SCREENSIZE, screen, board_offset, size, BOARDSIZE
SCREENSIZE = (700,700)
screen = pygame.display.set_mode(SCREENSIZE)
size = 25
min_size = 15
max_size = 40

board_offset = [10,100]
WATER = "Water"
GRASS = "Grass"
MOUNTAIN = "Mountain"
Forest = "Forest"
BOARDSIZE = (9,9)
fontsize = 20
HELVETICA = pygame.font.SysFont('arial',fontsize)
mouse_select = (round(BOARDSIZE[0]/2),round(BOARDSIZE[1]/2))
global turn
turn = 1
WINNER = None

def toggleTurn():
    global turn
    if turn == 1: turn = 2
    elif turn == 2: turn = 1

def point_in_hex(point,base):
    m = [-1/math.sqrt(3),1/math.sqrt(3),'dne',-1/math.sqrt(3),1/math.sqrt(3),'dne']
    B = [base,(base[0]+size,base[1]-size/math.sqrt(3)),(base[0]+2*size,base[1]),(base[0]+2*size,base[1]+2*size/math.sqrt(3)),(base[0]+size,base[1]+3*size/math.sqrt(3)),(base[0],base[1]+2*size/math.sqrt(3))]
    b = []
    for a in range(6):
        if m[a] != 'dne':
            b.append(B[a][1]-m[a]*B[a][0])
        else:
            b.append(B[a][0])
    if point[1] >= point[0]*m[0]+b[0] and point[1] >= point[0]*m[1]+b[1] and point[0] <= b[2] and point[1] <= point[0]*m[3]+b[3] and point[1] <= point[0]*m[4]+b[4] and point[0] >= b[5]:
        return True
    else:
        return False

def Hex(base):
    point1 = base
    point2 = (base[0]+size,base[1]-size/math.sqrt(3))
    point3 = (base[0]+2*size,base[1])
    point4 = (base[0]+2*size,base[1]+2*size/math.sqrt(3))
    point5 = (base[0]+size,base[1]+3*size/math.sqrt(3))
    point6 = (base[0],base[1]+2*size/math.sqrt(3))
    return point1, point2, point3, point4, point5, point6
def getBase(x,y):
    base = (board_offset[0]+2*size*x,board_offset[1]+3*y*size/math.sqrt(3))
    if y%2 == 1: base = (base[0]-size,base[1])
    return base

def get_mouse():
    mouse_pos = pygame.mouse.get_pos()
    top = board_offset[1] - size/math.sqrt(3)
    yt = math.floor((mouse_pos[1] - top)/(3*size/math.sqrt(3)))
    if yt%2 == 0:
        xt = math.floor((mouse_pos[0] - board_offset[0])/(2*size))
    else:
        xt = math.floor((mouse_pos[0] - board_offset[0] + size)/(2*size))
    if yt < BOARDSIZE[1] and yt >= 0 and xt >= 0 and xt < BOARDSIZE[0]:
        base = getBase(xt,yt)
        if point_in_hex(mouse_pos,base): return (xt,yt)
        if yt-1 >= 0:
            base = getBase(xt,yt-1)
            if point_in_hex(mouse_pos,base): return (xt,yt-1)
            if xt-1 >= 0:
                base = getBase(xt-1,yt-1)
                if point_in_hex(mouse_pos,base): return (xt-1,yt-1)
            if xt+1 < BOARDSIZE[0]:
                base = getBase(xt+1,yt-1)
                if point_in_hex(mouse_pos,base): return (xt+1,yt-1)
    return False
def draw_border(space,color,borderSize=3):
    base = (board_offset[0]+2*size*space[0],board_offset[1]+3*space[1]*size/math.sqrt(3))
    if space[1]%2 == 1:
        base = (base[0]-size,base[1])
    pygame.draw.polygon(screen,color,Hex(base),borderSize)    
def step(space,direction):
    if space[1]%2 == 1:
        if direction == 0: return (space[0]-1,space[1]-1)
        if direction == 1: return (space[0],space[1]-1)
        if direction == 3: return (space[0],space[1]+1)
        if direction == 4: return (space[0]-1,space[1]+1)
    if space[1]%2 == 0:
        if direction == 0: return (space[0],space[1]-1)
        if direction == 1: return (space[0]+1,space[1]-1)
        if direction == 3: return (space[0]+1,space[1]+1)
        if direction == 4: return (space[0],space[1]+1)
    if direction == 2: return (space[0]+1,space[1])
    if direction == 5: return (space[0]-1,space[1])

menus = []
class Menu:
    def __init__(self,offset,dimensions,border=5,borderColor=(200,200,200),textColor=(80,200,170),margins=[],font=HELVETICA,content=[]):
        self.margins = margins
        self.textColor = textColor
        self.border = border
        self.borderColor = borderColor
        self.font = font
        self.content = content
        self.dimensions = dimensions
        self.offset = offset
        menus.append(self)
    def draw(self):
        pygame.draw.polygon(screen,(0,0,0),[self.offset,(self.offset[0]+self.dimensions[0],self.offset[1]),(self.offset[0]+self.dimensions[0],self.offset[1]+self.dimensions[1]),(self.offset[0],self.offset[1]+self.dimensions[1])])
        pygame.draw.polygon(screen,self.borderColor,[self.offset,(self.offset[0]+self.dimensions[0],self.offset[1]),(self.offset[0]+self.dimensions[0],self.offset[1]+self.dimensions[1]),(self.offset[0],self.offset[1]+self.dimensions[1])],self.border)

        for a in range(len(self.content)): #iterates each column in self.content
            for i in range(len(self.content[a])):   #iterates lines in each column
                line = self.font.render(self.content[a][i],True,self.textColor)
                screen.blit(line,(self.offset[0]+self.margins[a][i][0],self.offset[1]+self.margins[a][i][1]))
statsMenu = Menu([10,10],[140,200],content=[[None,None,None],[None,None,None]],margins=[[[3,3],[3,30],[3,60]],[[70,3],[70,30],[70,60]]])
movesMenu = Menu([10,SCREENSIZE[1]-200],[SCREENSIZE[0]-20,190], content=[[None,None,None,None]], margins=[[[3,3],[3,33],[3,63],[3,93]]])

class Space:
    def __init__(self,pos,type,item=None,effects=[None]):
        self.pos = pos
        self.item = item
        self.effects = []
        self.set_type(type)
    def set_type(self,type):
        self.type = type
        if type == "Grass":
            self.color = (0,170,0)
        if type == "Trees":
            self.color = (0,70,0)
        if type == "Water":
            self.color = (0,200,230)



class Selector:
    def __init__(self,status="null",color=(200,200,200),space=None):
        self.prevStatus = status
        self.space = space
        self.status=status
        self.color = color
        self.moveSelectors = []
        self.hover = None
    def select(self,space):
        print('selecting: ', space)
        self.prevStatus = self.status
        self.status = "static"
        self.space = Board[str(space)]
        global turn
        #get possible moves based on cursor
        if self.space.item != None and self.space.item.player == turn: # if its that players turn
            moves = self.space.item.getMoves()
            #print(moves)
            for move in moves:
                moveSpace = move["space"]
                moveType = move["type"]
                if moveType == "change pos":
                    #add blue selector for possible moves
                    self.moveSelectors.append(Selector(status="static",color=(200,200,100),space=Board[str(moveSpace)]))
                if moveType == "take piece":
                    #add red selector for take piece action
                    self.moveSelectors.append(Selector(status="static",color=(230,100,100),space=Board[str(moveSpace)]))
        #---update menus and game options according to cursor
        statsMenu.content[0][0] = "Player: " + str(turn)
        if (self.space.item):
            for line in range(len(self.space.item.description)):
                if line >= len(movesMenu.content[0]):
                    movesMenu.content[0].append(self.space.item.description[line])
                else: 
                    movesMenu.content[0][line] = self.space.item.description[line]
        if self.space != None:
            statsMenu.content[0][1] = str(self.space.pos)
            statsMenu.content[1][1] = self.space.type
            if Cursor.space.item != None:
                statsMenu.content[0][2] = "Content: " + self.space.item.name
            else:
                statsMenu.content[0][2] = "Content: "
        
    def deselect(self):
        print('deselecting', self.space)
        self.draw_selected(COLOR=(0,0,0))
        self.status = self.prevStatus
        self.prevStatus = "static"
        self.space = None
        self.moveSelectors = []
    def move(self,x,y):
        currentSpace = self.space.pos
        try:
            self.deselect()
            self.select((currentSpace[0]+x,currentSpace[1]+y))
        except:
            pass
    def draw_selected(self,COLOR=None):
        if self.status == "static":
            for a in range(-1,len(self.moveSelectors)):
                if a == -1: 
                    space = self.space.pos
                    color = self.color
                else: 
                    space = self.moveSelectors[a].space.pos
                    color = self.moveSelectors[a].color
                if COLOR != None: color = color
                draw_border(space,color)
    def remove(self):
        if self.status == "static":
            for a in range(-1,len(self.moveSelectors)):
                if a == -1: 
                    space = self.space.pos
                    color = self.color
                else: 
                    space = self.moveSelectors[a].space.pos
                    color = self.moveSelectors[a].color
                draw_border(space,(0,0,0))
    def update_hover(self):
        if self.status == "floating":
            new_mouse = get_mouse()
            if new_mouse and new_mouse != self.hover:
                if self.hover != None:
                    draw_border(self.hover,(0,0,0))
                self.hover = new_mouse
                draw_border(new_mouse,self.color)

        


Board = {}
for x in range(BOARDSIZE[0]):
    for y in range(BOARDSIZE[1]):
        Board[str((x,y))] = Space((x,y), GRASS)
Board["(7, 7)"] = Space((7,7), WATER)


Cursor = Selector(status="floating")



pieces = []
player1_pieces = []
player2_pieces = []
captured_pieces = []
class Piece:
    def __init__(self,space,player):
        self.space = space
        self.player = player
        pieces.append(self)
        if player == 1: player1_pieces.append(self)
        if player == 2: player2_pieces.append(self)
        Board[str(space)].item = self
    def moveTo(self,space):
        print('moving piece')
        Cursor.deselect()
        Board[str(self.space)].item = None
        self.space = space
        if Board[str(space)].item == None:
            Board[str(space)].item = self
        else:
            captured_piece = Board[str(space)].item
            captured_pieces.append(captured_piece)
            if captured_piece.player == 1: player1_pieces.remove(captured_piece)
            if captured_piece.player == 2: player2_pieces.remove(captured_piece)
            pieces.remove(captured_piece)
            Board[str(space)].item = self
            global WINNER
            if len(player1_pieces) == 0: WINNER = 2
            if len(player2_pieces) == 0: WINNER = 1
        toggleTurn()
        statsMenu.content[0][0] = "Player: " + str(turn)
        draw_all()

        #subclasses of piece must have:
        # self.img
        #self.name
        #function get moves -> returns array of possible moves [{space: (x,y), move: 'change pos'},{space: (x,y), move: 'take piece},{}...]



class Ghost(Piece):
    def __init__(self,space, player):
        self.name = "Ghost"
        self.img = pygame.image.load('images/ghost1.png')
        self.description = ["The Ghost is insane! It can move in any direction as far as you like.",
                    "A lot like the queen in chess, but more spooky...",
                  "Be careful! Ghost can not go over water."]
        Piece.__init__(self,space,player)
    def getMoves(self):
        moves = []
        for d in range(6): #6 possible directions
            spacePos = self.space
            for s in range(BOARDSIZE[0]):
                spacePos = step(spacePos, d)
                try:
                    Space = Board[str(spacePos)]
                except:
                    break
                if Space.type == WATER:
                    break
                if Space.item == None:
                    moves.append({"space": spacePos, "type": "change pos"})
                else:
                    if Space.item.player == self.player:
                        break
                    else:
                        moves.append({"space": spacePos, "type": "take piece"})
                        break

        return moves
class Wizard(Piece):
    def __init__(self,space, player):
        self.name = "Wizard"
        self.description = ["The wizard is kind of like the Knight in Chess...",
        "...but it can jump much farther.",
         "So watch out! Becuase it can hop over players and water."]
        self.img = pygame.image.load('images/player1-sprite.png')
        Piece.__init__(self,space,player)
    def getMoves(self):
        moves = []
        for d in range(6): #6 possible directions
            if d == 0: d1, d2 = 1, 5
            elif d == 5: d1, d2 = 0, 4
            else: d1, d2 = d+1, d-1
            spacePos = self.space
            for i in range(2):
                spacePos = step(spacePos,d)
            for di in [d1,d2]:

                spacePosi = step(spacePos,di)
                try:
                    Space = Board[str(spacePosi)]
                    if Space.type != WATER:
                        if Space.item == None:
                            moves.append({"space": spacePosi, "type": "change pos"})
                        elif Space.item.player != self.player:
                            moves.append({"space": spacePosi, "type": "take piece"})
                except:
                    pass
        return moves

class Skeleton(Piece):
    def __init__(self,space,player):
        self.name = "Skeleton"
        self.img = pygame.image.load('images/player2-sprite.png')
        self.description = ["The skeleton is like the Knight in Chess",
        "It can hop over players...",
        "...but with limited range"]
        Piece.__init__(self,space,player)
    def getMoves(self):
        moves = []
        for d in range(6): #6 possible directions
            if d == 0: d1, d2 = 1, 5
            elif d == 5: d1, d2 = 0, 4
            else: d1, d2 = d+1, d-1
            spacePos = self.space
            for i in range(1):
                spacePos = step(spacePos,d)
            for di in [d1,d2]:

                spacePosi = step(spacePos,di)
                try:
                    Space = Board[str(spacePosi)]
                    if Space.type != WATER:
                        if Space.item == None:
                            moves.append({"space": spacePosi, "type": "change pos"})
                        elif Space.item.player != self.player:
                            moves.append({"space": spacePosi, "type": "take piece"})
                except:
                    pass
        return moves

class Undead(Piece):
    def __init__(self,space,player):
        self.name = "Undead"
        self.img = pygame.image.load('images/player3-sprite.png')
        self.description = ["The undead is just your basic average piece.",
        "It can move two spaces in any direction.",
        "But don't underestimate him or you'll regret it"]
        Piece.__init__(self,space,player)
    def getMoves(self):
        moves = []
        for d in range(6): #6 possible directions
            spacePos = self.space
            for i in range(2):
                spacePos = step(spacePos,d)
                try:
                    Space = Board[str(spacePos)]
                    if Space.type == WATER or(Space.item != None and Space.item.player == turn):
                        break
                    if Space.item == None:
                        moves.append({"space": spacePos, "type": "change pos"})
                    elif Space.item.player != self.player:
                        moves.append({"space": spacePos, "type": "take piece"})
                except:
                    pass
        return moves




players = []
class Player:
    def __init__(self,name):
        self.name = name
        self.pieces = []
        if len(players) == 0:
            self.turn = 1
        else:
            self.turn = 0


def draw_board():
    global mouse_select
    base = board_offset
    highlightbase = False

    #draw board
    for y in range(BOARDSIZE[0]):
        for x in range(BOARDSIZE[1]):
            base = getBase(x,y)
            space = Board[str((x,y))]
            pygame.draw.polygon(screen,Board[str((x,y))].color,Hex(base))
            pygame.draw.polygon(screen,(0,0,0),Hex(base),3)
            if space.item != None:
                screen.blit(space.item.img,(base[0]+(2*size-space.item.img.get_size()[0])/2,base[1]+((2*size/math.sqrt(3))-space.item.img.get_size()[1])/2))

    Cursor.draw_selected()


def draw_menus():
    statsMenu.draw()
    movesMenu.draw()



def draw_all():
    screen.fill((0,0,0))
    draw_board()
    draw_menus()

def populate_water(num=6):
    for a in range(num):
        x = round(random()*(BOARDSIZE[0]-1))
        y = round(random()*(BOARDSIZE[1]-1))
        space = Board[str((x,y))]
        while (space.item != None and space.type != WATER):
            x = round(random()*(BOARDSIZE[0]-1))
            y = round(random()*(BOARDSIZE[1]-1))
            space = Board[str((x,y))]
        print(a,str((x,y)))
        space.set_type(WATER)


testPiece = Ghost((4,8), 1)
testPiece2 = Ghost((4,0),2)
testWizard = Wizard((4,7),1)
testWizard = Wizard((4,1),2)
testSkeleton = Skeleton((5,7),1)
testSkeleton = Skeleton((5,1),2)
testUndead11 = Undead((3,6),1)
testUndead12 = Undead((4,6),1)
testUndead13 = Undead((5,6),1)
testUndead21 = Undead((3,2),2)
testUndead22 = Undead((4,2),2)
testUndead23 = Undead((5,2),2)

populate_water(14)
done = False
mouse_ref = False
draw_all()
while not done:
    if not WINNER:
        Cursor.update_hover()
        mouse_select = get_mouse()
        for event in pygame.event.get():
            #close logic
            if event.type == pygame.QUIT:
                done = True
            #keypress logic
            if event.type == pygame.KEYDOWN:
                # cursor selecting a space, arrow keys move cursor
                if Cursor.status == "static":
                    if event.key == pygame.K_UP: Cursor.move(0,-1)
                    if event.key == pygame.K_DOWN: Cursor.move(0,1)
                    if event.key == pygame.K_LEFT: Cursor.move(-1,0)
                    if event.key == pygame.K_RIGHT: Cursor.move(1,0)
                    draw_all()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #left click to select and deselect space
                if event.button == 1:
                    if Cursor.status == "floating":
                        if mouse_select:
                            print('selecting...')
                            Cursor.select(mouse_select)
                            print(Cursor.space, 'selected')
                            draw_all()
                    elif Cursor.status == "static":
                        Cursor.deselect()
                        draw_all()
                #right click to do a move
                if event.button == 3:
                    if Cursor.status == "static" and len(Cursor.moveSelectors) != 0:
                        for selector in Cursor.moveSelectors:
                            if mouse_select == selector.space.pos:
                                Cursor.space.item.moveTo(mouse_select)
                                break
                if event.button == 5 and size > min_size:
                    #scroll out
                    increment = 30*(size/SCREENSIZE[0])
                    Bx = (pygame.mouse.get_pos()[0]-board_offset[0])/size
                    By = (pygame.mouse.get_pos()[1]-board_offset[1])/size
                    board_offset = [board_offset[0]+increment*Bx,board_offset[1]+increment*By]
                    size -= increment
                    draw_all()
                elif event.button == 4 and size < max_size:
                    #scroll in
                    increment = 30*(size/SCREENSIZE[0])
                    Bx = (pygame.mouse.get_pos()[0]-board_offset[0])/size
                    By = (pygame.mouse.get_pos()[1]-board_offset[1])/size
                    board_offset = [board_offset[0]-increment*Bx,board_offset[1]-increment*By]
                    size += increment
                    draw_all()
                if event.button == 1 and mouse_ref == False:
                    mouse_ref = pygame.mouse.get_pos()
        
            #if holding mouse down move board
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_ref = False
            if pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_pos() != mouse_ref and mouse_ref != False:
                    board_offset = [board_offset[0]+(pygame.mouse.get_pos()[0]-mouse_ref[0]),(board_offset[1]+(pygame.mouse.get_pos()[1]-mouse_ref[1]))]
                    mouse_ref = pygame.mouse.get_pos()
                    draw_all()
                    
        
        pygame.display.update()
    else:
        print("player ", str(WINNER), "wins!!!")
        done = True
pygame.quit()
