import sys
from math import sqrt
from random import randint
import time
from PIL import Image, ImageDraw, ImageFont
import setup
import random

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

WIDTH = 12
HEIGHT = 22
INTERVAL = 40
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), \
          (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
GRID_COLOR="#080404"
BLOCK = None
NEXT_BLOCK = None
PIECE_SIZE = 9 # 9x9
PIECE_GRID_SIZE = PIECE_SIZE+1 
BLOCK_DATA = (
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)

class Block:
    """ About block """
    def __init__(self, count):
        self.turn = randint(0, 3)
        self.type = BLOCK_DATA[randint(0, 6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = randint(2, 8 - self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL
 
    def update(self, count):
        """ Update block state (return erased row amount) """
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            for y_offset in range(BLOCK.size):
                for x_offset in range(BLOCK.size):
                    if 0 <= self.ypos+y_offset < HEIGHT and \
                       0 <= self.xpos+x_offset < WIDTH:
                        index = y_offset * self.size + x_offset
                        val = BLOCK.data[index]
                        if val != 0:
                            FIELD[self.ypos+y_offset][self.xpos+x_offset] = val
 
            erased = erase_line()
            go_next_block(count)
 
        if self.fire < count:    #Control drop speed
            self.fire = count + INTERVAL
            self.ypos += 1
        return erased
 
    def draw(self):
        """ Draw block """
        for index in range(len(self.data)):
            
            xpos = index % self.size
            ypos = index // self.size
            
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
                0 <= xpos + self.xpos < WIDTH and val != 0:
                ## f_xpos : calculated on field area
                f_xpos = PIECE_GRID_SIZE + (xpos + self.xpos) * PIECE_GRID_SIZE
                f_ypos = PIECE_GRID_SIZE + (ypos + self.ypos) * PIECE_GRID_SIZE
                
                draw_rect(f_xpos, f_ypos, 0, val)

def draw_rect(f_xpos, f_ypos, outline_color, val): #(x, y, outline color, block color)
    setup.draw.rectangle((f_xpos, f_ypos,
                          f_xpos + PIECE_SIZE, f_ypos + PIECE_SIZE),
                          outline=outline_color , fill=COLORS[val])

def erase_line():
    erased = 0
    ypos = HEIGHT-2
    #print(FIELD[ypos])
    while ypos >=0:
        if  all(FIELD[ypos]) == True:
            del FIELD[ypos]
            FIELD.insert(0, [8, 0,0,0,0,0,0,0,0,0,0 ,8])
            erased += 1
        else:
            ypos -= 1
    return erased
 
def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2
 
def go_next_block(count):
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)
 
def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            index = y_offset * BLOCK.size + x_offset
            val = data[index]

            if 0 <= xpos+x_offset < WIDTH and \
                0 <= ypos+y_offset < HEIGHT:
                if val != 0 and \
                    FIELD[ypos+y_offset][xpos+x_offset] != 0:
                    return True
    return False
 
def set_game_field():
    for i in range(HEIGHT-1):
        FIELD.insert(0, [8, 0,0,0,0,0,0,0,0,0,0 ,8])
    
    FIELD.insert(HEIGHT-1, [8, 8,8,8,8,8,8,8,8,8,8 ,8])
    
 
def draw_game_field():
    for y_offset in range(HEIGHT):
        for x_offset in range(WIDTH):
            val = FIELD[y_offset][x_offset]
            f_xpos = PIECE_GRID_SIZE + x_offset*PIECE_GRID_SIZE
            f_ypos = PIECE_GRID_SIZE + y_offset*PIECE_GRID_SIZE
            #!!
            if val == 0:
                draw_rect(f_xpos, f_ypos, GRID_COLOR, val)
            else:
                draw_rect(f_xpos, f_ypos, 0, val)

def draw_current_block():
    BLOCK.draw()
 
def draw_next_block():
    for y_offset in range(NEXT_BLOCK.size):
        for x_offset in range(NEXT_BLOCK.size):
            index = y_offset * NEXT_BLOCK.size + x_offset
            val = NEXT_BLOCK.data[index]
            if val != 0:
                f_xpos = 175 + (x_offset) * PIECE_GRID_SIZE
                f_ypos = 70 + (y_offset) * PIECE_GRID_SIZE
                #!!
                draw_rect(f_xpos, f_ypos, 0, val)

def draw_score(score):
    score_str = str(score).zfill(6)
    setup.draw.text((180, 10), score_str, font=setup.small_fnt, fill="#FFFFFF")
    #show text on diplay

def draw_gameover_message():
    #same like score
    rcolor = tuple(int(x*255) for x in setup.hsv_to_rgb(random.random(), 1, 1))
    setup.draw.text((32, 105), "GAME OVER", font=setup.large_fnt, fill=rcolor)

def runGame():
    """ main func"""
    global INTERVAL
    count = 0
    score = 0
    signal = False
    game_over = False
    
    go_next_block(INTERVAL)
 
    set_game_field()
 
    while True:
        
        game_over = is_game_over()      
        if not game_over:
            count += 5
            #Interval decreased = Faster drop speed
            if count % 1000 == 0:
                INTERVAL = max(1, INTERVAL - 2)
            erased = BLOCK.update(count)

            #Erasing more line at once, more score received
            if erased > 0:
                score += (2 ** erased) * 100

            #key event
            next_x, next_y, next_t = \
                BLOCK.xpos, BLOCK.ypos, BLOCK.turn
            
            if not setup.button_B.value:
                next_t = (next_t + 1) % 4
            if not setup.button_R.value:
                next_x += 1
            if not setup.button_L.value:
                next_x -= 1
            if not setup.button_D.value:
                next_y += 1
            #!!
            if not is_overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]
 
        # Game Field
        draw_game_field()
 
        # Draw current dropping block
        draw_current_block()
 
        # Draw next block
        draw_next_block()
        
        # Show score
        draw_score(score)
        
        # Show GAMEOVER message
        if game_over:
            draw_gameover_message()
 
        setup.disp.image(setup.image)
        setup.bg_black()
        time.sleep(0.01)
runGame()
sys.quit()