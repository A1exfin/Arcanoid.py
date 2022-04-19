import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, arc_settings, screen, guns):
        super(Bullet, self).__init__()
        self.arc_settings = arc_settings
        self.screen = screen
        self.guns = guns
        self.rect = pygame.Rect(0, 0, arc_settings.bullet_width, arc_settings.bullet_height)
        if self.arc_settings.bullet_side == 1:
            self.rect.top = self.guns.rect_right.top
            self.rect.centerx = self.guns.rect_right.centerx
        if self.arc_settings.bullet_side == -1:
            self.rect.top = self.guns.rect_left.top
            self.rect.centerx = self.guns.rect_left.centerx
        self.y = float(self.rect.y)
        self.colour = self.arc_settings.bullet_colour
        self.speed_factor = arc_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)
