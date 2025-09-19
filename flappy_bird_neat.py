import pygame
import os
import random
import sys
import neat 

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

        self.bird_rect.y = self.y
        bird = self.rotate()
        WIN.blit(bird, self.bird_rect)
    
    def move(self):

        self.vel += self.g
        self.y += self.vel  

    def check_collision(self, pipes):

        if self.bird_rect.bottom >= 900 or self.bird_rect.top <= 0:
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
        self.gap_size = 250
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
        self.birds = []
        self.ge = []
        self.nets = []
        self.spwan_pipe = pygame.USEREVENT
        self.birdflap = pygame.USEREVENT + 1
        self.pipes = []
        self.clock = pygame.time.Clock()
        self.test = 0
        self.pipe_idx = 0

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

    def game_loop(self, genomes, config):

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.birds.append(Bird(100, 512))
            g.fitness = 0
            self.ge.append(g)
            self.nets.append(net)

        pygame.time.set_timer(self.spwan_pipe, 2400)
        pygame.time.set_timer(self.birdflap, 100)   

        while True:  
            if self.test == 0:
                self.pipes.append(Pipe())
                self.test = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == self.spwan_pipe:
                    self.test = 1
                    self.pipes.append(Pipe())
                    if len(self.pipes) > 3:
                        self.pipes.pop(0)
                        for g in self.ge:
                            g.fitness += 5

                if event.type == self.birdflap:
                    for bird in self.birds:
                        bird.flap_count = (bird.flap_count + 1) % 3

            self.pipe_idx = 0
            if len(self.birds) > 0 and len(self.pipes) > 0: 
                if self.birds[0].bird_rect.bottomleft[0] > self.pipes[0].pipe_rect_bot.x + self.pipes[0].pipe_rect_bot.width:
                    self.pipe_idx = 1

            for i, bird in enumerate(self.birds):
                    bird.move()
                    self.ge[i].fitness += 0.1
                    output = self.nets[i].activate((bird.y, bird.vel, abs(bird.y - self.pipes[self.pipe_idx].pipe_rect_bot.y), abs(bird.y - self.pipes[self.pipe_idx].pipe_rect_top.y)))

                    if output[0] > 0.5:
                        bird.jump()

            WIN.blit(BG_IMG, (0, 0))
            for i,bird in reversed(list(enumerate(self.birds))):
                    bird.draw()
                    bird.check_collision(self.pipes)
                    if bird.alive == False:
                        self.ge[i].fitness -= 1
                        self.birds.pop(i)
                        self.nets.pop(i)
                        self.ge.pop(i)

            for pipe in self.pipes:
                pipe.draw()
            self.draw_floor()

            if len(self.birds) == 0:
                self.pipes = []
                self.test = 0
                break

            self.clock.tick(120)
            pygame.display.update()

if __name__ == "__main__":
    Game = Game()
    Game.game_loop()