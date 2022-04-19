import pygame


class Info:
    def __init__(self, arc_settings, screen, stats, play_button):
        self.arc_settings = arc_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.play_button = play_button
        self.font_loot_description = pygame.font.SysFont(None, 30)
        self.font_last_level_done = pygame.font.SysFont(None, 48)
        self.loots_description = (" - Расширение платформы.", " - Укорочение платформы.", " - Активация пушек.",
                                  " - Увеличение скорости мяча.", " - Уменьшение скорости мяча.",
                                  " - Дополнительный мяч (попытка).", " - Активация супер-мяча.",
                                  " - Два активных мяча.")
        self.one_more = "Хотите сыграть ещё раз?"
        self.one_more_image = self.font_last_level_done.render(self.one_more, True, (0, 0, 250), self.arc_settings.bg_colour)
        self.one_more_rect = self.one_more_image.get_rect()
        self.one_more_rect.centerx = self.play_button.rect.centerx
        self.one_more_rect.bottom = self.play_button.rect.top - 20
        self.prep_last_info()
        self.you_lose()
        self.loot_images = []
        self.loot_rects = []
        self.description_images = []
        self.description_rects = []
        for number in range(0, 8, 1):
            self.loot_image = pygame.image.load("images/loot/" + arc_settings.images_loot_type[number])
            self.loot_rect = self.loot_image.get_rect()
            self.loot_images.append(self.loot_image)
            self.loot_rects.append(self.loot_rect)
            self.description_image = self.font_loot_description.render(self.loots_description[number], True, (200, 200, 200), arc_settings.bg_colour)
            self.description_image_rect = self.description_image.get_rect()
            self.description_images.append(self.description_image)
            self.description_rects.append(self.description_image_rect)

    def prep_last_info(self):
        total_score = "{:,}".format(self.stats.score)
        best_score = "{:,}".format(self.stats.high_score)
        self.high_score_info = "Лучший результат: " + best_score
        self.high_score_info_image = self.font_last_level_done.render(self.high_score_info, True, (0, 0, 250), self.arc_settings.bg_colour)
        self.high_score_info_rect = self.high_score_info_image.get_rect()
        self.high_score_info_rect.centerx = self.play_button.rect.centerx
        self.high_score_info_rect.bottom = self.one_more_rect.top - 20
        self.last_level_done_congrats = "Вы прошли всю игру!!! Моё почтение!!! Ваш результат: " + total_score
        self.last_level_done_image = self.font_last_level_done.render(self.last_level_done_congrats, True, (0, 0, 250), self.arc_settings.bg_colour)
        self.last_level_done_rect = self.last_level_done_image.get_rect()
        self.last_level_done_rect.centerx = self.play_button.rect.centerx
        self.last_level_done_rect.bottom = self.high_score_info_rect.top - 20

    def you_lose(self):
        self.lose = "Вы проиграли"
        self.lose_image = self.font_last_level_done.render(self.lose, True, (0, 0, 250), self.arc_settings.bg_colour)
        self.lose_rect = self.lose_image.get_rect()
        self.lose_rect.centerx = self.play_button.rect.centerx
        self.lose_rect.bottom = self.one_more_rect.top - 20

    def draw_info(self):
        for number in range(0, 8, 1):
            self.loot_rects[number].top = 40 + self.play_button.rect.bottom + (10 + self.loot_rects[number].height) * number
            self.loot_rects[number].right = self.play_button.rect.left
            self.description_rects[number].centery = self.loot_rects[number].centery
            self.description_rects[number].left = self.loot_rects[number].right
            self.screen.blit(self.loot_images[number], self.loot_rects[number])
            self.screen.blit(self.description_images[number], self.description_rects[number])

    def draw_congrats(self):
        self.screen.blit(self.one_more_image, self.one_more_rect)
        self.screen.blit(self.last_level_done_image, self.last_level_done_rect)
        self.screen.blit(self.high_score_info_image, self.high_score_info_rect)

    def draw_lose(self):
        self.screen.blit(self.one_more_image, self.one_more_rect)
        self.screen.blit(self.lose_image, self.lose_rect)