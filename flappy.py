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

    def summon_central_pipe(self, pipes):
        pipe_bottom = pipes[0]
        pipe_top = pipes[1]
        central_pipe_height = pipe_bottom.y - pipe_top.bottom
        self.central_pipe = (pipe_bottom.x,
                             pipe_top.bottom,
                             30,
                             central_pipe_height)
        pygame.Rect(self.central_pipe)

        pygame.draw.rect(self.image, (255, 255, 255), self.central_pipe)

    def check_collision(self, pipes, top_bottom):
        self.summon_central_pipe(pipes)
        pipe_bottom = pipes[0]
        pipe_top = pipes[1]

        bird_right = self.rect.right
        bird_left = self.rect.left
        bird_top = self.rect.bottom - self.size
        bird_bottom = self.rect.bottom

        pipe_top_bottom = top_bottom

        # if (bird_right > pipe_bottom.left and bird_left < pipe_bottom.right) \
        #         and (bird_bottom > pipe_bottom[1] or bird_top < pipe_top_bottom + 35):
        #     return True
        # return False


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

    def draw(self, surface):
        pygame.draw.rect(surface, self.set_color(TEAL), self.central_space)
        # pygame.draw.rect(surface, self.set_color(TEAL, collision), self.rect)
        # pygame.draw.rect(surface, self.set_color(TEAL, collision), self.rect_top)
        pass

    def update(self):
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
    # ifCollision = player.check_collision(pipe.get_pipes(), pipe.returns())

    # render
    screen_surface.fill(DARK)
    player.draw(screen_surface)
    pipe.draw(screen_surface)
    pygame.display.update()
    Frames.tick(FPS)
