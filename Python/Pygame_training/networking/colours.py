import random

WHITE = (0xff, 0xff, 0xff)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0x80)
YELLOW = (0xff, 0xff, 0)
RED = (0xA5, 12, 12)

def random_color():
    return (random.randint(0, 0xff), random.randint(0, 0xff), random.randint(0, 0xff))