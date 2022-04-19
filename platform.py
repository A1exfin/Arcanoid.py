import pygame


class Platform:

    def __init__(self, arc_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.platform_width_tuple = arc_settings.platform_width_tuple
        self.platform_width = arc_settings.platform_width
        self.platform_speed = arc_settings.platform_speed
        self.image = pygame.image.load(
            "images/platforms/" + self.platform_width_tuple[self.platform_width])
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def get_new_image(self):
        self.image = pygame.image.load(
            "images/platforms/" + self.platform_width_tuple[self.platform_width])
        self.rect.width = self.image.get_width()

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.platform_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.platform_speed
        self.rect.centerx = self.center

    def platform_center(self):
        self.center = self.screen_rect.centerx

    def reset_platform(self, arc_settings):
        self.center = self.screen_rect.centerx
        self.platform_width = arc_settings.platform_width
        self.platform_width = 2
        self.get_new_image()

    def blitme(self):
        self.screen.blit(self.image, self.rect)