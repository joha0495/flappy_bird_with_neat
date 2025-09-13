import pygame
import os
import random
import sys

WIN_WIDTH = 672
WIN_HEIGHT = 1024

pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")).convert_alpha())]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert())
PIPE_IMG180 = pygame.transform.flip(PIPE_IMG, False, True)
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert())
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert(), (WIN_WIDTH, WIN_HEIGHT))
START_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "message.png")).convert_alpha(), (350, 500))

class Bird:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0.25
        self.vel = 0
        self.imgs = BIRD_IMGS
        self.bird_rect = self.imgs[0].get_rect(center = (self.x, self.y))
        self.alive = True
        self.flap_count = 0

    def jump(self):
        self.vel = -6

    def draw(self):
        self.y += self.vel
        self.vel += self.g

        self.bird_rect.y = self.y
        bird = self.rotate()
        WIN.blit(bird, self.bird_rect)

    def check_collision(self, pipes):
        if self.bird_rect.bottom >= 900 or self.bird_rect.top <= 0 :
            self.alive = False
        
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe.pipe_rect_bot) or self.bird_rect.colliderect(pipe.pipe_rect_top):
                self.alive = False

    def rotate(self):
        new_bird = pygame.transform.rotozoom(self.imgs [self.flap_count], -self.vel * 3, 1)
        return new_bird

class Pipe:

    def __init__(self):
        self.x = WIN_WIDTH
        self.gap_center = random.randint(200, 700)
        self.gap_size = 300
        self.y = self.gap_center - (self.gap_size / 2)
        self.y2 = self.gap_center + (self.gap_size / 2)
        self.img_bot = PIPE_IMG
        self.img_top = PIPE_IMG180
        self.pipe_rect_bot = self.img_bot.get_rect(x = self.x, top = self.y2)
        self.pipe_rect_top = self.img_top .get_rect(x = self.x, bottom = self.y)

    def draw(self):
        WIN.blit(self.img_bot, self.pipe_rect_bot)
        WIN.blit(self.img_top, self.pipe_rect_top)
        self.pipe_rect_bot.x -= 1
        self.pipe_rect_top.x -= 1

class Game:

    def __init__(self):
        self.floor_x = 0
        self.bird = Bird(100, 512)
        self.spwan_pipe = pygame.USEREVENT
        self.birdflap = pygame.USEREVENT + 1
        self.pipes = []
        self.game_state = False
        self.score_font = pygame.font.Font("flappy_bird.ttf", 40)
        self.score = 0
        self.high_score = 0
        self.start_img = START_IMG
        self.clock = pygame.time.Clock()

    def draw_score(self):
        score = self.score_font.render(f"{self.score}", True, (255, 255, 255))
        score_rect = score.get_rect(center = (WIN_WIDTH / 2, 100))
        WIN.blit(score, score_rect)

    def draw_game_over(self):
        score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score.get_rect(center = (WIN_WIDTH / 2, 100))
        WIN.blit(score, score_rect)
        high_score = self.score_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        high_score_rect = high_score.get_rect(center = (WIN_WIDTH / 2, 900))
        WIN.blit(high_score, high_score_rect)
        start_img_rect = self.start_img.get_rect(center = (WIN_WIDTH / 2, 500))
        WIN.blit(self.start_img, start_img_rect)

    def draw_floor(self):
        if self.floor_x <= -WIN_WIDTH:
            self.floor_x = 0
        WIN.blit(BASE_IMG, (self.floor_x, 900))
        WIN.blit(BASE_IMG, (self.floor_x + WIN_WIDTH, 900))
        self.floor_x -= 1

    def game_loop(self):
        pygame.time.set_timer(self.spwan_pipe, 2400)
        pygame.time.set_timer(self.birdflap, 100)   
        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.game_state == True:   
                        self.bird.jump()
                    if self.game_state == False:
                        self.bird = Bird(100, 512)
                        self.pipes = []
                        self.game_state = True
                        self.score = 0
                    
                if event.type == self.spwan_pipe and self.game_state == True:
                    self.pipes.append(Pipe())
                    if len(self.pipes) > 3:
                        self.pipes.pop(0)
                        self.score += 1

                if event.type == self.birdflap and self.game_state == True:
                    self.bird.flap_count = (self.bird.flap_count + 1) % 3

            WIN.blit(BG_IMG, (0, 0))
            if self.game_state == True:
                self.bird.draw()
                self.bird.check_collision(self.pipes)
                for pipe in self.pipes:
                    pipe.draw()
                self.draw_score()
                self.draw_floor()
                if self.bird.alive == False:
                    self.game_state = False
                    if self.score > self.high_score:
                        self.high_score = self.score
            else:
                self.draw_game_over()
            self.clock.tick(120)
            pygame.display.update()

if __name__ == "__main__":
    Game = Game()
    Game.game_loop()