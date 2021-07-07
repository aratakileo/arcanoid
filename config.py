class window:
    width, height, fps = 1200, 800, 60
    title = 'Arcanoid'

class paddle:
    width, height, speed = 330, 35, 15

class ball:
    radius = 20
    speed = 6
    rect = int(radius * 2 ** 0.5)

class game:
    lvl_min = 2
    lvl_max = 6