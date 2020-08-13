import os
import random
import sys
from pathlib import Path

import pygame
from pygame.locals import *


#---
class Stage:
    def __init__(self,screen):
        self.screen = screen
        self.make_parts()
        
        self._map = (
            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (0,6,14 ,14,14,14,14,14,14,14,14,14,14,14,11,5,14,14,14,14,14,14,14,14,14,14,14,14,12,0),
            (0,2,0, 0,0, 0, 0,0,0, 0,0,0, 0,0,15,1,0,0, 0,0, 0, 0,0,0,0,0, 0,0,13,0),
            (0,2,0, 5,3, 3,11,0,5, 3,3,3,11,0,15,1,0,5, 3,3, 3,11,0,5,3,3,11,0,13,0),
            (0,2,0, 1,0, 0, 1,0,1, 0,0,0, 1,0,15,1,0,1, 0,0, 0, 1,0,1,0,0, 1,0,13,0),
            (0,2,0, 7,3, 3, 9,0,7, 3,3,3, 9,0, 7,9,0,7, 3,3, 3, 9,0,7,3,3, 9,0,13,0),
            (0,2,0, 0,0, 0, 0,0,0, 0,0,0, 0,0, 0,0,0,0, 0,0, 0, 0,0,0,0,0, 0,0,13,0),
            (0,2,0, 5,3, 3,11,0,5,11,0,5, 3,3, 3,3,3,3,11,0, 5,11,0,5,3,3,11,0,13,0),
            (0,2,0, 7,3, 3, 9,0,1, 1,0,7, 3,3,11,5,3,3, 9,0, 1, 1,0,7,3,3, 9,0,13,0),
            (0,2,0, 0,0, 0, 0,0,1, 1,0,0, 0,0, 1,1,0,0, 0,0, 1, 1,0,0,0,0, 0,0,13,0),
            (0,8,4, 4,4, 4,12,0,1, 7,3,3,11,0, 1,1,0,5, 3,3, 9, 1,0,6,4,4, 4,4,10,0),
            (0,0,0, 0,0, 0, 2,0,1, 5,3,3, 9,0, 7,9,0,7, 3,3,11, 1,0,2,0,0, 0,0, 0,0),
            (0,0,0, 0,0, 0, 2,0,1, 1,0,0, 0,0, 0,0,0,0, 0,0, 1, 1,0,2,0,0, 0,0, 0,0),
            (0,0,0, 0,0, 0, 2,0,1, 1,0,6, 4,4, 4,4,4,4,12,0, 1, 1,0,2,0,0, 0,0, 0,0),
            (0,4,4, 4,4, 4,10,0,7, 9,0,2, 0,0, 0,0,0,0, 2,0, 7, 9,0,8,4,4, 4,4, 4,0),
            (0,0,0, 0,0, 0, 0,0,0, 0,0,2, 0,0, 0,0,0,0, 2,0, 0, 0,0,0,0,0, 0,0, 0,0),
            (0,4,4, 4,4, 4,12,0,0, 0,0,2, 0,0, 0,0,0,0, 2,0, 0, 0,0,6,4,4, 4,4, 4,0),
            (0,0,0, 0,0, 0, 2,0,5,11,0,8, 4,4, 4,4,4,4,10,0, 5,11,0,2,0,0, 0,0, 0,0),
            (0,0,0, 0,0, 0, 2,0,1, 1,0,0, 0,0, 0,0,0,0, 0,0, 1, 1,0,2,0,0, 0,0, 0,0),
            (0,0,0, 0,0, 0, 2,0,1, 1,0,5, 3,3, 3,3,3,3,11,0, 1, 1,0,2,0,0, 0,0, 0,0),
            (0,6,4, 4,4, 4,10,0,7, 9,0,7, 3,3,11,5,3,3, 9,0, 7, 9,0,8,4,4, 4,4,12,0),
            (0,2,0, 0,0, 0, 0,0,0, 0,0,0, 0,0, 1,1,0,0, 0,0, 0, 0,0,0,0,0, 0,0,13,0),
            (0,2,0, 5,3, 3,11,0,5, 3,3,3,11,0, 1,1,0,5, 3,3, 3,11,0,5,3,3,11,0,13,0),
            (0,2,0, 7,3,11, 1,0,7, 3,3,3, 9,0, 7,9,0,7, 3,3, 3, 9,0,1,5,3, 9,0,13,0),
            (0,2,0, 0,0, 1, 1,0,0, 0,0,0, 0,0, 0,0,0,0, 0,0, 0, 0,0,1,1,0, 0,0,13,0),
            (0,7,3,11,0, 1, 1,0,5,11,0,5, 3,3, 3,3,3,3,11,0, 5,11,0,1,1,0, 5,3, 9,0),
            (0,5,3, 9,0, 7, 9,0,1, 1,0,7, 3,3,11,5,3,3, 9,0, 1, 1,0,7,9,0, 7,3,11,0),
            (0,2,0, 0,0, 0, 0,0,1, 1,0,0, 0,0, 1,1,0,0, 0,0, 1, 1,0,0,0,0, 0,0, 2,0),
            (0,2,0, 5,3, 3, 3,3,9, 7,3,3,11,0, 1,1,0,5, 3,3, 9, 7,3,3,3,3,11,0, 2,0),
            (0,2,0, 7,3, 3, 3,3,3, 3,3,3, 9,0, 7,9,0,7, 3,3, 3, 3,3,3,3,3, 9,0, 2,0),
            (0,2,0, 0,0, 0, 0,0,0, 0,0,0, 0,0, 0,0,0,0, 0,0, 0, 0,0,0,0,0, 0,0, 2,0),
            (0,8,4, 4,4, 4, 4,4,4, 4,4,4, 4,4, 4,4,4,4, 4,4, 4, 4,4,4,4,4, 4,4,10,0),
            (0,0,0, 0,0, 0, 0,0,0, 0,0,0, 0,0, 0,0,0,0, 0,0, 0, 0,0,0,0,0, 0,0, 0,0),
        )
    def make_parts(self):
        ub=Units()
        w1=ub(9)
        w2=ub(10)
        r=ub(11)
        walls_0 = [w1[1],w2[1]]
        walls_90 = [pygame.transform.rotate(parts,90) for parts in walls_0]
        dwalls = [pygame.transform.rotate(w2[1],180),pygame.transform.rotate(w2[1],270)]
        rwalls_0 = [w1[0],w2[0]]
        swalls = [pygame.transform.rotate(
            w1[1], 180), pygame.transform.rotate(w1[1], 270)]
        rwalls_90 = [pygame.transform.rotate(parts,90) for parts in rwalls_0]
        rwalls_180 = [pygame.transform.rotate(parts,180) for parts in rwalls_0]
        rwalls_270 = [pygame.transform.rotate(parts, 270) for parts in rwalls_0]

        self.parts = [*r,*walls_0,*walls_90,*rwalls_0,*rwalls_90,*rwalls_180,*rwalls_270,*dwalls,*swalls]

    def blit(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                self.screen.blit(self.parts[self._map[y][x]], 
                Rect(x*24,y*24,24,24))

class Esa:
    def __init__(self, ppos):
        units = Units
        self.ppos = ppos
        self.esa = units(6)
    



class POS:
    def __init__(self,_map, screen):
        self.abso_dir = ((0,-3,0), (1,0,-3), (2,3,0), (3,0,3),(0,0,0))
        self.pos_list = [[0, 300, 280], [3, 240, 300], [
            3, 460, 300], [3, 240, 420], [3, 460, 420]]
        self.font = pygame.font.Font(None, 24)
        self._map = _map
        self.meslis = [self._move_pacman, self._move_aka,self._move_pinky, self._move_ao, self._move_guzu]
        self.screen = screen
        self.typecolor = ((0,0,0), (255,31,31), (255,127,127), (127,127,255), (255,255,127))
        self.modetime = [10,10,10,10,10]
        self.mode = [0,0,0,0,0]
        self.difencepos = ((0,0),(24*2,24*2),(24*27,24*2),(24*2,24*30),(24*27,24*30),)
        self.izikemode = False
    def _move_pacman(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            d = self.abso_dir[0]
        elif pressed_key[K_RIGHT]:
            d = self.abso_dir[2]
        elif pressed_key[K_UP]:
            d = self.abso_dir[1]
        elif pressed_key[K_DOWN]:
            d = self.abso_dir[3]
        else:
            d = (self.pos_list[0][0],*self.abso_dir[4][1:])
            

        n_pos = d[0], self.pos_list[0][1] + \
            d[1], self.pos_list[0][2]+d[2]
        if self.is_move(0,*n_pos[1:]):
            self.pos_list[0] = [*n_pos]
        else:
            pass
    
    
    def _move_animal(self,_type, goal):
        (d, x, y) = self.pos_list[_type]
        (px, py) = goal
        r_dir = self.get_rel_dir(d)
        emarg = r_dir.pop(2)
        dir_opt = []
        for _dir in r_dir[:]:
            (dd, dx, dy) = self.abso_dir[_dir]
            nx, ny = dx+x, dy+y
            if self.is_move(_type, nx, ny):
                distance = (px-nx)**2+(py-ny)**2
                dir_opt.append([_dir, nx, ny, distance])
                continue
            else:
                r_dir.remove(_dir)
                continue

        dis_list = [_dir[3] for _dir in dir_opt]
        if dis_list:
            f_dir = dir_opt[dis_list.index(min(dis_list))]
            self.pos_list[_type] = f_dir[:3]
            return

        else:
            (dd, dx, dy) = self.abso_dir[emarg]
            nx, ny = dx+x, dy+y
            self.pos_list[_type] = [emarg, nx, ny]



    def _move_aka(self):
        goal = self.pos_list[0][1:]
        self._move_animal(1,goal)
        pygame.draw.ellipse(self.screen, (255, 31, 31),
                            Rect(*goal, 20, 20))
        

    def _move_pinky(self):
        x,y = self.pos_list[2][1:]
        (pd,px,py) = self.pos_list[0]
        distance = (abs(x-px)+abs(y-py))/3
        if distance > 100:
            distance = 100
        goal = px+self.abso_dir[pd][1]*distance, py + \
            self.abso_dir[pd][2]*distance
        self._move_animal(2,goal)
        pygame.draw.ellipse(self.screen, (255, 127, 127),
                            Rect(*goal, 20, 20))



    def _move_ao(self):
        goal = 2*self.pos_list[0][1]-self.pos_list[1][1],2*self.pos_list[0][2]-self.pos_list[1][2]
        dx,dy = self.pos_list[0][1:]
        self._move_animal(3,goal)
        pygame.draw.ellipse(self.screen, (127, 127, 255),
                            Rect(*goal, 20, 20))
    
    def _move_guzu(self):
        px,py = self.pos_list[0][1:]
        goal = random.randrange(px-24*4, px+24*4), random.randrange(py-24*4, py+24*4)
        self._move_animal(4,goal)
        pygame.draw.ellipse(self.screen, (255, 255, 127),
                            Rect(*goal, 20, 20))
    
    def _move_difence(self, _type):
        goal = self.difencepos[_type]
        self._move_animal(_type, goal)
        pygame.draw.ellipse(self.screen, self.typecolor[_type],
                            Rect(*goal, 20, 20))
    


    
    def is_move(self,_type,x,y):
        pos = [int((x+12)/24),
               int((y+12)/24)]
        if not (0<pos[0]<30 and 0<pos[1]<35):
            return False
        if self._map._map[pos[1]][pos[0]]:
            return False
        else:
            for num,pos in enumerate(self.pos_list):
                if num == _type:
                    continue
                if pos[1] -24 <= x <= pos[1]+24 and pos[2] -24 <= y <= pos[2]+24:
                    return False
            
            return True
    
    def get_rel_dir(self, d):
        return [d % 4, (d+1) % 4, (d+2) % 4, (d+3) % 4]
    
    def is_change(self,_type):
        if self.modetime[_type]:
            self.modetime[_type] -= 1
        else:
            self.modetime[_type] = 200
            self.mode[_type] = 1-self.mode[_type]

    def get_pos(self,_type):
        if not _type:
            self._move_pacman()
            self._move_pacman()    
        else:
            self.is_change(_type)
            if self.mode[_type]:
                self.meslis[_type]()
                self.meslis[_type]()
            else:
                self._move_difence(_type)
                self._move_difence(_type)
        return self.pos_list[_type]

        



class Chara:
    def __init__(self,_type,pos):
        units = Units()
        self.type = _type
        self.pos = pos
        self.units = units(_type)
        self.current_unit = self.units[0]
        self.repeat = len(self.units)
        self.size = self.current_unit.get_size()
        self.counter = 0

    def __call__(self,screen):
        npos = self.pos.get_pos(self.type)
        self.update(npos[0])
        self.draw(screen, npos)

    def update(self,direction):
        self.counter += 1
        if self.counter > self.repeat-1:
            self.counter = 0
        
        if not self.type:
            self.current_unit = pygame.transform.rotate(
                self.units[self.counter], -90*direction)
        else:
            self.current_unit = self.units[self.counter]

    def draw(self, screen, npos):
        screen.blit(self.current_unit, (npos[1], npos[2], self.size[0], self.size[1]))

class Units:
    def __init__(self):
        self.pos = (
            ((0, 0), (1, 0), (3, 2), (1, 0)),# pac-man
                    ((0, 1), (1, 1)),# akabe
                    ((0, 2), (1, 2)),# pinky
                    ((0, 3), (1, 3)),# aosuke
                    ((0, 4), (1, 4)),# guzuta
                    ((0, 6), (1, 6)),# nige
                    ((0, 5), (1, 5)),# esa
                    ((2, 0), (2, 1)),# eye
                    (
                        (2, 4), (2, 5), # items
                        (3, 5), (2, 6), 
                        (3, 6)
                    ),
                    ((3, 0), (3, 1)), # normalkabe
                    ((2, 2), (2, 3)), # tokushukabe
                    [(3, 3)] # None
                    )
  
    def __call__(self,_type):
        units = []
        for pos_list in self.pos[_type]:
            units.append(get_unit(pos_list[0],pos_list[1]))
        
        for unit in units:
            print(unit.get_colorkey)
        return units


def get_unit_size(size=20):
    return size

def get_display_size(x=30, y=35, unit_size=24):
    unit_size = get_unit_size(unit_size)
    return [unit_size, (unit_size*x, unit_size*y)]

def get_image(file_name):
    main_path = os.getcwd()
    file_path = os.path.join(main_path, file_name)
    return file_path

def get_unit(x,y):
    image = pygame.image.load(get_image('pac-man.png'))
    colorkey = image.get_at((0,0))
    ret = image.subsurface(x*24, y*24, 24, 24)
    ret.set_colorkey(colorkey,RLEACCEL)
    
    return ret

# メイン関数---
def main():
    display_size = get_display_size()[1]
    pygame.init()
    pygame.display.set_mode(display_size, pygame.RESIZABLE)
    display = pygame.display.get_surface()
    
    stage = Stage(display)
    pos = POS(stage,display)
    pacman = Chara(0, pos)
    aka = Chara(1,pos)
    pink = Chara(2,pos)
    ao = Chara(3,pos)
    guzu = Chara(4, pos)

    while(1):
        display.fill((24,24,24))
        stage.blit()
        pacman(display)
        aka(display)
        pink(display)
        ao(display)
        guzu(display)
        pygame.time.wait(30)
        

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    




# ---
if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    main()
