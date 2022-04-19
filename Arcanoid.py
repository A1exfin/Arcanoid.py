import pygame
from pygame.sprite import Group
from scoreboard import Scoreboard
from game_stats import GameStats
from settings import Settings
from button import Button
from stick import Stick
# from platform import Platform
from guns import Guns
from info import Info
from loot import Loot
from block import Block
from ball import Ball
import game_functions as gf


def run_game():
    pygame.init()
    arc_settings = Settings()
    screen = pygame.display.set_mode((arc_settings.screen_width, arc_settings.screen_height))
    pygame.display.set_caption("Arcanoid")
    stats = GameStats(arc_settings)
    gf.load_highest_score(stats)
    sb = Scoreboard(arc_settings, screen, stats)
    platform = Stick(arc_settings, screen)
    # ball1 = Ball(arc_settings, screen, platform, stats, sb)
    # ball2 = Ball(arc_settings, screen, platform, stats, sb)
    # ball2.ball_speed_x = 0.4
    balls = Group()
    # balls.add(ball1)
    # balls.add(ball2)
    blocks = Group()
    guns = Guns(screen, platform)
    bullets = Group()
    loots = Group()
    play_button = Button(arc_settings, screen, "Старт")
    info = Info(arc_settings, screen, stats, play_button)
    while True:
        gf.check_events(arc_settings, screen, platform, guns, bullets, balls, blocks, stats, sb, play_button)
        if stats.game_active:
            gf.update_platform(platform, guns)
            gf.update_balls(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)
            gf.update_scoreboard(sb)
            gf.update_bullets(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)
            gf.update_loot(arc_settings, screen, platform, guns, balls, loots, sb, stats)
        gf.update_screen(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, play_button, info)


run_game()