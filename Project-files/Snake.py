import pygame,sys,random
from pygame.math import Vector2

pygame.init()

#COLORS
GREEN = (173,204,96)
DARK_GREEN = (43,51,24)
RED = (166,33,29)

#DIMENSIONS
CELL_SIZE = 30
NUMBER_OF_CELLS = 25

#CLASSES
class Food:
    def __init__(self, snake_body):
        self.positon = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(self.positon.x * CELL_SIZE, self.positon.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x =  random.randint(0,NUMBER_OF_CELLS-1)
        y =  random.randint(0,NUMBER_OF_CELLS-1)
        return Vector2(x,y)

    def generate_random_pos(self, snake_body):
        positon = self.generate_random_cell()
        while positon in snake_body:
            positon = self.generate_random_cell()
        return positon
class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen,DARK_GREEN,segment_rect,0,5)
    
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_border()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.positon:
            print("NOM NOM NOM")
            self.food.positon = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True

    def check_collision_with_border(self):
        if self.snake.body[0].x == NUMBER_OF_CELLS or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == NUMBER_OF_CELLS or self.snake.body[0].y == -1:
            self.game_over()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.positon = self.food.generate_random_pos(self.snake.body)
        self.state = "PAUSED"

#SCREEN STUFF
screen  = pygame.display.set_mode((CELL_SIZE * NUMBER_OF_CELLS, CELL_SIZE * NUMBER_OF_CELLS))
pygame.display.set_caption("Retro Snake Game")
clock = pygame.time.Clock()

#MORE STUFF
game = Game()
food_surface = pygame.image.load("Project-files/Graphics/apple.png")
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,200)


#MAIN GAME LOOP
while True:
    for event in pygame.event.get():

        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if game.state == "PAUSED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
                game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    #DRAWING THE OBJECTS
    screen.fill(GREEN)
    game.draw()
    game.draw()

    #OTHER STUFF
    pygame.display.update()
    clock.tick(60)