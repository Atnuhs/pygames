import pygame
from pygame.locals import *
import sys

class Game:
    def __init__(self):
        pass

    def start(self, display, logic):
        while(True):

            for event in pygame.event.get(): # 終了処理
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
            if event.type == MOUSEBUTTONDOWN \
            and event.button == 1:
                logic.put_stone(display.to_pos(event.pos))
                game_stat = logic.pass_check()
                display.show(logic)
                if game_stat == "game_over":
                    print("game over")
                    display.game_over(logic)



class Display:
    def __init__(self,logic):
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))
        self.font = pygame.font.Font(None, 32)
        pygame.display.set_caption("Othello")
        self.show(logic)


    def show_stone(self,stone,x,y):
        if stone == 0: return
        if stone == 1:
            pygame.draw.ellipse(self.screen, (16,16,16), Rect(x,y,32,32))
        else:
            pygame.draw.ellipse(self.screen, (240,240,240), Rect(x,y,32,32))
        pygame.draw.ellipse(self.screen, (64,64,64), Rect(x,y,32,32), 2)
    
    def show_board(self,board):
        for i in range(8):
            for j in range(8):
                x = 32*j+10
                y = 32*i+10
                pygame.draw.rect(self.screen,(0,196,0),Rect(x,y,32,32))
                pygame.draw.rect(self.screen,(32,32,32),Rect(x,y,32,32),1)
                self.show_stone(board[i][j],x,y)
    
    def show_stat(self,count,turn):
        black,white = count
        count_stat = self.font.render(f"black: {black}, whilte: {white}", True, (32,64,64))
        self.screen.blit(count_stat,[20,272])
        turn_stat = self.font.render(f"turn: {turn}", True, [128,128,32])
        self.screen.blit(turn_stat,[20,288])



    
    def show(self,logic):
        self.screen.fill((200,100,100))
        self.show_board(logic.get_board())
        self.show_stat(logic.count_stone(), logic.turn_of())
        pygame.display.update()
    
    def to_pos(self, pos):
        x,y = pos
        return int((x-10)/32), int((y-10)/32)
    
    def game_over(self,logic):
        b,w = logic.count_stone()
        if b > w:
            result = "black won"
        elif w > b:
            result = "white won"
        else:
            result = "draw"
        
        result_f = self.font.render(result, True, [16,16,64])
        self.screen.blit(result_f,[20,304])
        pygame.display.update()


class Logic:
    def __init__(self):
        self.board = [[0 for i in range(10)] for j in range(10)]
        self.board[4][4:6] = [1,2]
        self.board[5][4:6] = [2,1]
        self.turn = 1

    def get_board(self):
        return [[self.board[j][i] for i in range(1,9)] for j in range(1,9)]

    def count_stone(self):
        black,white=0,0
        for i in range(1,9):
            for j in range(1,9):
                if self.board[i][j] == 1:
                    black+=1
                elif self.board[i][j] == 2:
                    white+=1
        return black, white

    def sub_can_put(self,y,x,dy,dx):
        nx, ny = x+dx, y+dy
        ret = []
        if self.board[ny][nx] != 3-self.turn: return []
        while self.board[ny][nx] == 3-self.turn:
            ret.append([nx,ny])
            nx,ny = nx+dx,ny+dy
        if self.board[ny][nx] != self.turn: return []
        return ret

    def can_put(self, y, x):
        change_pos = []
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                if dx==dy==0: continue
                change_pos += self.sub_can_put(y,x,dy,dx)
        return change_pos

    def put_stone(self, pos):
        x,y=pos
        if (x<0 or 7<x) or (y<0 or 7<y): return
        if self.board[y+1][x+1] != 0: return

        reverse = self.can_put(y+1,x+1)
        if reverse:
            self.board[y+1][x+1] = self.turn
            for rx,ry in reverse:
                self.board[ry][rx] = self.turn
            self.turn = 3 - self.turn
    
    def pass_check(self):
        if not self.turn_pass():
            self.turn=3-self.turn
            if not self.turn_pass():
                return "game_over"
            return "pass"
        return "in_game"

    def turn_pass(self):
        exist_put_pos = False
        for i in range(1,9):
            for j in range(1,9):
                if self.board[i][j] != 0: continue
                exist_put_pos = exist_put_pos or (self.can_put(i,j))
        return exist_put_pos
    
    def turn_of(self):
        ret = ["","black","white"]
        return ret[self.turn]




def main():
    logic = Logic()
    display = Display(logic)
    game = Game()
    game.start(display,logic)



if __name__ == "__main__":
    main()