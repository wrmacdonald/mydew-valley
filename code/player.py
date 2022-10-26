import pygame
from settings import *
from support import *
from spritesheet import SpriteSheet


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

    def import_from_ss(self):
        """
        import character art from spritesheet
        """
        ss_path = '../art/char_ss.png'
        chars_ss = SpriteSheet(ss_path)

        # ss coordinates
        ss_coords = {
            'down': [(0, 0, 16, 16), (16, 0, 16, 16), (32, 0, 16, 16)],
            'up': [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 16)],
            'left': [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)],
            'right': [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16)],
            'down_idle': [(16, 0, 16, 16)],
            'up_idle': [(16, 48, 16, 16)],
            'left_idle': [(16, 16, 16, 16)],
            'right_idle': [(16, 32, 16, 16)],
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

        # horizontal movement
        if keys[pygame.K_RIGHT]:
            self.direction.x = +1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = +1
            self.status = 'down'
        else:
            self.direction.y = 0

    def get_status(self):
        """
        add idle animation
        """
        # idle animation
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

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
        self.move(dt)
        self.animate(dt)
