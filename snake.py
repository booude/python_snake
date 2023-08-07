import pygame as p
import math
import random
import time
import sys

WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = WIDTH // PIXELS

BG1 = (156, 210, 54)
BG2 = (147, 203, 57)
RED = (255, 0, 0)
BLUE = (0, 0, 50)
BLACK = (0, 0, 0)


class Snake:
    def __init__(self):
        self.color = BLUE
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.state = "STOP"

    def move(self):
        if self.state == "UP":
            self.headY -= PIXELS

        elif self.state == "DOWN":
            self.headY += PIXELS

        elif self.state == "LEFT":
            self.headX -= PIXELS

        elif self.state == "RIGHT":
            self.headX += PIXELS

    def move_body(self):
        if len(self.bodies) > 0:
            for i in range(len(self.bodies) - 1, -1, -1):
                if i == 0:
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    self.bodies[i].posX = self.bodies[i - 1].posX
                    self.bodies[i].posY = self.bodies[i - 1].posY

    def add_body(self):
        body = Body(BLUE, self.headX, self.headY)
        self.bodies.append(body)

    def draw(self, surface):
        p.draw.rect(surface, self.color, (self.headX, self.headY, PIXELS, PIXELS))
        if len(self.bodies) > 0:
            for body in self.bodies:
                body.draw(surface)

    def die(self):
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.state = "STOP"


class Body:
    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self, surface):
        p.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))


class Apple:
    def __init__(self):
        self.color = RED
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        p.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))


class Background:
    def draw(self, surface):
        counter = 0
        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    surface.fill(BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                else:
                    surface.fill(BG1, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                counter += 1
            counter += 1


class Colision:
    def between_snake_and_apple(self, snake, apple):
        if snake.headX == apple.posX and snake.headY == apple.posY:
            return True
        else:
            return False

    def between_snake_and_walls(self, snake):
        if (
            snake.headX < 0
            or snake.headX > WIDTH - PIXELS
            or snake.headY < 0
            or snake.headY > HEIGHT - PIXELS
        ):
            return True
        else:
            return False

    def between_head_and_body(self, snake):
        for body in snake.bodies:
            if body.posX == snake.headX and body.posY == snake.headY:
                return True
        return False


class Score:
    def __init__(self):
        self.score = 0
        self.font = p.font.SysFont("monospace", 30, bold=False)

    def increase(self):
        self.score += 1

    def reset(self):
        self.score = 0

    def show(self, surface):
        lbl = self.font.render("Score: " + str(self.score), 1, BLACK)
        surface.blit(lbl, (10, 10))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Python Snake")

    snake = Snake()
    apple = Apple()
    background = Background()
    collision = Colision()
    score = Score()

    while True:
        background.draw(screen)
        snake.draw(screen)
        apple.draw(screen)
        score.show(screen)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.KEYDOWN:
                if event.key == p.K_UP:
                    if snake.state != "DOWN":
                        snake.state = "UP"
                elif event.key == p.K_DOWN:
                    if snake.state != "UP":
                        snake.state = "DOWN"
                elif event.key == p.K_LEFT:
                    if snake.state != "RIGHT":
                        snake.state = "LEFT"
                elif event.key == p.K_RIGHT:
                    if snake.state != "LEFT":
                        snake.state = "RIGHT"
                elif event.key == p.K_p:
                    snake.state = "STOP"
        if collision.between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()

        if snake.state != "STOP":
            snake.move_body()
            snake.move()

        if collision.between_snake_and_walls(snake):
            if snake.headX < 0:
                snake.headX = WIDTH
            elif snake.headY < 0:
                snake.headY = HEIGHT
            elif snake.headX > WIDTH:
                snake.headX = 0
            elif snake.headY > HEIGHT:
                snake.headY = 0
            # apple.spawn()
        if collision.between_head_and_body(snake):
            snake.die()
            apple.spawn()
            score.reset()

        p.time.delay(80)

        p.display.update()


main()
