import pygame,sys,random
from pygame.math import Vector2

pygame.init()

#FONTS
title_font = pygame.font.Font(None,60)
score_display = pygame.font.Font(None,40)
high_score_display = pygame.font.Font(None,40)
developer_display = pygame.font.Font(None,40)

#COLORS
GREEN = (173,204,96)
SLIGHTLY_DARKER_GREEN = (150, 180, 85)
DARK_GREEN = (43,51,24)
RED = (166,33,29)

#DIMENSIONS
CELL_SIZE = 30
NUMBER_OF_CELLS = 20
OFFSET = 75

#CLASSES
class Food:
    def __init__(self, snake_body):
        self.positon = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.positon.x * CELL_SIZE, OFFSET + self.positon.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
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
        self.direction_queue = []
        self.eating_sound = pygame.mixer.Sound("Project-files/Sounds/eating.mp3")
        self.collision_sound = pygame.mixer.Sound("Project-files/Sounds/collision.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen,DARK_GREEN,segment_rect,0,5)
    
    def update(self, grow=False):
        self.body.insert(0, self.body[0] + self.direction)
        if not grow:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.direction_queue = []

    def queue_direction(self, new_direction):
        reference_direction = self.direction_queue[-1] if self.direction_queue else self.direction
        if new_direction == reference_direction:
            return
        if new_direction + reference_direction == Vector2(0,0):
            return
        if len(self.direction_queue) < 2:
            self.direction_queue.append(new_direction)

    def apply_queued_direction(self):
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.high_score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.apply_queued_direction()
            next_head = self.snake.body[0] + self.snake.direction
            will_grow = next_head == self.food.positon

            if self.check_collision_with_border(next_head):
                return
            if self.check_collision_with_tail(next_head, will_grow):
                return

            self.snake.update(grow=will_grow)
            if will_grow:
                self.snake.eating_sound.play()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                self.food.positon = self.food.generate_random_pos(self.snake.body)

    def reset_game(self):
        self.snake.reset()
        self.food.positon = self.food.generate_random_pos(self.snake.body)
        self.score = 0
        self.state = "RUNNING"

    def check_collision_with_border(self, position):
        if position.x < 0 or position.x >= NUMBER_OF_CELLS:
            self.snake.collision_sound.play()
            self.game_over()
            return True
        if position.y < 0 or position.y >= NUMBER_OF_CELLS:
            self.snake.collision_sound.play()
            self.game_over()
            return True
        return False

    def check_collision_with_tail(self, next_head, will_grow):
        body_to_check = self.snake.body if will_grow else self.snake.body[:-1]
        if next_head in body_to_check:
            self.snake.collision_sound.play()
            self.game_over()
            return True
        return False

    def game_over(self):
        self.state = "GAME_OVER"

#SCREEN STUFF
screen  = pygame.display.set_mode((2 * OFFSET + CELL_SIZE * NUMBER_OF_CELLS, 2 * OFFSET + CELL_SIZE * NUMBER_OF_CELLS))
pygame.display.set_caption("Retro Snake Game")
clock = pygame.time.Clock()

#INITIALIZATION AND CUSTOM EVENTS AND STUFF
game = Game()
food_surface = pygame.image.load("Project-files/Graphics/apple.png")
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,175)
snake_length = len(game.snake.body)

#MAIN GAME LOOP
while True:
    for event in pygame.event.get():

        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            #GAME STATE CONTROL
            if event.key == pygame.K_SPACE:
                if game.state == "RUNNING":
                    game.state = "PAUSED"
                elif game.state == "PAUSED":
                    game.state = "RUNNING"
            if event.key == pygame.K_r and game.state == "GAME_OVER":
                game.reset_game()

            #SNAKE DIRECTION CONTROL
            if game.state == "RUNNING":
                if event.key in (pygame.K_UP, pygame.K_w):
                    game.snake.queue_direction(Vector2(0,-1))
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    game.snake.queue_direction(Vector2(0,1))
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.snake.queue_direction(Vector2(1,0))
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    game.snake.queue_direction(Vector2(-1,0))

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #DRAWING THE OBJECTS
    screen.fill(GREEN)
    pygame.draw.rect(screen,DARK_GREEN,(OFFSET - 5,OFFSET - 5,CELL_SIZE * NUMBER_OF_CELLS + 10,CELL_SIZE * NUMBER_OF_CELLS + 10),5)

    #DRAWING THE GRID
    for row in range(NUMBER_OF_CELLS):
        for col in range(NUMBER_OF_CELLS):
            grid_cell_color = GREEN if (row + col) % 2 == 0 else SLIGHTLY_DARKER_GREEN
            grid_cell_rect = (OFFSET + col * CELL_SIZE, OFFSET + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid_cell_color, grid_cell_rect)

    #TEXT AND SCORE DISPLAY
    game.draw()

    title_surface = title_font.render("Retro Snake", True, RED)
    screen.blit(title_surface,(OFFSET-5, 20))

    score_surface = score_display.render("SCORE:" + str(game.score).zfill(3),True,RED)
    screen.blit(score_surface,(OFFSET + CELL_SIZE * NUMBER_OF_CELLS - 150, 35))

    high_score_surface = high_score_display.render("HIGH SCORE: " + str(game.high_score).zfill(3), True, RED)
    screen.blit(high_score_surface, (CELL_SIZE * NUMBER_OF_CELLS - 160, OFFSET + CELL_SIZE * NUMBER_OF_CELLS + 10))

    developer_surface = developer_display.render("By Frogtarts", True, RED)
    screen.blit(developer_surface, (OFFSET - 5, OFFSET + CELL_SIZE * NUMBER_OF_CELLS + 10))

    #GAME STATE DETAILS
    if game.state == "PAUSED":
        paused_surface = score_display.render("GAME PAUSED", True, RED)
        paused_rect = paused_surface.get_rect(center=(OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2, OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2 - 20))
        screen.blit(paused_surface, paused_rect)

        hint_surface = developer_display.render("Press SPACE to continue", True, RED)
        hint_rect = hint_surface.get_rect(center=(OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2, OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2 + 20))
        screen.blit(hint_surface, hint_rect)

    if game.state == "GAME_OVER":
        game_over_surface = score_display.render("GAME OVER", True, RED)
        game_over_rect = game_over_surface.get_rect(center=(OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2, OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2 - 20))
        screen.blit(game_over_surface, game_over_rect)

        restart_surface = developer_display.render("Press R to restart", True, RED)
        restart_rect = restart_surface.get_rect(center=(OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2, OFFSET + (CELL_SIZE * NUMBER_OF_CELLS) // 2 + 20))
        screen.blit(restart_surface, restart_rect)

    #OTHER STUFF
    pygame.display.update()
    clock.tick(60)