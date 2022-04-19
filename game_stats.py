class GameStats:

    def __init__(self, arc_settings):
        self.arc_settings = arc_settings
        # self.reset_stats()
        self.game_active = False
        self.super_ball = False
        self.active_balls = 0
        self.high_score = 0

    # def reset_stats(self):
        self.balls_left = self.arc_settings.balls_limit
        self.score = 0
        self.level = 1
        self.last_level_done = False
        self.lose = False
