class Settings:
    """Хранение настроек игры"""
    def __init__(self):
        # Настройки игрового экрана
        self.screen_width = 1400
        self.screen_height = 950
        self.bg_colour = (15, 15, 15)
        # Настройки мяча
        self.ball_direction_y = 1
        self.ball_direction_x = 1
        self.ball_speed_limit_y_max = 1
        self.ball_speed_limit_x_max = 2
        self.ball_speed_limit_y_min = 0.2
        self.ball_speed_limit_x_min = 0.4
        self.initialize_default_settings()
        self.ball_speedup_scale = 1.2
        # Настройки платформы
        self.platform_speed = 2
        self.platform_width_tuple = (
            "platform-2.bmp", "platform-1.bmp", "platform0.bmp", "platform1.bmp", "platform2.bmp", "platform3.bmp")
        self.platform_width = 2
        # Настройки пули
        self.bullet_width = 2
        self.bullet_height = 20
        self.bullets_allowed = 6
        self.bullet_speed_factor = 3
        self.bullet_colour = (250, 0, 0)
        self.bullet_side = 1  # Сторона на которой появляется пуля. 1 - справа, -1 - слева.
        # Настройки лута
        self.loot_drop_speed = 0.2
        self.images_loot_type = ("increase_platform.bmp", "decrease_platform.bmp", "shooting_platform.bmp",
                                 "ball_spedup.bmp", "ball_speeddown.bmp", "one_more_try.bmp", "super_ball.bmp",
                                 "two_balls.bmp")
        self.balls_limit = 3
        self.block_points = 50
        self.loot_points = 50
        self.high_difficult_loot_points = 50

    def initialize_default_settings(self):
        self.ball_speed_factor_y = 0.4
        self.ball_speed_factor_x = 0.8
