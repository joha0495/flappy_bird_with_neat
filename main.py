import pygame
import neat
import os
import time
import random
import sys

WIN_WIDTH = 672
WIN_HEIGHT = 1024

pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")).convert_alpha())]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert())
PIPE_IMG180 = pygame.transform.flip(PIPE_IMG, False, True)
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert())
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert(), (WIN_WIDTH, WIN_HEIGHT))

class Bird:
    IMGS = BIRD_IMGS
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0.25
        self.vel = 0
        self.bird_rect = self.IMGS[0].get_rect(center = (self.x, self.y))
        self.alive = True
        self.flap_count = 0

    def jump(self):
        self.vel = -6

    def draw(self):
        self.y += self.vel
        self.vel += self.g

        self.bird_rect.y = self.y
        bird = self.rotate()
        win.blit(bird, self.bird_rect)

    def check_collision(self, pipes):
        if self.bird_rect.bottom >= 900 or self.bird_rect.top <= 0 :
            self.alive = False
        
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe.pipe_rect_bot) or self.bird_rect.colliderect(pipe.pipe_rect_top):
                self.alive = False

    def rotate(self):
        new_bird = pygame.transform.rotozoom(self.IMGS[self.flap_count], -self.vel * 3, 1)
        return new_bird

class Pipe:
    IMG_BOT = PIPE_IMG
    IMG_TOP = PIPE_IMG180
    
    def __init__(self):
        self.x = WIN_WIDTH
        self.gap_center = random.randint(200, 700)
        self.gap_size = 300
        self.y = self.gap_center - (self.gap_size / 2)
        self.y2 = self.gap_center + (self.gap_size / 2)
        self.pipe_rect_bot = self.IMG_BOT.get_rect(x = self.x, top = self.y2)
        self.pipe_rect_top = self.IMG_TOP.get_rect(x = self.x, bottom = self.y)

    def draw(self):
        win.blit(self.IMG_BOT, self.pipe_rect_bot)
        win.blit(self.IMG_TOP, self.pipe_rect_top)
        self.pipe_rect_bot.x -= 1
        self.pipe_rect_top.x -= 1

class Game:

    def __init__(self):
        self.floor_x = 0
        self.bird = Bird(100, 512)
        self.spwan_pipe = pygame.USEREVENT
        self.birdflap = pygame.USEREVENT + 1
        self.pipes = []

    def draw_floor(self):
        if self.floor_x <= -WIN_WIDTH:
            self.floor_x = 0
        win.blit(BASE_IMG, (self.floor_x, 900))
        win.blit(BASE_IMG, (self.floor_x + WIN_WIDTH, 900))
        self.floor_x -= 1

    def game_loop(self):
        
        pygame.time.set_timer(self.spwan_pipe, 2400)
        pygame.time.set_timer(self.birdflap, 200)   

        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:   
                        self.bird.jump()
                    if event.key == pygame.K_SPACE and self.bird.alive == False:
                        self.bird = Bird(100, 512)
                        self.pipes = []
                    
                if event.type == self.spwan_pipe:
                    self.pipes.append(Pipe())
                    if len(self.pipes) > 3:
                        self.pipes.pop(0)

                if event.type == self.birdflap:
                    self.bird.flap_count = (self.bird.flap_count + 1) % 3

            win.blit(BG_IMG, (0, 0))
            if self.bird.alive:
                self.bird.draw()
                self.bird.check_collision(self.pipes)
                for pipe in self.pipes:
                    pipe.draw()

            self.draw_floor()
            clock.tick(120)
            pygame.display.update()


if __name__ == "__main__":
    Game = Game()
    Game.game_loop()