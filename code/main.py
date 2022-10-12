import pygame
import sys
from settings import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))      # create graphical window
        self.clock = pygame.time.Clock()

        self.speed = [2, 2]
        self.black = 0, 0, 0

        self.ball = pygame.image.load('../art/Girl.png').convert_alpha()      # return surface
        self.ball_rect = self.ball.get_rect()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Ball movement
            self.ball_rect = self.ball_rect.move(self.speed)
            if self.ball_rect.left < 0 or self.ball_rect.right > SCREEN_WIDTH:
                self.speed[0] = -self.speed[0]
            if self.ball_rect.top < 0 or self.ball_rect.bottom > SCREEN_HEIGHT:
                self.speed[1] = -self.speed[1]

            self.screen.fill(self.black)                                  # overwrite old screen
            self.screen.blit(self.ball, self.ball_rect)                        # write ball to screen
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
