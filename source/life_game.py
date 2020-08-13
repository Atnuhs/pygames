
import random
import sys

import pygame
from pygame.locals import *


def get_color(_type, saturation=6):
    #0:black, 1:red, 2:green, 3:blue, 4:white, 5,orange
    #6:pink,  7:yellowgreen
    sat_list = [0,63,127,159,199,139,255]
    type_list = ([0,0,0],[1,0,0],[0,1,0],
                [0,0,1],[1,1,1],[1,0.5,0],
                [1,0,0.5],[0.5,1,0],[0,1,0.5],
                 [0.5,0,1],[0,0.5,1])
    return [(i)*sat_list[saturation] for i in type_list[_type]]

class Figure:
    def __init__(self, screen, unit, unit_num, menu_height=30, state_w=100):
        self.screen = screen
        self.unit = unit
        self.menu_h = menu_height
        self.un_w = unit_num[0]
        self.un_h = unit_num[1]
        self.font_size = 30
        self.color = get_color(2)
        self.menu_color = get_color(2,5)
        self.text_color = get_color(4,1)
        self.accelarate = 1
        self.black = get_color(0,0)
        self.gray = get_color(4,4)
        self.state_menu_h = self.screen.get_height()
        self.state_menu_pos_x = self.screen.get_width() - state_w+8
        self.stats = [0,0,0,0,10,0]
        self.message_list = ['time','state','edge','life num','speed']
        self.stats_message = [0,['move','stop'], ['normal', 'roop'], 0,['o','x']]
        self.font = pygame.font.Font(None, self.font_size)
            
    def draw_message(self,message="None", pos=0, color=0,sat=6):
        text = self.font.render(message, True, self.text_color)
        self.screen.blit(text, self.get_message_pos(pos))
    
    def draw_side_message(self, message="None", pos=0,color=4,sat=1):
        text = self.font.render(message, True, self.text_color)
        self.screen.blit(text, self.get_stat_message_pos(pos))
    
    def draw_button(self, pos, col, sat=6,sat2=5):
        pygame.draw.rect(self.screen, get_color(col, sat),
                         Rect(self.get_button_pos(pos)[1]))
        pygame.draw.rect(self.screen, get_color(col,sat2), 
            Rect(self.get_button_pos(pos)[0]),2)
    
    def get_stat_message_pos(self,pos):
        return (self.state_menu_pos_x, self.menu_h+1+20*pos+10, 30, 30)
        
    def get_message_pos(self, pos):
        return (30*pos+5, 5, 30, 30)
    
    def get_button_pos(self, pos):
        return ((30*pos, 0, 30, self.menu_h),
                (30*pos+1, 1, 28, self.menu_h-2))

    def draw_menu(self):
        menu_w = self.un_w*self.unit
        menu_h = self.menu_h
        pygame.draw.rect(self.screen,self.menu_color, 
            Rect(0,0,menu_w, menu_h))
        self.draw_message("move / stop",1,4,4)
        self.draw_button(0,4,4)
        self.draw_message(self.stats_message[4][self.stats[1]], 0, 4)
        for i in range(10):
            self.draw_button(i+6,i+1)
        self.draw_config_buttons()
        self.draw_state_menu()
    
    def draw_state_menu(self):
        pygame.draw.rect(self.screen, self.menu_color, Rect(self.state_menu_pos_x-8, self.menu_h+1, 100, self.state_menu_h))
        pygame.draw.rect(self.screen, (224,224,224), Rect(
            self.state_menu_pos_x-5, self.menu_h+4, 94, self.state_menu_h-200))
        self.support_state_message(0,1)
        self.support_state_message(3,0)
        self.support_state_message(6,0)
        self.support_state_message(9,1)
        self.support_state_message(12,1)

    def support_state_message(self, _pos, _type):
        p = int(_pos/3)
        self.draw_side_message(message=self.message_list[p], pos=_pos)
       
        if _type == 0:
            self.draw_side_message(
            message='>'+self.stats_message[p][self.stats[p]], pos=_pos+1)
        
        elif _type == 1:
            self.draw_side_message(
                message='>'+str(self.stats[p]), pos=_pos+1)

        

    def draw_black_unit(self, x, y):
        u = self.unit
        pygame.draw.rect(self.screen, self.black, # outer
                         Rect((x-1)*u, (y-1)*u+self.menu_h, u, u))
        pygame.draw.rect(self.screen, self.gray,# inner
                         Rect((x-1)*u, (y-1)*u+self.menu_h, u, u), 1)
        
    def draw_color_unit(self, x, y):
        u = self.unit
        pygame.draw.rect(self.screen, self.color, # outer
                         Rect((x-1)*u, (y-1)*u+self.menu_h, u, u))
        pygame.draw.rect(self.screen, self.gray, # inner
                         Rect((x-1)*u, (y-1)*u+self.menu_h, u, u), 1)
    
    def color_change(self, color):
        color -= 5
        self.color = get_color(color)
        self.menu_color = get_color(color,5)
        if color >= 9:
            color -= 9
        self.text_color = get_color(color+2,1)
    
    def draw_config_buttons(self):
        self._draw_scene_button()
        self._draw_edge_button()
        self._draw_acceleration_button()
        self._draw_crear_button()
        self._draw_speed_buton()

    def _draw_scene_button(self):
        self.draw_button(17,4,5,3)
        self.draw_message(">",17.2,4,6)

    def _draw_edge_button(self):
        self.draw_button(18,4,5,3)
        self.draw_message("L",18.2,4,6)

    def _draw_acceleration_button(self):
        self.draw_button(19,4,5,3)
        self.draw_message(">>", 19, 4, 6)
        self.draw_message("x"+str(self.accelarate), 20,4,6)
    
    def _draw_crear_button(self):
        self.draw_button(22,4,5,3)
        self.draw_message("C",22,4)
    
    def _draw_speed_buton(self):
        self.draw_button(23,4,5,3)
        self.draw_message("S",23,4)


