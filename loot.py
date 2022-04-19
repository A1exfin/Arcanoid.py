import pygame
from pygame.sprite import Sprite
# Замедление мяча
# Ускорение мяча
# Супер мяч
# Дополнительная попытка
# Два мяча
# Удлиннение платформы
# Укорочение платформы
# Стреляющая платформа


class Loot(Sprite):

    def __init__(self, arc_settings, screen, block):
        super(Loot, self).__init__()
        self.arc_settings = arc_settings
        self.screen = screen
        self.block = block
        self.type = 0
        self.images = arc_settings.images_loot_type
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.centery = self.block.rect.centery
        self.rect.centerx = self.block.rect.centerx
        self.y = float(self.rect.y)

    def get_image(self):
        self.image = pygame.image.load("images/loot/" + self.images[self.type])

    def update(self):
        self.y += self.arc_settings.loot_drop_speed
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)