# インポート宣言
import sys

import pygame
from pygame.locals import *

class Figure:
    def __init__(self, screen, bx=20, by=20, mass=32):
        self.screen = screen
        self.bx, self.by = bx, by
        self.mass = mass

    def message(self, message="test", size=30, pos=0):
        font = pygame.font.Font(None,size)
        text = font.render(message, True, (178,178,178))
        self.screen.blit(text,self.pos(pos))
    
    def pos(self, pos=0):
            return (self.mass*8+4*self.bx,(pos*3+2)*self.bx)
    
    def conversion(self,x, y):
        self.px = x*self.mass + self.bx
        self.py = y*self.mass + self.by
    
    def square(self, x=0, y=0):
        self.conversion(x, y)
        pygame.draw.rect(self.screen, (20,128,20), 
            Rect(self.px, self.py, self.mass-1, self.mass-1))
        pygame.draw.rect(self.screen, (0,0,0), 
            Rect(self.px, self.py, self.mass, self.mass), 1)
        pygame.draw.rect(self.screen, (00,64,0), 
            Rect(self.px, self.py, self.mass+1, self.mass+1), 1)

    def black(self, x=0, y=0):
        self.square(x, y)
        posx = self.px+int(self.mass*0.1)
        posy = self.py+int(self.mass*0.1)
        rad = int(self.mass*0.8)
        pygame.draw.ellipse(self.screen, (20,20,20), 
                            (posx, posy, rad, rad))
        pygame.draw.ellipse(self.screen, (40, 40, 40),
                            (posx, posy, rad, rad),2)
    
    def white(self, x=0, y=0):
        self.square(x, y)
        posx = self.px+int(self.mass*0.1)
        posy = self.py+int(self.mass*0.1)
        rad = int(self.mass*0.8)
        pygame.draw.ellipse(self.screen, (236, 236, 236),
                            (posx, posy, rad, rad))
        pygame.draw.ellipse(self.screen, (216, 216, 216),
                            (posx, posy, rad, rad),2)
    
    def board(self):
        for x in range(8):
            for y in range(8):
                self.square(x,y)
    
    def sc1(self):
        pygame.draw.rect(self.screen, (128,20,20),
            Rect(self.mass*8+3*self.bx, self.by, 
            self.mass*4, self.mass*10+self.by*2))
        pygame.draw.rect(self.screen, (64, 0, 0),
            Rect(self.mass*8+3*self.bx, self.by, 
            self.mass*4, self.mass*10+self.by*2), 2)
                
    def sc2(self):
        pygame.draw.rect(self.screen, (80, 80, 128), 
            Rect(self.bx, self.mass*8+3*self.by, 
            self.mass*8, self.mass*2))
        pygame.draw.rect(self.screen, (0, 0, 64),
            Rect(self.bx, self.mass*8+3*self.by, 
            self.mass*8, self.mass*2), 2)
        

