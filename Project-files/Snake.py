import pygame,sys,random
from pygame.math import Vector2

pygame.init()

GREEN = (173,204,96)
DARK_GREEN = (43,51,24)
RED = (166,33,29)

CELL_SIZE = 30
NUMBER_OF_CELLS = 20

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
    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen,DARK_GREEN,segment_rect,0,5)
    


screen  = pygame.display.set_mode((CELL_SIZE * NUMBER_OF_CELLS, CELL_SIZE * NUMBER_OF_CELLS))

pygame.display.set_caption("Retro Snake Game")

clock = pygame.time.Clock()

food = Food()
food_surface = pygame.image.load("Project-files/Graphics/apple.png")

snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(GREEN)
    food.draw()
    snake.draw()

    pygame.display.update()
    clock.tick(60)
    
