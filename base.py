import pygame
import pygame.color

BG_none = 0
BG_color = 1
BG_pygame_color = 2
BG_texture = 3

class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    pink = (233, 30, 99)
    lightpink = (248, 187, 208)
    darkpink = (136, 14, 79)
    red = (244, 67, 54)
    lightred = (255, 205, 210)
    darkred = (183, 28, 28)
    purple = (156, 39, 176)
    lightpurple = (225, 190, 231)
    darkpurple = (74, 20, 140)
    deepurple = (103, 58, 183)
    lightdeepurple = (209, 196, 233)
    darkdeepurple = (49, 27, 146)
    indigo = (63, 81, 181)
    lightindingo = (197, 202, 233)
    darkindigo = (26, 35, 126)
    blue = (33, 150, 243)
    lightblue = (207, 25, 98)
    darkblue = (13, 71, 161)
    cyan = (38, 198, 218)
    lightcyan = (178, 242, 235)
    darkcyan = (0, 96, 100)
    teal = (0, 150, 136)
    lighteal = (178, 223, 219)
    darkteal = (0, 77, 64)
    green = (76, 175, 80)
    lightgreen = (200, 230, 201)
    darkgreen = (27, 94, 32)
    lime = (205, 220, 57)
    lightlime = (220, 231, 117)
    darklime = (180, 119, 23)
    yellow = (255, 235, 59)
    lightyellow = (255, 241, 118)
    darkyellow = (245, 127, 23)
    amber = (255, 193, 7)
    lightamber = (255, 244, 130)
    darkamber = (255, 111, 0)
    orange = (255, 152, 0)
    lightorange = (255, 183, 77)
    darkorange = (230, 81, 0)
    deeporange = (255, 87, 34)
    lightdeeporange = (255, 138, 101)
    darkdeeporange = (191, 54, 12)
    brown = (121, 85, 72)
    lightbrown = (141, 110, 99)
    darkbrown = (62, 39, 35)
    bluegrey = (96, 125, 139)
    lightbluegrey = (144, 164, 174)
    darkbluegrey = (38,50,56)
    grey = (158, 158, 158)
    lightgrey = (224, 224, 224)
    darkgrey = (66, 66, 66)

    def __init__(self, color_name):
        self.returning = ('#' + hex(color_name[0]) + hex(color_name[1]) + hex(color_name[2])).replace('0x', '')

    def __str__(self):
        return self.returning

class Window:
    def none_func(self):
        pass

    def __init__(self, width, height, title='Project'):
        self.height = height
        self.width = width
        self.title = title
        self.bg_type = BG_none
        self.bg_arg = None
        self.before_textures = []
        self.textures = []
        self.before_loop_fun = self.none_func
        self.fun = self.none_func
        self.fps = 60
        self.keys = {
            '27': exit
        }

    def before_loop(self, before_loop_fun):
        self.before_loop_fun = before_loop_fun

    def load_textures(self, textures):
        self.before_textures = textures

    def create(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.before_loop_fun()

        for i in range(len(self.before_textures)):
            self.textures.append(pygame.image.load(self.before_textures[i]).convert())

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if str(event.key) in self.keys:
                        self.keys[str(event.key)]()

            if self.bg_type != BG_none:
                if self.bg_type == BG_pygame_color:
                    self.screen.fill(pygame.Color(self.bg_arg))
                elif self.bg_type == BG_color:
                    self.screen.fill(self.bg_arg)
                elif self.bg_type == BG_texture:
                    self.screen.blit(self.textures[self.bg_arg], (0, 0))
            else:
                self.screen.fill((0, 0, 0))

            self.fun()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def set_loop(self, fun, fps=60):
        self.fun = fun
        self.fps = fps

    def get(self):
        return self.screen

    def set_bg(self, bg_type, bg_arg = None):
        self.bg_type = bg_type
        self.bg_arg = bg_arg

    def set_fps(self, fps):
        self.fps = fps

    def keypressed(self, key, fun):
        self.keys[str(key)] = fun

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)