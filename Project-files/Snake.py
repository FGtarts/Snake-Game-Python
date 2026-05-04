import pygame,sys,random
from pygame.math import Vector2

pygame.init()

GREEN = (173,204,96)
DARK_GREEN = (43,51,24)
RED = (166,33,29)

CELL_SIZE = 30
NUMBER_OF_CELLS = 25

class Food:
    def __init__(self):
        self.positon = self.generate_random_pos()

    def draw(self):
        food_rect = pygame.Rect(self.positon.x * CELL_SIZE, self.positon.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(food_surface, food_rect)

    def generate_random_pos(self):
        x =  random.randint(0,NUMBER_OF_CELLS-1)
        y =  random.randint(0,NUMBER_OF_CELLS-1)
        positon = Vector2(x,y)
        return positon

class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)

    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen,DARK_GREEN,segment_rect,0,5)
    
    def update(self):
        self.body = self.body[:-1]
        self.body.insert(0, self.body[0]+self.direction)


screen  = pygame.display.set_mode((CELL_SIZE * NUMBER_OF_CELLS, CELL_SIZE * NUMBER_OF_CELLS))

pygame.display.set_caption("Retro Snake Game")

clock = pygame.time.Clock()

food = Food()
snake = Snake()
food_surface = pygame.image.load("Project-files/Graphics/apple.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,200)


while True:
    for event in pygame.event.get():

        if event.type == SNAKE_UPDATE:
            snake.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != Vector2(0,1):
                snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and snake.direction != Vector2(0,-1):
                snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT and snake.direction != Vector2(-1,0):
                snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT and snake.direction != Vector2(1,0):
                snake.direction = Vector2(-1,0)


    #DRAWING THE OBJECTS
    screen.fill(GREEN)
    food.draw()
    snake.draw()

    pygame.display.update()
    clock.tick(60)