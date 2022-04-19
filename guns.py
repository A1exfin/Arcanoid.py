import pygame


class Guns:

    def __init__(self, screen, platform):
        self.screen = screen
        self.platform = platform
        self.guns_active = True
        self.image_right = pygame.image.load("images/platforms/gun_right.bmp")
        self.image_left = pygame.image.load("images/platforms/gun_left.bmp")
        self.rect_right = self.image_right.get_rect()
        self.rect_left = self.image_left.get_rect()

    def update(self):
        self.rect_right.bottom = self.platform.rect.bottom
        self.rect_left.bottom = self.platform.rect.bottom
        self.rect_right.right = self.platform.rect.right
        self.rect_left.left = self.platform.rect.left

    def blitme(self):
        self.screen.blit(self.image_right, self.rect_right)
        self.screen.blit(self.image_left, self.rect_left)