class System:
    def __init__(self, figure):
        self.figure = figure
        self.screen = figure.screen
        self.unit = figure.unit
        self.unit_num = (figure.un_w,figure.un_h)
        self.current_status = [
            [0 for i in range(self.unit_num[1]+2)] 
            for j in range(self.unit_num[0]+2)]
        self.menu_h = figure.menu_h
        self.wait_time = 0
        self.time = 0
        self.rule = [3, 1, 4] # birth, depopulation, population
        self.stop = False
        self.accelarate = 1
        self.edgemode = 0
        self.game_time = 0

    def draw_status(self):
        # current_statusを描画
        life_num = 0
        _len1 = len(self.current_status)-1
        _len2 = len(self.current_status[0])-1
        for x in range(1,_len1):
            for y in range(1,_len2):
                if self.current_status[x][y] == 0:
                    self.figure.draw_black_unit(x,y)
                elif self.current_status[x][y] == 1:
                    life_num += 1
                    self.figure.draw_color_unit(x,y)
        self.figure.stats[3] = life_num
        self.figure.draw_menu()
    
    def advance(self):
        self.time += 1
        if self.time > self.wait_time:
            self.time = 0
            self.stat_update()
        else:
            pass
        
    def stat_update(self):
        if self.stop:
            return

        for i in range(self.accelarate):
            w = len(self.current_status)-1
            h = len(self.current_status[0])-1

            if self.edgemode:
                for row in self.current_status:
                    row[0] = row[h-1]
                    row[h] = row[1]
                self.current_status[0] = self.current_status[w-1]
                self.current_status[w] = self.current_status[1]

            new_stat = [x[:] for x in self.current_status]
            for x in range(1,w):
                for y in range(1,h):
                    if self.current_status[x][y] == 0:
                        if self.is_birth(x,y):
                            new_stat[x][y] = 1
                    elif self.current_status[x][y] == 1:
                        if not self.is_survival(x,y):
                            new_stat[x][y] = 0
            self.current_status = new_stat
            self.game_time += 1
        self.figure.stats[0] = self.game_time
                
    def is_birth(self,x,y):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx==0 and dy==0:
                    continue
                if self.current_status[x+dx][y+dy] == 1:
                    count += 1
                    if count > self.rule[0]:
                        return False
        if count != self.rule[0]:
            return False
        else:
            return True
    
    def is_survival(self,x,y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx==0 and dy==0:
                    continue
                if self.current_status[x+dx][y+dy] == 1:
                    count += 1
                    if count >= self.rule[2]:
                        return False
        if count <= self.rule[1]:
            return False
        return True

    def change_scene_mode(self):
        if not self.stop:
            self.stat_update()
            self.stop = True
        else:
            self.stop = False
            self.stat_update()
            self.stop = True
    
    def change_acceleration_mode(self):
        if self.accelarate > 20:
            self.accelarate = 1
        else:
            self.accelarate += 1
        
        self.figure.accelarate = self.accelarate
    
    def change_edge_mode(self):
        self.edgemode = 1 - self.edgemode
        self.figure.stats[2] = self.edgemode
    
    def init_stat(self):
        self.game_time = 0
        self.current_status = [
            [0 for i in range(self.unit_num[1]+2)]
            for j in range(self.unit_num[0]+2)]

    def change_speed(self):
        scale =2
        self.wait_time -= scale
        if self.wait_time < 0:
            self.wait_time = 10*scale
        self.figure.stats[4] = int((10*scale - self.wait_time)/scale)+1

    def draw_in_mouse(self, x, y, mouse):
        mx,my = x/30,y/30
        if my < 1:
            mx = int(mx)
            if mx == 0:
                self.stop = False
                self.figure.stats[1] = 1-self.figure.stats[1]
                return False
            elif 6 <= mx <= 15:
                self.figure.color_change(mx)
                return True
            elif 16 < mx <= 17:
                self.change_scene_mode()
                return True
            elif 17 < mx <= 18:
                self.change_edge_mode()
                return True
            elif 18 < mx <= 19:
                self.change_acceleration_mode()
                return True
            elif 21 < mx <= 22:
                self.init_stat()
                return True
            elif 22 < mx <= 23:
                self.change_speed()
                return True
            else:
                return True

        x, y = (x)/self.unit, (y-self.menu_h)/self.unit
        if 0< x < self.unit_num[0] and 0 < y < self.unit_num[1]:
            self.current_status[int(x)+1][int(y)+1] = mouse
            return True


# メイン関数
def main():
    pygame.init()
    unit = 20
    unit_num = (40,30)
    menu_height = 30
    state_w = 100
    screen_size = (unit_num[0]*unit+state_w, unit_num[1]*unit+menu_height)
    screen = pygame.display.set_mode(screen_size)
    figure = Figure(screen, unit, unit_num, menu_height=menu_height)
    stop = False
    system = System(figure)

    while (1):
        pygame.time.wait(10)
        screen.fill((0,0,0))
        system.draw_status()
        pygame.display.update()
        if not stop:
            system.advance()
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = event.pos
                    if not system.draw_in_mouse(x,y,1):
                        if stop:
                            stop = False
                        else:
                            stop = True

              
                if event.button == 3:
                    x,y = event.pos
                    if not system.draw_in_mouse(x,y,0):
                        if stop:
                            stop = False
                        else:
                            stop = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_t:
                    figure.stats[1] = 1-figure.stats[1]
                    system.stop = False
                    if stop:
                        stop = False
                    else:
                        stop = True
                elif event.key == K_l:
                    system.change_edge_mode()
                elif event.key == K_c:
                    system.init_stat()
                elif event.key == K_s:
                    system.change_speed() 
                
if __name__ == "__main__":
    main()
