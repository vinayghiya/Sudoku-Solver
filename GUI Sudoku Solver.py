import pygame
from sys import exit
import time

pygame.init()

class Cube:
    rows,cols=9,9

    def __init__(self,value,row,col,width,height):
        self.value=value
        self.temp=0
        self.row=row
        self.col=col
        self.width=width
        self.height=height
        self.selected=False

    def draw(self,screen):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp!=0 and self.value==0:
            text=fnt.render(str(self.temp),1,'Grey')
            screen.blit(text,(x+5,y+5))
        elif not(self.value==0):
            text=fnt.render(str(self.value),1,'Black')
            screen.blit(text,(x + (gap/2-text.get_width()/2),y + (gap/2-text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(screen,'Green',(x,y,gap,gap),3)

    def set(self,val):
        self.value=val

    def set_temp(self,val):
        self.temp=val

    def draw_change(self,screen,f=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(screen, 'White', (x, y, gap, gap), 0)
        text=fnt.render(str(self.value),1,'Black')
        screen.blit(text, (x + (gap/2 - text.get_height()/2), y + (gap/2 - text.get_height()/2)))

        if f:
            pygame.draw.rect(screen,'Green',(x,y,gap,gap),3)
        else:
            pygame.draw.rect(screen,'Red',(x,y,gap,gap),3)


class Grid:

    sudoku = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self,col,row,width,height,screen):
        self.row=row
        self.col=col
        self.width=width
        self.height=height
        self.cubes = [[Cube(self.sudoku[i][j], i, j, width, height) for j in range(self.col)] for i in range(self.row)]
        self.screen=screen
        self.model=None
        self.update_model()
        self.selected=None

    def update_model(self):
        self.model=[[self.cubes[i][j].value for j in range(self.col)]for i in range(self.row)]

    def place(self,val):
        rows,cols=self.selected
        if self.cubes[rows][cols].value==0:
            self.cubes[rows][cols].set(val)
            self.update_model()

            if isvalid(self.model,rows,cols,val):
                return True
            else:
                self.cubes[rows][cols].set(0)
                self.cubes[rows][cols].set_temp(0)
                self.update_model()
                return False

    def sketch(self,val):
        rows,cols=self.selected
        self.cubes[rows][cols].set_temp(val)

    def draw(self):

        gap=self.width/9
        for i in range(self.row+1):
            if i%3==0 and i!=0:
                thick=4
            else:
                thick=2
            pygame.draw.line(self.screen,'Black',(0,i*gap),(self.width,i*gap),thick)
            pygame.draw.line(self.screen,'Black',(i*gap,0),(i*gap,self.height),thick)

        for i in range(self.row):
            for j in range(self.col):
                self.cubes[i][j].draw(self.screen)

    def select(self,rows,cols):
        for i in range(self.row):
            for j in range(self.col):
                self.cubes[i][j].selected=False

        self.cubes[rows][cols].selected=True
        self.selected=(rows,cols)

    def clear(self):
        rows,cols=self.selected
        if self.cubes[rows][cols].value==0:
            self.cubes[rows][cols].set_temp(0)

    def click(self,x,y):
        if x<self.width and y<self.height:
            gap=self.width/9
            rows=x//gap
            cols=y//gap
            return (int(cols),int(rows))
        else:
            return None


    def is_finished(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.cubes[i][j].value==0:
                    return False
        return True

    def solve(self):
        self.update_model()
        empty=get_empty(self.model)
        if empty:
            rows,cols=empty
        else:
            return True

        for i in range(10):
            if isvalid(self.model,rows,cols,i):
                self.model[rows][cols]=i
                if self.solve():
                    return True;
                self.model[rows][cols]=0
        return False

    def gui_solve(self):

        self.update_model()
        empty=get_empty(self.model)

        if empty:
            rows,cols=empty
        else:
            return True

        for i in range(10):
            if isvalid(self.model,rows,cols,i):
                self.model[rows][cols]=i
                self.cubes[rows][cols].set(i)
                self.cubes[rows][cols].draw_change(self.screen,True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.gui_solve():
                    return True

                self.model[rows][cols]=0
                self.cubes[rows][cols].set(0)
                self.update_model()
                self.cubes[rows][cols].draw_change(self.screen,False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


def get_empty(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return (i,j)
    return None


def isvalid(sudoku,row,column,target):
    for i in range(9):
        if sudoku[row][i]==target and column!=i:
            return False
        else:
            continue

    for i in range(9):
        if sudoku[i][column]==target and row!=i:
            return False

    row_block=(row//3)*3
    col_block=(column//3)*3

    for i in range(3):
        for j in range(3):
            if sudoku[row_block+i][col_block+j]==target and row_block!=row and col_block!=column:
                return False

    return True


def redraw_win(screen,sudoku,time,strikes):
    screen.fill('White')
    fnt=pygame.font.SysFont('comicsans',20)
    text=fnt.render("Time: "+format_time(time),1,'black')
    screen.blit(text,(470,605))

    text=fnt.render("X "*strikes,1,'Red')
    screen.blit(text,(20,605))

    sudoku.draw()


def format_time(secs):
    sec=secs%60
    mins=secs//60
    hour=mins//60

    tm=" "+str(hour)+":"+str(mins)+":"+str(sec)
    return tm


def main():

    screen=pygame.display.set_mode((600,650))
    pygame.display.set_caption("Sudoku")
    sudoku=Grid(9,9,600,600,screen)
    key=None
    start=time.time()
    strikes=0

    while True:
        play_time=round(time.time()-start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1 or event.key==pygame.K_KP1:
                    key=1
                if event.key==pygame.K_2 or event.key==pygame.K_KP2:
                    key=2
                if event.key==pygame.K_3 or event.key==pygame.K_KP3:
                    key=3
                if event.key==pygame.K_4 or event.key==pygame.K_KP4:
                    key=4
                if event.key==pygame.K_5 or event.key==pygame.K_KP5:
                    key=5
                if event.key==pygame.K_6 or event.key==pygame.K_KP6:
                    key=6
                if event.key==pygame.K_7 or event.key==pygame.K_KP7:
                    key=7
                if event.key==pygame.K_8 or event.key==pygame.K_KP8:
                    key=8
                if event.key==pygame.K_9 or event.key==pygame.K_KP9:
                    key=9
                if event.key==pygame.K_DELETE:
                    key=None
                    sudoku.clear()
                if event.key==pygame.K_SPACE:
                    sudoku.gui_solve()
                if event.key==pygame.K_RETURN:
                    x,y=sudoku.selected
                    if sudoku.cubes[x][y].temp!=0:
                        if sudoku.place(sudoku.cubes[x][y].temp):
                            print("Success")
                        else:
                            print("Wrong")

                            strikes+=1
                        key=None

                        if sudoku.is_finished():
                            print("Game over")

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                clicked=sudoku.click(pos[0],pos[1])
                if clicked:
                    sudoku.select(clicked[0],clicked[1])
                    key=None

            if sudoku.selected and key!=None:
                sudoku.sketch(key)

            redraw_win(screen,sudoku, play_time, strikes)
            pygame.display.update()

        #pygame.display.update()

main()
