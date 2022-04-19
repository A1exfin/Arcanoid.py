import pygame.image
from pygame.sprite import Sprite


class Ball(Sprite):

    def __init__(self, arc_settings, screen, platform, stats, sb):
        super(Ball, self).__init__()
        self.arc_settings = arc_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.platform = platform
        self.sb = sb
        self.stats = stats
        self.super = self.stats.super_ball
        self.ball_active = False
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.bottom = self.platform.rect.top
        self.rect.centerx = self.platform.rect.centerx
        # self.ball_speed_y = arc_settings.ball_speed_factor_y
        # self.ball_speed_x = arc_settings.ball_speed_factor_x
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.ball_direction_y = arc_settings.ball_direction_y
        self.ball_direction_x = arc_settings.ball_direction_x

    def get_image(self):
        if self.super:
            self.image = pygame.image.load("images/balls/super_ball.bmp")
        else:
            self.image = pygame.image.load("images/balls/ball.bmp")

    def update(self):
        if self.ball_active:
            self.y -= (self.arc_settings.ball_speed_factor_y * self.ball_direction_y)
            self.x += (self.arc_settings.ball_speed_factor_x * self.ball_direction_x)
            self.rect.y = self.y
            self.rect.x = self.x
        else:
            self.rect.bottom = self.platform.rect.top
            self.rect.centerx = self.platform.rect.centerx
            self.y = self.rect.y
            self.x = self.rect.x

    def check_lr_edges(self):
        if self.rect.right >= self.screen_rect.right:
            return True
        if self.rect.left <= self.screen_rect.left:
            return True

    def check_top_edge(self):
        if self.rect.top <= self.sb.bg_rect.bottom:
            return True

    def check_bottom_edge(self):
        if self.rect.bottom > self.screen_rect.bottom:
            return True

    def reset_ball(self, arc_settings):
        self.ball_active = False
        # self.ball_speed_y = arc_settings.ball_speed_factor_y
        # self.ball_speed_x = arc_settings.ball_speed_factor_x
        self.ball_direction_y = arc_settings.ball_direction_y
        self.ball_direction_x = arc_settings.ball_direction_x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
