# import declaration
import random
import sys
import time

import pygame
from pygame.locals import *

import numpy as np


def create_color_list(saturation_number=5, _max=255,_min=0):
    # R,G,B,GB,RB,RG
    saturation_list = [int(_min + (_max+_min)/(saturation_number-1)*saturation) 
                       for saturation in range(saturation_number)]
    color_list = ((1,1,1),(1,0,0),(0,1,0),(0,0,1),
        (0,0.5,0.5),(0.5,0,0.5),(0.5,0.5,0))

    ret = [[[RGB*sat for RGB in color] 
            for sat in saturation_list] 
           for color in color_list]
    return ret


class Cells:
    def __init__(self, screen,size,menu_height,color_list):
        self.screen = screen
        self.unit_size,self.row_num,self.col_num = size
        self.menu_height = menu_height
        self.color_list = color_list
        self.cell_num = self.row_num*self.col_num
    def draw_cell_frame(self,x,y):
        pygame.draw.rect(self.screen, self.color_list[0][1],
            Rect((x-1)*self.unit_size,(y-1)*self.unit_size+self.menu_height,self.unit_size, self.unit_size),1)
    
    def draw_living_cell(self,state,size1,size2,_max):
        screen,us,mh,cell = self.screen,self.unit_size,self.menu_height,self.cell_num
        ''
        for i,ref in enumerate(state):
            color = self.color_list[1][_max-i]
            for j in range(cell):
                if int(ref) & 1: # 重い（確定）
                    y,x = divmod(j,size1)
                    pygame.draw.rect(screen, color,
                        Rect((x)*us,(y)*us+mh,us, us))
                ref >>= 1
        ''
    
    

class Menu:
    def __init__(self,screen,menu_size,color_list):
        self.screen = screen
        self.size = menu_size
        self.color_list = color_list
        self.font = pygame.font.Font(None, 30)
    
    def draw_rect(self,_rect):
        pygame.draw.rect(self.screen, self.color_list[1][1],Rect(*_rect))
        pygame.draw.rect(self.screen, self.color_list[1][1],Rect(*_rect),1)
    
    def draw_main_menu_bg(self):
        self.draw_rect((0,0,self.size[0],self.size[1]))

    def draw_main_menu_button(self,pos,message):
        b_pos = (pos*self.size[1],0,self.size[1],self.size[1])
        self.draw_rect(b_pos)
        text = self.font.render(message,True,self.color_list[0][1])
        self.screen.blit(text, Rect(*b_pos))
        
        
class Units:
    def __init__(self,screen,cell_size, menu_size, definition):
        color_list = create_color_list(definition[2])
        self.definition = definition
        self.cells = Cells(screen, cell_size,menu_size[1],color_list)
        self.menu = Menu(screen, menu_size,color_list)
        self.game = Game(cell_size,self.cells,self.menu,definition)
        self.ship = Ship(screen,cell_size,color_list,menu_size,self.game,self.menu)