class Game:
    def __init__(self, board):
        
        self.status = [[0 for i in range(10)] for j in range(10)]
        self.board = board
        self.turn = 2
        self.messages = ["","", "", "", "", ""]
        self.computer = 3
        self.mass = self.board.mass
        self.senni = [[],[]]
    
    def update_status(self, x, y):
        if self.turn == 1:
            self.status[x+1][y+1] = 1
        elif self.turn == 2:
            self.status[x+1][y+1] = 2

    def currentboard(self):
        self.board.sc1()
        self.board.sc2()
        for x in range(8):
            for y in range(8):
                state = self.status[x+1][y+1]
                if state == 0:
                    self.board.square(x,y)
                elif state == 1:
                    self.board.black(x,y)
                elif state == 2 :
                    self.board.white(x,y)
        for num, message in enumerate(self.messages): 
            self.board.message(message, 30,num)

    def start(self):
        self.status[4][5] = 1
        self.status[5][4] = 1
        self.status[4][4] = 2
        self.status[5][5] = 2
        self.turn_change()
    
    def stonenumber(self, black, white, put):
        self.messages[2] = "black > " + str(black)
        self.messages[3] = "white > " + str(white)
        if put == True:
            self.senni[0].append(black)
            self.senni[1].append(white)

    def turn_change(self):
        self.turn = 3-self.turn
        if self.turn == 1:
            turn = "Black"
        else:
            turn = "White"
        black = 0
        white = 0
        for x in range(8):
            for y in range(8):
                if self.status[x+1][y+1] == 1:
                    black += 1
                elif self.status[x+1][y+1] == 2:
                    white += 1
        self.stonenumber(black, white, True)
        for x in range(8):
            for y in range(8):
                if self.status[x+1][y+1] == 0\
                        and self.put_judge(x,y,False):
                    self.messages[0] = turn + " turn"
                    self.messages[1] = ''
                    self.stonenumber(black, white, False)
                    self.computerMove()
                    return
        self.turn = 3-self.turn
        if self.turn == 1:
            turn = "Black"
        else:
            turn = "White"
        black = 0
        white = 0
        for x in range(8):
            for y in range(8):
                if self.status[x+1][y+1] == 0\
                        and self.put_judge(x, y, False):
                    self.messages[0] = 'pass'
                    self.messages[1] = turn + " turn"
                    self.stonenumber(black, white, False)
                    return
                else:
                    if self.status[x+1][y+1] == 1:
                        black += 1
                    elif self.status[x+1][y+1] == 2:
                        white += 1
        self.messages[1] = ''
        self.stonenumber(black, white, False)
        if black > white:
            self.messages[0] = 'black won'
           
        elif black < white:
            self.messages[0] = 'white won'
           
        else:
            self.messages[0] = 'draw'
        

    def put_stone(self, px, py):
        x,y = int(px/self.mass),int(py/self.mass)
        if x>7 or y>7:
            return
        if self.put_judge(x, y, True) != 0:
            self.update_status(x,y)
            self.turn_change()
        else:
            pass
        pygame.display.update()

    def put_judge(self, x, y, flip):
        if self.status[x+1][y+1] == 0:
            pass
        else:
            return 0
        ret = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx,ny = x+dx, y+dy
                n = 0
                while self.status[nx+1][ny+1]\
                        == 3-self.turn:
                    n += 1
                    nx += dx
                    ny += dy
                if n > 0 and self.status[nx+1][ny+1]\
                        == self.turn:
                    ret += n
                    if flip:
                        nx, ny = x+dx, y+dy
                        while self.status[nx+1][ny+1]\
                                == 3 - self.turn:
                            self.update_status(nx, ny)
                            nx += dx
                            ny += dy
        return ret

    def computerMove(self):
        self.currentboard()
        pygame.display.update()
        pygame.time.wait(100)
        if self.computer == self.turn:
            for x in range(8):
                for y in range(8):
                    if self.status[x+1][y+1] == 0\
                            and self.put_judge(x, y, True):
                        self.update_status(x, y)
                        self.turn_change()
                        return 


def main():
    pygame.init()
    mass = 40
    board = mass*8
    xgap, ygap = int(mass/4), int(mass/4)
    systemscreen = mass*4
    systemscreen2 = mass*2
    screen = pygame.display.set_mode(
        (board+4*xgap+systemscreen, 
        board+4*ygap+systemscreen2))
    pygame.display.set_caption('Pygame')
    font = pygame.font.Font(None, 55)
    board = Figure(screen, xgap, ygap, mass)
    game = Game(board)
    game.start()

    while(1):
        pygame.display.update()
        pygame.time.wait(30)
        screen.fill((20, 20, 20))
        game.currentboard()
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN \
            and event.button == 1:
                x,y = event.pos
                if 0<=(x-xgap)/mass<=8 \
                and 0<=(y-ygap)/mass<=8:
                    game.put_stone(x-xgap,y-ygap)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()



# 実行文---
if __name__ == "__main__":
    main()
