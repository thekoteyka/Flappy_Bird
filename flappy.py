import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()
# pygame.font.init()
myfont = pygame.font.SysFont('Arial', 5)

FPS = 60
Frames = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DEBUG = True

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

    def get(self, height):
        self.height_top = height

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

    def check_collision(self, pipe):
        bird_top = self.rect.top
        bird_right = self.rect.right
        bird_bottom = self.rect.bottom
        bird_left = self.rect.left

        central_pipe = pipe.central_space

        if bird_right > central_pipe.left and bird_left < central_pipe.right \
            and (bird_top < central_pipe.top or bird_bottom > central_pipe.bottom):
                return True

        return False


class Pipe(pygame.sprite.Sprite):
    PIPE_WIDTH = 30

    def __init__(self, bird_size):
        super().__init__()
        self.width = Pipe.PIPE_WIDTH # for testing
        self.bird_size = bird_size
        self.height = self.generate_random_height() # for testing, min max
        self.central_space = pygame.Rect(
            SCREEN_WIDTH - self.width, #x
            self.generate_random_y_position(), #y
            self.width, #width
            self.height #height
        )

    def generate_random_height(self):
        return randint(self.bird_size * 2, (SCREEN_HEIGHT - self.bird_size * 2))

    def generate_random_y_position(self):
        return randint(self.bird_size, SCREEN_HEIGHT - (self.bird_size + self.height))

    def set_color(self, color, collision=False):
        if DEBUG:
            if collision:
                return (255, 0, 0)
            else:
                return (255, 155, 155)
        return color

    def get_pipes(self):
        return self.rect, self.rect_top

    def returns(self):
        return self.height_top

    def set_pipes_props(self):
        self.top_pipe = (self.central_space.x,
                            0,
                            self.central_space.width,
                            self.central_space.y)

        self.bottom_pipe = (self.central_space.x,
                            self.central_space.bottom,
                            self.central_space.width,
                            SCREEN_HEIGHT)

    def draw(self, surface):
        # pygame.draw.rect(surface, self.set_color(TEAL, ifCollision), self.central_space)
        pygame.draw.rect(surface, self.set_color(TEAL, ifCollision), self.top_pipe)
        pygame.draw.rect(surface, self.set_color(TEAL, ifCollision), self.bottom_pipe)

    def update(self):
        self.set_pipes_props()
        self.central_space.move_ip(-3, 0)
        # self.rect.move_ip(-3, 0)
        # self.rect_top.move_ip(-3, 0)
        # self.set_rect_props()
        if self.central_space.right < 0:
            self.reset_pipe()

    def reset_pipe(self):
        self.central_space.left = SCREEN_WIDTH - self.width
        self.height = self.generate_random_height()
        self.central_space.height = self.height
        self.central_space.top = self.generate_random_y_position()


player = Bird()
pipe = Pipe(player.get_bird_size())

textsurface = myfont.render('Some Text', True, (255, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    player.update()
    pipe.update()
    ifCollision = player.check_collision(pipe)

    # render
    screen_surface.fill(DARK)
    player.draw(screen_surface)
    pipe.draw(screen_surface)
    pygame.display.update()
    Frames.tick(FPS)
