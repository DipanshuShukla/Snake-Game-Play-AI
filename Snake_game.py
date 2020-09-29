import pygame
import random

pygame.init()

WIN_WIDTH, WIN_HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake")

# Scaling
FPS = 18
SCALE = 14
WIDTH, HEIGHT = int(WIN_WIDTH / SCALE), int(WIN_HEIGHT / SCALE)

# color pallet
BG = [65, 65, 65]
RED = [235, 5, 50]
GREEN = [255, 255, 255]


class Food:
    def __init__(self):
        global WIDTH, HEIGHT, SCALE
        self.scl = SCALE
        self.location = []

    def Pick_location(self, snake):
        picked = False
        snake = snake.Get()

        while not picked:
            self.location = [random.choice(range(WIDTH)), random.choice(range(HEIGHT))]
            if not self.location in snake:
                picked = True

    def Location(self):
        return self.location

    def Draw(self):
        pygame.draw.rect(WINDOW, RED, (
            int(self.location[0] * self.scl), int(self.location[1] * self.scl), int(self.scl), int(self.scl)))


class Snake:
    def __init__(self):
        global WIDTH, HEIGHT, SCALE
        self.scl = SCALE
        self.s = [[WIDTH / 2, HEIGHT / 2]]
        self.inc = False
        self.dir = [0, -1]
        self.dead = False

    def Increase(self):
        self.inc = True

    def Update(self):
        head = [self.s[0][0] + self.dir[0], self.s[0][1] + self.dir[1]]

        if head[0] >= WIDTH or head[0] < 0 or head[1] >= HEIGHT or head[1] < 0:
            self.dead = True
        if head in self.s[1:]:
            self.dead = True
        else:
            self.s = [head] + self.s

            if not self.inc:
                self.s = self.s[:-1]
                pass
            else:
                self.inc = False

    def Dead(self):
        return self.dead

    def Change_Dir(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and not self.dir == [0, 1]:  # up
            self.dir = [0, -1]
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not self.dir == [0, -1]:  # down
            self.dir = [0, 1]
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not self.dir == [1, 0]:  # left
            self.dir = [-1, 0]
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not self.dir == [-1, 0]:  # right
            self.dir = [1, 0]

    def Get(self):
        return self.s

    def Draw(self):
        self.Change_Dir()
        self.Update()
        WINDOW.fill(BG)
        for pos in self.s:
            pygame.draw.rect(WINDOW, GREEN,
                             (int(pos[0] * self.scl), int(pos[1] * self.scl), int(self.scl), int(self.scl)))

    def Eat(self, food):
        if self.s[0] == food.Location():
            self.Increase()
            food.Pick_location(self)


def main():
    run = True
    global FPS
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    food.Pick_location(snake)

    while run:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            snake.Increase()

        snake.Eat(food)
        snake.Draw()
        food.Draw()

        pygame.display.update()

        if snake.Dead():
            run = False
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    return False


def New_Game():
    play = True

    while play:
        if not main():
            play = False


New_Game()
