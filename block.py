import pygame
from pygame.sprite import Sprite


class Block(Sprite):

    def __init__(self, screen):
        super(Block, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.loot_flag = False
        self.get_image()

    def get_image(self):
        if self.loot_flag:
            self.image = pygame.image.load("images/blocks/loot_block.bmp")
        else:
            self.image = pygame.image.load("images/blocks/regular_block.bmp")
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)