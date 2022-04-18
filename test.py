from random import randint

SCREEN_HEIGHT = 600

bird_size = 50

for i in range(100000):
    height = randint(bird_size * 2, (SCREEN_HEIGHT - bird_size * 2))
    pass_data = 50, SCREEN_HEIGHT - bird_size - height
    cur_size = randint(bird_size, SCREEN_HEIGHT - (bird_size + height)) 
    if cur_size < pass_data[0] or cur_size > pass_data[1]:
        print(f'{cur_size} - failed')