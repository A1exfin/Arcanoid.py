import pygame.font


class Scoreboard:

    def __init__(self, arc_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.arc_settings = arc_settings
        self.stats = stats
        self.stats_bg_colour = (0, 0, 228)
        self.text_colour = (0, 250, 0)
        self.font = pygame.font.SysFont(None, 30)
        self.prep_high_score()
        self.prep_score()
        self.prep_level()
        self.prep_balls_left()
        self.prep_stats_bg()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("Очки: " + score_str, True, self.text_colour, self.stats_bg_colour)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 10
        self.score_rect.top = self.high_score_rect.bottom + 10

    def prep_high_score(self):
        rounded_high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render("Рекорд: " + high_score_str, True, self.text_colour, self.stats_bg_colour)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 10
        self.high_score_rect.top = 10

    def prep_level(self):
        self.level_image = self.font.render("Уровень: " + str(self.stats.level), True, self.text_colour, self.stats_bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = 10

    def prep_balls_left(self):
        self.balls_left_image = self.font.render("Мячей осталось: " + str(self.stats.balls_left), True, self.text_colour, self.stats_bg_colour)
        self.balls_left_rect = self.balls_left_image.get_rect()
        self.balls_left_rect.centerx = self.screen_rect.centerx
        self.balls_left_rect.top = 10

    def prep_stats_bg(self):
        self.bg_rect = pygame.Rect(0, 0, self.arc_settings.screen_width, (10 + self.high_score_rect.height + 10 + self.score_rect.height + 10))

    def show_score(self):
        pygame.draw.rect(self.screen, self.stats_bg_colour, self.bg_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.balls_left_image, self.balls_left_rect)
