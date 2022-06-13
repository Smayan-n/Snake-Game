#AUTHOR: Smayan Nirantare

import pygame, sys, random, time
pygame.init()

#grid class
class Grid():
    def __init__(self):
        self.new_screen_height = ROWS * CELL_SIZE
        self.new_screen_width =  COLS * CELL_SIZE

        pygame.display.set_mode((self.new_screen_width, self.new_screen_height))
    
    def drawGrid(self):
        #horizontal lines
        for y in range(ROWS):
            pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (self.new_screen_width, y * CELL_SIZE), 1)

        #vertical lines
        for x in range(COLS):
            pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, self.new_screen_height), 1)


class Snake():
    def __init__(self):

        #stores current position of snake head
        self.row = 5
        self.col = 5

        #direction of snake
        self.dirx = 0
        self.diry = 0
        
        self.food_x, self.food_y, self.food_row, self.food_col = self.getFoodPos()

        #snake elements
        #stores a tuple of (row, col) of each section of the snake
        self.snake_body = []
        #current length of snake(also used as score)
        self.snake_length = 1
  
    def draw(self):
        self.handleSnakeLength()
        #each section is one box of the snake
        for i, section in enumerate(self.snake_body):
            #calculates corresponding x, y coords for cell depending on row and col
            snake_x = section[1] * CELL_SIZE + 1
            snake_y = section[0] * CELL_SIZE + 1
            
            section = (snake_x, snake_y, CELL_SIZE - 1, CELL_SIZE - 1)

            #making the head of the snake Dark green and drawing eyes
            color = GREEN
            if i == len(self.snake_body) - 1:
                color = DARK_GREEN
            
            pygame.draw.rect(screen, color, section)

        #drawing food
        pygame.draw.rect(screen, RED, (self.food_x, self.food_y, CELL_SIZE - 1, CELL_SIZE - 1))

    #handles snakes length and growth
    def handleSnakeLength(self):

        #increasing the snake's length
        snake_head = []
        snake_head.append(self.row)
        snake_head.append(self.col)
        self.snake_body.append(snake_head)
        if len(self.snake_body) > self.snake_length:
            del self.snake_body[0]

        #checking for self collision
        if self.snake_body[-1] in self.snake_body[:-1]:
            self.reset()

        #checking for food collision
        if self.row == self.food_row and self.col == self.food_col:
            self.snake_length += 1
            self.food_x, self.food_y, self.food_row, self.food_col = self.getFoodPos()

        
    #calculates food pos at random location and returns it
    def getFoodPos(self):
        food_col = random.randint(0, COLS - 1) 
        food_row = random.randint(0, ROWS - 1)
        food_x = food_col * CELL_SIZE + 1
        food_y = food_row * CELL_SIZE + 1
        
        return food_x, food_y, food_row, food_col

    #resetting snake if player looses
    def reset(self):
        pygame.time.delay(400)
        game_over_lbl = FONT2.render("Game Over", True, RED)
        screen.blit(game_over_lbl, (SCREEN_WIDTH / 2 - game_over_lbl.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_lbl.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(1000)

        self.dirx = 0
        self.diry = 0
        self.snake_length = 1
        self.snake_body.clear()

        self.row = 5
        self.col = 5

        self.food_x, self.food_y, self.food_row, self.food_col = self.getFoodPos()


def drawGameWin():

    screen.fill(WHITE)
    grid.drawGrid()
    snake.draw()

    #score label
    score_lbl = FONT1.render("Score: " + str(snake.snake_length), True, RED)
    screen.blit(score_lbl, (5, 0))
    


def main():

    #main gameloop
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
       
        #getting key input and making sure that the snake can only move at 90 degrees (not 180)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.dirx != 1:
            snake.dirx = -1
            snake.diry = 0
            #snake.col += snake.dirx

        elif keys[pygame.K_RIGHT] and snake.dirx != -1:
            snake.dirx = 1
            snake.diry = 0
            #snake.col += snake.dirx

        elif keys[pygame.K_UP] and snake.diry != 1:
            snake.dirx = 0
            snake.diry = -1
            #snake.row += snake.diry

        elif keys[pygame.K_DOWN] and snake.diry != -1:
            snake.dirx = 0
            snake.diry = 1


        #snake's draw function is done here to resuce input lag
        #changing snake's direction based on key input

        #moving snake
        snake.col += snake.dirx
        snake.row += snake.diry

        #if snake goes outside of grid, it will appear on the opposite side
        if snake.col == COLS:
            snake.col = 0
        if snake.row == ROWS:
            snake.row = 0
        
        if snake.col == -1:
            snake.col = COLS - 1
        if snake.row == -1:
            snake.row = ROWS - 1

        drawGameWin()
        #handles game fps and update
        clock.tick(12)
        pygame.display.update()
        


#constants
CELL_SIZE = 30
ROWS = 15
COLS = 15

SCREEN_WIDTH = ROWS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FONT1 = pygame.font.SysFont("comicsansms", 20)
FONT2 = pygame.font.SysFont("comicsansms", 80)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game!")
clock = pygame.time.Clock()


grid = Grid()
snake = Snake()


if __name__ == '__main__':
   main()