class Game:
    def __init__(self,size,cells,menu,definition):
        self.size,self.menu = size,menu # size, colum, row
        self.cells,self.definition = cells,definition
        self.max = self.definition[2]-1
        self.size = size
        self.state = [0,0,0]
        self.masks = self.make_masks()
        self.loop_mask = self.make_loopmasks()
        self.shift = self.make_shift()
        self.show_board()
        self.loop = 1

    def make_loopmasks(self):
        x,y = self.size[1:]
        rnum = y - 2
        lsnum = x * (y-1)
        ssnum = x - 1
        
        d2 = 1
        c2 = d2 << ssnum
        c3 = ((1<<x)-1) & ~c2
        d3 = (c2 << 1) - 2

        b2 = d2 << lsnum
        a1 = c2 << lsnum
        a2 = c3 << lsnum
        b1 = d3 << lsnum

        a3,b3 = c2,d2
        for i in range(rnum):
            a3 <<= x
            b3 <<= x
            a3 |= c2
            b3 |= d2
        
        c1 = a3 << x
        d1 = b3 << x

        return (a1,a2,a3,b1,b2,b3,c1,c2,c3,d1,d2,d3)
    
    def make_shift(self):
        x,y = self.size[1:]
        side = x*(y-1)
        a1 = 1
        a2 = side - 1
        a3 = x*y - 1
        c1 = 2*x - 1
        c2 = side + 1
        c3 = x*(y-2)+1
        return(a1,a2,a3,c1,c2,c3)

    def make_masks(self):
        x,y = self.size[1:]
        _left = (2<<(x-2)) - 1
        # 0111 ex(4*4)
        _right = (2<<(x-1)) - 2
        # 1110 ex(4*4)
        _L,_R = 0,0
        for i in range(y):
            _L <<= x
            _R <<= x
            _L |= _left
            _R |= _right
        '''
        ex(4*4)
        _L = 0111
             0111
             0111
             0111

        _R = 1110
             1110
             1110
             1110
        '''
        _all = (1<<(x*y)) - 1
        '''
        1111
        1111
        1111
        1111
        '''
        _U = _all >> x
        '''
        0000
        1111
        1111
        1111
        '''
        _D = _U << x
        '''
        1111
        1111
        1111
        0000
        '''
        _UL = _U & _L
        '''
        0000
        0111
        0111
        0111
        '''
        _UR = _U & _R
        '''
        0000
        1110
        1110
        1110
        '''
        _DL = _D & _L
        '''
        0111
        0111
        0111
        0000
        '''
        _DR = _D & _R
        '''
        1110
        1110
        1110
        0000
        '''
        return (_DR,_D,_DL,_R,_L,_UR,_U,_UL,_all)

    def show_board(self):
        self.cells.draw_living_cell(self.state,self.size[1],self.size[2],int(self.max))

    def debug(self,bits):
        x,y = self.size[1:]
        bits = format(bits,'016b')
        for i in range(y):
           print(bits[i*x:(i+1)*x])
        print('-'*4)

    def make_next_state(self):
        T = self.state[0]
        x,y = self.size[1:]
        zeros = (self.masks[8] & ~(self.state[0] | self.state[1] | self.state[2]))
        self.state[2] = self.state[1]

        a = (T & self.masks[0]) >> x+1
        b = (T & self.masks[1]) >> x
        c = (T & self.masks[2]) >> x-1
        d = (T & self.masks[3]) >> 1
        e = (T & self.masks[4]) << 1
        f = (T & self.masks[5]) << x-1
        g = (T & self.masks[6]) << x
        h = (T & self.masks[7]) << x+1

        if self.loop:
            a1 = (T & self.loop_mask[9]) >> self.shift[0]
            a2 = (T & self.loop_mask[11]) << self.shift[1]
            a3 = (T & self.loop_mask[10]) << self.shift[2]
            b_ = (T & ~self.masks[1]) << x*(y-1)
            c1 = (T & self.loop_mask[6]) >> self.shift[3]
            c2 = (T & self.loop_mask[8]) << self.shift[4]
            c3 = (T & self.loop_mask[7]) << self.shift[5]
            d_ = (T & ~self.masks[3]) << x-1
            e_ = (T & ~self.masks[4]) >> x-1
            f1 = (T & self.loop_mask[5]) << self.shift[3]
            f2 = (T & self.loop_mask[3]) >> self.shift[4]
            f3 = (T & self.loop_mask[4]) >> self.shift[5]
            g_ = (T & ~self.masks[6]) >> x*(y-1)
            h1 = (T & self.loop_mask[2]) << self.shift[0]
            h2 = (T & self.loop_mask[1]) >> self.shift[1]
            h3 = (T & self.loop_mask[0]) >> self.shift[2]
            
            a_ = a1|a2|a3
            c_ = c1|c2|c3
            f_ = f1|f2|f3
            h_ = h1|h2|h3

            a |= a_
            b |= b_
            c |= c_
            d |= d_
            e |= e_
            f |= f_
            g |= g_
            h |= h_

        s0 = ~(a|b)
        s1 = a^b
        s2 = a&b

        s3 = c & s2
        s2 = (s2 & ~c) | (s1 & c)
        s1 = (s1 & ~c) | (s0 & c)
        s0 = s0 & ~c

        s4 = d & s3
        s3 = (s3 & ~d) | (s2 & d)
        s2 = (s2 & ~d) | (s1 & d)
        s1 = (s1 & ~d) | (s0 & d)
        s0 = s0 & ~d

        s5 = e & s4
        s4 = (s4 & ~e) | (s3 & e)
        s3 = (s3 & ~e) | (s2 & e)
        s2 = (s2 & ~e) | (s1 & e)
        s1 = (s1 & ~e) | (s0 & e)
        s0 = s0 & ~e

        s6 = f & s5
        s5 = (s5 & ~f) | (s4 & f)
        s4 = (s4 & ~f) | (s3 & f)
        s3 = (s3 & ~f) | (s2 & f)
        s2 = (s2 & ~f) | (s1 & f)
        s1 = (s1 & ~f) | (s0 & f)
        s0 = s0 & ~f
        
        s7 = g & s6
        s6 = (s6 & ~g) | (s5 & g)
        s5 = (s5 & ~g) | (s4 & g)
        s4 = (s4 & ~g) | (s3 & g)
        s3 = (s3 & ~g) | (s2 & g)
        s2 = (s2 & ~g) | (s1 & g)
        s1 = (s1 & ~g) | (s0 & g)
        s0 = s0 & ~g

        s8 = h & s7
        s7 = (s7 & ~h) | (s6 & h)
        s6 = (s6 & ~h) | (s5 & h)
        s5 = (s5 & ~h) | (s4 & h)
        s4 = (s4 & ~h) | (s3 & h)
        s3 = (s3 & ~h) | (s2 & h)
        s2 = (s2 & ~h) | (s1 & h)
        s1 = (s1 & ~h) | (s0 & h)
        s0 = s0 & ~h
            
        self.state[0], self.state[1] = (T & (s3|s4|s5))|(zeros & (s2)), T & ~(s3|s4|s5)
        
    def show_menu(self):
        self.menu.draw_main_menu_bg()
        self.menu.draw_main_menu_button(0,"0")
        self.menu.draw_main_menu_button(1,"1")

    def __call__(self):
        start = time.time()
        self.show_board()
        time1 = time.time() -start
        start = time.time()
        self.show_menu()
        time2 = time.time() -start
        start = time.time()
        self.make_next_state()
        time3 = time.time() -start
        total = (time1+time2+time3)/100
        try:
            print('-'*20 + '\nshowboard{0},\nshowmenu{1},\ncalcstate{2}'.format(time1,time2,time3))
        except:
            pass
    
