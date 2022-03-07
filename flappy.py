import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()

FPS = 60
Frames = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DARK = (87, 87, 81)
TEAL = (244, 250, 156)

screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_surface.fill(DARK)

pygame.display.set_caption('Flappy Bird')


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("twitter.png")
        self.rect = self.image.get_rect()
        self.rect.top = SCREEN_HEIGHT / 2 - self.rect.size[0] / 2
        self.rect.left = 20
        self.velocity = 1
        self.gravity = 0.2
        self.size = self.rect.size[0]
    def update(self):
        self.rect.move_ip(0, self.velocity)
        self.velocity += self.gravity
        self.key_press()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0

    def get_bird_size(self):
        return self.size

    def key_press(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE] or pressed_keys[K_z] or pressed_keys[K_x]:
            self.velocity = -4

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, bird_size):
        super().__init__()
        self.width = 30
        self.height = 400
        self.rect = pygame.Rect(SCREEN_WIDTH - self.width,
                                SCREEN_HEIGHT - self.height,
                                self.width,
                                self.height)

        self.width_top = 30
        self.height_top = 200
        self.rect_top = pygame.Rect(SCREEN_WIDTH - self.width_top,
                                    SCREEN_HEIGHT - self.height_top,
                                    self.width_top,
                                    self.height_top)
        self.bird_size = bird_size

    def draw(self, surface):
        self.rect.move_ip(-1, 0)
        pygame.draw.rect(surface, TEAL, self.rect)




    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            # self.rect.y = 400
            self.rect.y = SCREEN_HEIGHT - randint(20, SCREEN_HEIGHT // 2 + self.bird_size)



player = Bird()
pipe = Pipe(player.get_bird_size())



while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    # Update
    player.update()
    pipe.update()

    # render
    screen_surface.fill(DARK)
    player.draw(screen_surface)
    pipe.draw(screen_surface)
    pygame.display.update()
    Frames.tick(FPS)
