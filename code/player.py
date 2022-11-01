import pygame
from settings import *
from support import *
from spritesheet import SpriteSheet
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # import player animations
        self.animations = {
            'down': [],
            'up': [],
            'left': [],
            'right': [],
            'down_idle': [],
            'up_idle': [],
            'left_idle': [],
            'right_idle': [],
            'down_water': [],
            'up_water': [],
            'left_water': [],
            'right_water': [],
            'down_hoe': [],
            'up_hoe': [],
            'left_hoe': [],
            'right_hoe': [],
        }
        self.import_from_ss()
        self.status = 'down_idle'
        self.frame_index = 0

        # general
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=pos)

        # movement
        self.direction = pygame.math.Vector2()      # +y = down, +x = right
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
        }

        # tools
        self.tools = ['hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        # print(self.selected_tool)
        # TODO: implement
        pass

    def use_seed(self):
        # print(self.selected_seed)
        # TODO: implement
        pass

    def import_from_ss(self):
        """
        import character art from spritesheet
        """
        ss_path = '../art/char_ss_tools.png'
        chars_ss = SpriteSheet(ss_path)

        # ss coordinates
        # TODO: Better implementation of row/col imports from ss
        ss_coords = {
            'down': [(0, 0, 16, 16), (16, 0, 16, 16), (32, 0, 16, 16)],
            'left': [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)],
            'right': [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16)],
            'up': [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 16)],
            'down_idle': [(16, 0, 16, 16)],
            'up_idle': [(16, 48, 16, 16)],
            'left_idle': [(16, 16, 16, 16)],
            'right_idle': [(16, 32, 16, 16)],
            'down_hoe': [(0, 64, 16, 16), (16, 64, 16, 16), (32, 64, 16, 16)],
            'left_hoe': [(0, 80, 16, 16), (16, 80, 16, 16), (32, 80, 16, 16)],
            'right_hoe': [(0, 96, 16, 16), (16, 96, 16, 16), (32, 96, 16, 16)],
            'up_hoe': [(0, 112, 16, 16), (16, 112, 16, 16), (32, 112, 16, 16)],
            'down_water': [(0, 128, 16, 16), (16, 128, 16, 16), (32, 128, 16, 16)],
            'left_water': [(0, 144, 16, 16), (16, 144, 16, 16), (32, 144, 16, 16)],
            'right_water': [(0, 160, 16, 16), (16, 160, 16, 16), (32, 160, 16, 16)],
            'up_water': [(0, 176, 16, 16), (16, 176, 16, 16), (32, 176, 16, 16)],
        }

        for animation in self.animations.keys():
            self.animations[animation] = chars_ss.images_at(ss_coords[animation])

    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (64, 64))

    def input(self):
        keys = pygame.key.get_pressed()

        # only allow player to move/use tool when not already using tool
        if not self.timers['tool use'].active:
            # horizontal movement - L/R ARROW_KEYS
            if keys[pygame.K_RIGHT]:
                self.direction.x = +1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # vertical movement - U/D ARROW_KEYS
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = +1
                self.status = 'down'
            else:
                self.direction.y = 0

            # tool use - SPACE
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()          # start timer
                self.frame_index = 0                        # ensure start of tool animation
                self.direction = pygame.math.Vector2()      # stop player movement
                print(f'use {self.selected_tool}')

            # change tool - Q
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use - R_ALT
            if keys[pygame.K_RALT]:
                self.timers['seed use'].activate()          # start timer
                self.frame_index = 0                        # ensure start of tool animation
                self.direction = pygame.math.Vector2()      # stop player movement
                print(f'use {self.selected_seed}')

            # change seed - E
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]

    def get_status(self):
        """
        add idle animation
        """
        # idle animation
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool animation
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        # normalize vector so diag speed not faster
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
