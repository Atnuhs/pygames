import os
import random
import sys
from pathlib import Path

import pygame
from pygame.locals import *


class System:
    def __init__(self, blocks, screen):
        self.screen = screen
        self.board = [
            [1 for i in range(25)] if j == 0 or j == 11 
            else [1 if i == 24 else 0 for i in range(25)] 
            for j in range(12)]
        self.blocks = blocks
        self.current = [0,0,0,0]
        self.order = random.sample(range(2,9), k=7)
    
    def blit(self, image):
        img_order = [0,6,1,2,3,4,9,10,11,13]
        for x,line in enumerate(self.board):
            for y, cell in enumerate(line):
                ref_px = 24*(img_order[cell])
                self.screen.blit(image,(24*(x),24*(y-5)), 
                    area=(0,ref_px,24,24))

    def create(self):
        self.current[0],self.current[1] = 5,4
        if self.order:
            self.current[2] = self.order.pop()
        else:
            self.order = random.sample(range(2,9),k=7)
        self.current[3] = random.randrange(4)
        if self.put_block(self.current) == False:
            self.game_over()
    
    def game_over(self):
        for x in range(1,11):
            for y in range(2,24):
                if self.board[x][y] != 0:
                    self.board[x][y] = 9
        pygame.time.set_timer(24,0)

    def event(self, event, down=False):
        x,y,r = self.current[0], self.current[1], self.current[3]
        if down == True:
            self.block_down()
            return
        if event.key == K_RIGHT:
            x += 1        
        elif event.key == K_LEFT:
            x -= 1
        elif event.key == K_UP:
            r -= 1
        elif event.key == K_r:
            r += 1
        else:
            pass
        if x != self.current[0] or y != self.current[1] or r != self.current[3]:
            n = [x,y,self.current[2], r]
            self.delete_block()
            if self.put_block(n) == True:
                self.current = n
            else:
                self.put_block(self.current)
        
    def block_down(self):
        self.delete_block()
        self.current[1] += 1
        if self.put_block(self.current) == False:
            self.current[1] -= 1
            self.put_block(self.current)
            self.delete_line()
            self.create()

    def delete_line(self):
        for y in range(2,24):
            flag = True
            for x in range(1,11):
                if self.board[x][y] == 0:
                    flag = False
            if flag == True:
                for j in range(y, 3, -1):
                    for i in range(1,11):
                        self.board[i][j] = self.board[i][j-1]

    def put_block(self, c, act=False):
        x, y, t = c[0], c[1], c[2]
        board = self.board
        blocks = self.blocks
        if board[x][y] != 0:
            return False
        if act == True:
            board[x][y] = t
        for i in range(3):
            dx = blocks.block[t][i+1][0]
            dy = blocks.block[t][i+1][1]
            r = c[3] % blocks.block[t][0]
            for j in range(r):
                dx,dy = dy,-dx
            if board[x+dx][y+dy] != 0:
                return False
            if act:
                board[x+dx][y+dy] = t
        if not act == True:
            self.put_block(c,act=True)
        self.board = board
        return True
    
    def delete_block(self):
        blocks = self.blocks
        board = self.board
        x,y,t = self.current[0], self.current[1], self.current[2] 
        board[self.current[0]][self.current[1]] = 0
        for i in range(3):
            dx = blocks.block[t][i+1][0]
            dy = blocks.block[t][i+1][1]
            r = self.current[3] % blocks.block[t][0]
            for j in range(r):
                dx, dy = dy, -dx
            board[x+dx][y+dy] = 0
        self.board = board
        self.blocks = blocks
            



class Blocks:
    def __init__(self):
        self.block = (
            (1, (0, 0), (0, 0), (0, 0)),    # null
            (1, (0, 0), (0, 0), (0, 0)),    # wall
            (2, (0, -1), (0, 1), (0, 2)),   # I
            (4, (0, -1), (0, 1), (1, 1)),   # L
            (4, (0, -1), (0, 1), (-1, 1)),  # J
            (2, (0, -1), (1, 0), (1, 1)),   # S
            (2, (0, -1), (-1, 0), (-1, 1)), # Z
            (1, (0, 1), (1, 0), (1, 1)),    # O
            (4, (1, 0), (0, -1), (-1, 0))   # T
        )
    
def main():
    main_path = Path(__file__).parent
    file_path = os.path.join(main_path, 'tetris.png')
    field = [10, 20]
    screen = [12, 20]
    entire_field = [12, 25]
    unit = 24
    field_px = (screen[0]*unit, screen[1]*unit)
    pygame.init()
    pygame.display.set_mode(field_px, 0, 32)
    screen = pygame.display.get_surface()
    image = pygame.image.load(file_path)
    blocks = Blocks()
    system = System(blocks, screen)
    time = 0
    system.create()
    while(1):
        pygame.display.update()
        pygame.time.wait(30)
        screen.fill((0,20,0,0))
        system.blit(image)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP or event.key == K_RIGHT or event.key == K_LEFT:
                    system.event(event)
                elif event.key == K_DOWN:
                    system.event(event, down=True)
                else:
                    pass
        time += 1
        if time >= 10:
            time = 0
            system.event(event, down=True)             
            
if __name__ == '__main__':
    main()