class Ship:
    def __init__(self,screen,size,color_list,menu_size,game,menu):
        self.shape = np.array([[-1,-1],[2,-1],\
            [-2,0],[-1,0],[0,0],[1,0],[2,0],[3,0],\
            [-2,1],[-1,1],[2,1],[3,1]])
        self.bullet_shape = np.array([[[0,-2],[1,-2]],[[0,-1],[1,-1]]])
        self.direction = 0
        self.screen = screen
        self.cell, self.x,self.y = size
        self.initpos = [self.x//2,self.y//2]
        self.color_list = color_list
        self.menu_size = menu_size
        self.game = game
        self.show_hp = menu.draw_main_menu_button
        self.cool_time = 0
        self.hp = 100

    def __call__(self):
        self.detect_key_input()
        self.show_ship(self.shape.copy())
        self.calc_dmg()

    def calc_dmg(self):
        s_bin = self.conv_cor_to_bin(self.initpos)
        if s_bin & self.game.state[0]:
            self.hp -= 1
        self.show_hp(2,'HP')
        self.show_hp(3,'<'+str(self.hp)+'>')
        
    
    def detect_key_input(self):
        pressed_key = pygame.key.get_pressed()

        if pressed_key[K_UP]:
            self.direction = 0
            self.initpos[1] -= 1
        if pressed_key[K_RIGHT]:
            self.direction = 3
            self.initpos[0] += 1
        if pressed_key[K_DOWN]:
            self.direction = 2
            self.initpos[1] += 1
        if pressed_key[K_LEFT]:
            self.direction = 1
            self.initpos[0] -= 1
        if pressed_key[K_SPACE]:
            self.show_shot()
        else:
            self.cool_time = 0

    
    def show_shot(self):
        if self.cool_time:
            self.cool_time -= 1
            return
        b_shape = self.bullet_shape.copy()
        for i in range(self.direction):
            b_shape[:,:,0],b_shape[:,:,1] = b_shape[:,:,1],-b_shape[:,:,0]
        b_shape += self.initpos
        b1_bin = 0
        b2_bin = 0
        for cor in b_shape[0]:
            ret = self.conv_cor_to_bin(cor)
            b1_bin |= ret
        for cor in b_shape[1]:
            ret = self.conv_cor_to_bin(cor)
            b2_bin |= ret
        
        self.game.state[0] |= b1_bin
        self.game.state[1] |= b2_bin
        self.cool_time = 1

    def conv_cor_to_bin(self,cor):
        try:
            ret1 = int(self.x*cor[1] + cor[0])
            ret2 = 1 << ret1
            if ret2 > 0:   
                return ret2
            else:
                return 0
        except:
            return 0

        

    def show_ship(self,shape):
        x,y = self.x*self.cell,self.y*self.cell
        for i in range(self.direction):
            shape[:,0],shape[:,1] = shape[:,1],-shape[:,0]
        c_pos = shape + self.initpos
        c_pos *= self.cell
        c_pos[:,1] += self.menu_size[1]
        s_bin = 0
        for pos in c_pos:
            if x < pos[0]:
                pos[0] -= x
            elif self.menu_size[1] > pos[1]:
                pos[1] += y
            elif y+self.menu_size[1] < pos[1]:
                pos[1] -= y
            elif 0 > pos[0]:
                pos[0] += x
            pygame.draw.rect(self.screen,self.color_list[2][3],Rect(*pos,self.cell,self.cell))

        if 0 > self.initpos[0]:
            self.initpos[0] += self.x
        elif self.x < self.initpos[0]:
            self.initpos[0] -= self.x
        elif 0 > self.initpos[1]:
            self.initpos[1] += self.y
        elif self.y < self.initpos[1]:
            self.initpos[1] -= self.y



        pygame.draw.rect(self.screen, self.color_list[3][3],Rect(*c_pos[4],self.cell,self.cell))


        
def main():
    # main function
    pygame.init()

    cell_size = [4,150,120] #cellsize, 8*col, 8*row
    menu_size = [cell_size[0]*cell_size[1],30]
    definition = ((3,4,5),(2,),4) # S, B, C
    screen = pygame.display.set_mode((cell_size[0]*cell_size[1],\
        cell_size[0]*cell_size[2]+menu_size[1]))
    units = Units(screen,cell_size,menu_size,definition)
    
    while True:
        pygame.time.wait(20)
        screen.fill((0,0,0))
        units.game()
        start = time.time()
        units.ship()
        time3 = time.time() -start
        print('ship ='+str(time3))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = event.pos


if __name__ == '__main__':
    main()
