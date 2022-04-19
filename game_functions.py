import sys
import json
import random
import pygame
from time import sleep
from block import Block
from bullet import Bullet
from loot import Loot
from ball import Ball


def update_screen(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, play_button, info):
    """Отрисовка изиображения объектов на экране"""
    screen.fill(arc_settings.bg_colour)
    platform.blitme()
    balls.draw(screen)
    if guns.guns_active:
        guns.blitme()
    # bullets.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    blocks.draw(screen)
    loots.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
        info.draw_info()
        if stats.last_level_done:
            info.draw_congrats()
        elif stats.lose:
            info.draw_lose()
    pygame.display.flip()


def update_balls(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info):
    """Обновление положения мяча"""
    if len(balls) == 0:
        loose_try(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)
    balls.update()
    for ball in balls:
        check_ball_edges(ball, balls)
        check_ball_block_collision(arc_settings, screen, platform, guns, bullets, ball, balls, blocks, loots, stats, sb, info)
        check_ball_platform_collision(platform, ball)


def update_platform(platform, guns):
    """Обновление положения платформы"""
    if guns.guns_active:
        guns.update()
    platform.update()


def update_bullets(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info):
    """Обновление положения пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_block_collisions(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)


def update_loot(arc_settings, screen, platform, guns, balls, loots, sb, stats):
    """Обновление положения лута"""
    loots.update()
    for loot in loots.copy():
        check_loot_platform_collisions(arc_settings, screen, platform, guns, balls, loots, sb, stats)
        if loot.rect.top >= arc_settings.screen_height:
            loots.remove(loot)


def update_scoreboard(sb):
    """Обновление очков"""
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_balls_left()
    sb.prep_stats_bg()


def check_events(arc_settings, screen, platform, guns, bullets, balls, blocks, stats, sb, play_button):
    """Проверка событий клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highest_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, arc_settings, screen, platform, guns, bullets, blocks, balls, stats, sb, play_button)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, platform)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(arc_settings, screen, platform, guns, balls, blocks, stats, sb, play_button, mouse_x, mouse_y)


def check_keydown_events(event, arc_settings, screen, platform, guns, bullets, blocks, balls, stats, sb, play_button):
    """Проверка нажатий клавиш"""
    if event.key == pygame.K_RIGHT:
        platform.moving_right = True
    elif event.key == pygame.K_LEFT:
        platform.moving_left = True
    elif event.key == pygame.K_UP:
        if stats.game_active:
            for ball in balls:
                if not ball.ball_active:
                    ball.ball_active = True
                    break
    elif event.key == pygame.K_SPACE:
        # if not stats.game_active:
        #     mouse_x = play_button.rect.centerx
        #     mouse_y = play_button.rect.centery
        #     check_play_button(arc_settings, screen, platform, balls, blocks, stats, sb, play_button, mouse_x, mouse_y)
        # else:
        if guns.guns_active:
            for ball in balls:
                if ball.ball_active:
                    fire_bullets(arc_settings, screen, guns, bullets)
    elif event.key == pygame.K_ESCAPE:
        save_highest_score(stats)
        sys.exit()


def check_keyup_events(event, platform):
    """Проверка отжатий клавиш"""
    if event.key == pygame.K_RIGHT:
        platform.moving_right = False
    elif event.key == pygame.K_LEFT:
        platform.moving_left = False


def check_play_button(arc_settings, screen, platform, guns, balls, blocks, stats, sb, play_button, mouse_x, mouse_y):
    """Проверка нажатия кнопки старта игры"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        platform.reset_platform(arc_settings)
        arc_settings.initialize_default_settings()
        stats.super_ball = False
        guns.guns_active = False
        new_ball = Ball(arc_settings, screen, platform, stats, sb)
        balls.add(new_ball)
        stats.balls_left = arc_settings.balls_limit
        stats.score = 0
        stats.level = 1
        blocks.empty()
        update_scoreboard(sb)
        create_level_1(arc_settings, screen, blocks, sb)
        # create_level_2(screen, blocks, sb)
        # create_level_3(arc_settings, screen, blocks, sb)
        # create_level_4(screen, blocks, sb)
        # create_level_5(screen, blocks, sb)
        stats.lose = False
        stats.last_level_done = False
        stats.game_active = True
        pygame.mouse.set_visible(False)





def fire_bullets(arc_settings, screen, guns, bullets):
    """Стрельба"""
    i = 2
    if len(bullets) < arc_settings.bullets_allowed:
        for i in range(i):
            new_bullet = Bullet(arc_settings, screen, guns)
            bullets.add(new_bullet)
            arc_settings.bullet_side *= -1


def check_bullet_block_collisions(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info):
    """Проверка столкновения пуль и блоков"""
    collisions_bullets = pygame.sprite.groupcollide(bullets, blocks, True, True)
    if collisions_bullets:
        for colided_blocks in collisions_bullets.values():
            score_increase_bullet(arc_settings, stats, sb, colided_blocks)
            for colided_block in colided_blocks:
                if colided_block.loot_flag:
                    create_loot(arc_settings, screen, loots, colided_block)
    if len(blocks) == 0:
        check_level_done(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)


def create_loot(arc_settings, screen, loots, collided_block):
    """Создание случайного лута"""
    new_loot = Loot(arc_settings, screen, collided_block)
    new_loot.type = random.randint(0, 7)
    new_loot.get_image()
    loots.add(new_loot)


def check_loot_platform_collisions(arc_settings, screen, platform, guns, balls, loots, sb, stats):
    """Проверка столкновения лута с платформой"""
    collided_loots = pygame.sprite.spritecollide(platform, loots, True)
    if collided_loots:
        for loot in collided_loots:
            if loot.type == 0:  # Увеличение ширины платформы
                score_increase_loots(arc_settings, stats, sb)
                if platform.platform_width < 5:
                    platform.platform_width += 1
                    platform.get_new_image()
            if loot.type == 1:  # Уменьшение ширины платформы
                score_increase_loots(arc_settings, stats, sb)
                if platform.platform_width > 0:
                    platform.platform_width -= 1
                    platform.get_new_image()
            if loot.type == 2:  # Активация пушек
                score_increase_loots(arc_settings, stats, sb)
                guns.guns_active = True
            if loot.type == 3:  # Увеличение скорости мячей
                score_increase_loots(arc_settings, stats, sb)
                if arc_settings.ball_speed_factor_y < arc_settings.ball_speed_limit_y_max \
                        and arc_settings.ball_speed_factor_x < arc_settings.ball_speed_limit_x_max:
                    arc_settings.ball_speed_factor_y *= arc_settings.ball_speedup_scale
                    arc_settings.ball_speed_factor_x *= arc_settings.ball_speedup_scale
            if loot.type == 4:  # Уменьшение скорости мячей
                score_increase_loots(arc_settings, stats, sb)
                if arc_settings.ball_speed_factor_y > arc_settings.ball_speed_limit_y_min \
                        and arc_settings.ball_speed_factor_x > arc_settings.ball_speed_limit_x_min:
                    arc_settings.ball_speed_factor_y /= arc_settings.ball_speedup_scale
                    arc_settings.ball_speed_factor_x /= arc_settings.ball_speedup_scale
            if loot.type == 5:  # Дополнительная жизнь
                score_increase_loots(arc_settings, stats, sb)
                if stats.balls_left < 6:
                    stats.balls_left += 1
            if loot.type == 6:  # Активация супер мячей
                score_increase_loots(arc_settings, stats, sb)
                for ball in balls:
                    stats.super_ball = True
                    ball.super = True
                    ball.get_image()
            if loot.type == 7:  # Второй мяч
                score_increase_loots(arc_settings, stats, sb,)
                if len(balls) < 2:
                    new_ball = Ball(arc_settings, screen, platform, stats, sb)
                    balls.add(new_ball)


def check_ball_edges(ball, balls):
    """Проверка слолкновения мяча с границами экрана"""
    if ball.check_lr_edges():
        change_ball_directionx(ball)
    if ball.check_top_edge():
        change_ball_directiony(ball)
    if ball.check_bottom_edge():
        balls.remove(ball)


def change_ball_directionx(ball):
    """Изменение направления движения мяча по оси X"""
    ball.ball_direction_x *= -1


def change_ball_directiony(ball):
    """Изменение направления движения мяча по оси Y"""
    ball.ball_direction_y *= -1


def check_ball_platform_collision(platform, ball):
    """Проверка столкновения мяча с платформой"""
    if pygame.sprite.collide_rect(platform, ball):
        ball.ball_direction_y *= -1


def check_ball_block_collision(arc_settings, screen, platform, guns, bullets, ball, balls, blocks, loots, stats, sb, info):
    """Проверка слолкновения мяча и блока"""
    collided_blocks = pygame.sprite.spritecollide(ball, blocks, True)
    if collided_blocks:
        score_increase_ball(arc_settings, stats, sb, collided_blocks)
        for collided_block in collided_blocks:
            check_block_edge(ball, collided_block)
            if collided_block.loot_flag:
                create_loot(arc_settings, screen, loots, collided_block)
    if len(blocks) == 0:
        check_level_done(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info)


def check_block_edge(ball, collided_block):
    """Проверка границы блока с котрой столкнулся мяч"""
    if ball.rect.left <= collided_block.rect.right and ball.rect.right > collided_block.rect.right:  # Столкновение мяча с правой границей блока
        if not ball.super:
            change_ball_directionx(ball)
    elif ball.rect.right >= collided_block.rect.left and ball.rect.left < collided_block.rect.left:  # Столкновение мяча с левой границей блока
        if not ball.super:
            change_ball_directionx(ball)
    elif ball.rect.top <= collided_block.rect.bottom and ball.rect.bottom > collided_block.rect.bottom:  # Столкновение мяча с нижней границей блока
        if not ball.super:
            change_ball_directiony(ball)
    elif ball.rect.bottom >= collided_block.rect.top and ball.rect.top < collided_block.rect.top:  # Столкновение мяча с верхней границей блока
        if not ball.super:
            change_ball_directiony(ball)


def create_level_1(arc_settings, screen, blocks, sb):
    """Создание первого уровня"""
    block = Block(screen)
    screen_rect = screen.get_rect()
    available_space_x = arc_settings.screen_width - 2 * block.rect.width
    available_space_y = arc_settings.screen_height - sb.bg_rect.height - 15 * block.rect.height
    number_blocks_x = int(available_space_x / (1.3 * block.rect.width))
    number_blocks_y = int(available_space_y / (1.6 * block.rect.height))
    for block_number_y in range(number_blocks_y):
        for block_number_x in range(number_blocks_x):
            new_block = Block(screen)
            if block_number_y == 1 and (block_number_x == 1 or block_number_x == 13):
                new_block.loot_flag = True
            elif block_number_y == 5 and (block_number_x == 1 or block_number_x == 13):
                new_block.loot_flag = True
            elif block_number_y == 3 and (block_number_x == 7):
                new_block.loot_flag = True
            else:
                new_block.loot_flag = False
            new_block.get_image()
            new_block.rect.centerx = (screen_rect.centerx - (new_block.rect.width + 2) * int(number_blocks_x / 2)) + block_number_x * (new_block.rect.width + 2)
            new_block.rect.y = sb.bg_rect.height + 4 * new_block.rect.height + (new_block.rect.height + 2) * block_number_y
            blocks.add(new_block)


def create_level_2(screen, blocks, sb):
    """Создание второго уровня"""
    screen_rect = screen.get_rect()
    number_blocks_x = (1, 3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3, 1)
    number_blocks_y = 13
    for block_number_y in range(number_blocks_y):
        for block_number_x in range(number_blocks_x[block_number_y]):
            new_block = Block(screen)
            if block_number_y == 1 and block_number_x == 1:
                new_block.loot_flag = True
            elif block_number_y == 6 and (block_number_x == 1 or block_number_x == 11 or block_number_x == 6):
                new_block.loot_flag = True
            elif block_number_y == 11 and block_number_x == 1:
                new_block.loot_flag = True
            else:
                new_block.loot_flag = False
            new_block.get_image()
            new_block.rect.centerx = (screen_rect.centerx - (new_block.rect.width + 2) * (number_blocks_x[block_number_y] / 2)) + block_number_x * (new_block.rect.width + 2)
            new_block.rect.y = sb.bg_rect.height + 4 * new_block.rect.height + (new_block.rect.height + 2) * block_number_y
            blocks.add(new_block)


def create_level_3(arc_settings, screen, blocks, sb):
    """Создание третьего уровня"""
    block = Block(screen)
    available_space_x = arc_settings.screen_width
    available_space_y = arc_settings.screen_height - sb.bg_rect.height - 11 * block.rect.height
    number_blocks_x = int(available_space_x / (1.9 * block.rect.width))
    number_blocks_y = int(available_space_y / (1.6 * block.rect.height))
    for block_number_y in range(number_blocks_y):
        for block_number_x in range(number_blocks_x):
            new_block = Block(screen)
            if block_number_y == 1 and (block_number_x == 1 or block_number_x == 3 or block_number_x == 5 or block_number_x == 7 or block_number_x == 9):
                new_block.loot_flag = True
            elif block_number_y == 4 and (block_number_x == 1 or block_number_x == 3 or block_number_x == 5 or block_number_x == 7 or block_number_x == 9):
                new_block.loot_flag = True
            elif block_number_y == 7 and (block_number_x == 1 or block_number_x == 3 or block_number_x == 5 or block_number_x == 7 or block_number_x == 9):
                new_block.loot_flag = True
            else:
                new_block.loot_flag = False
            new_block.get_image()
            new_block.rect.x = 30 + block_number_x * 2 * new_block.rect.width
            new_block.rect.y = sb.bg_rect.height + 2 * new_block.rect.height + 2 * new_block.rect.height * block_number_y
            blocks.add(new_block)


def create_level_4(screen, blocks, sb):
    """Создание четвёртого уровня"""
    screen_rect = screen.get_rect()
    number_blocks_x = (14, 14, 14, 10, 6, 2, 6, 10, 14, 14, 14, 18)
    number_blocks_y = 12
    for block_number_y in range(number_blocks_y):
        for block_number_x in range(number_blocks_x[block_number_y]):
            new_block = Block(screen)
            if block_number_y == 11:
                if block_number_x > (number_blocks_x[block_number_y] / 2) - 1:
                    block_number_x -= number_blocks_x[block_number_y] / 2
                    if block_number_x == 1 or block_number_x == 7 or block_number_x == 4:
                        set_loot_flag(new_block)
                    new_block.rect.right = screen_rect.right + 2 - (new_block.rect.width + 2) * block_number_x
                else:
                    if block_number_x == 1 or block_number_x == 7 or block_number_x == 4:
                        set_loot_flag(new_block)
                    new_block.rect.left = screen_rect.left + 2 + (new_block.rect.width + 2) * block_number_x
                new_block.rect.y = screen_rect.bottom - 2 * new_block.rect.height
            else:
                if block_number_x > (number_blocks_x[block_number_y] / 2) - 1:
                    block_number_x -= number_blocks_x[block_number_y] / 2
                    if block_number_y == 5 and block_number_x == 0:
                        set_loot_flag(new_block)
                    elif block_number_y == 1 and block_number_x == 3:
                        set_loot_flag(new_block)
                    elif block_number_y == 9 and block_number_x == 3:
                        set_loot_flag(new_block)
                    new_block.rect.centerx = (screen_rect.centerx + screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x[block_number_y] / 4) + block_number_x * (new_block.rect.width + 2)
                else:
                    if block_number_y == 5 and block_number_x == 0:
                        set_loot_flag(new_block)
                    elif block_number_y == 1 and block_number_x == 3:
                        set_loot_flag(new_block)
                    elif block_number_y == 9 and block_number_x == 3:
                        set_loot_flag(new_block)
                    new_block.rect.centerx = (screen_rect.centerx - screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x[block_number_y] / 4) + block_number_x * (new_block.rect.width + 2)
                new_block.rect.y = sb.bg_rect.height + 3 * new_block.rect.height + (new_block.rect.height + 2) * block_number_y
            blocks.add(new_block)


def create_level_5(screen, blocks, sb):
    """Создание пятого уровня"""
    screen_rect = screen.get_rect()
    number_blocks_x = 18
    number_blocks_y = 15
    for block_number_y in range(number_blocks_y):
        for block_number_x in range(number_blocks_x):
            new_block = Block(screen)
            if block_number_y == 14:
                if block_number_x > (number_blocks_x / 2) - 1:
                    block_number_x -= number_blocks_x / 2
                    if block_number_x == 1 or block_number_x == 7:
                        set_loot_flag(new_block)
                    new_block.rect.centerx = (screen_rect.centerx + screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
                else:
                    if block_number_x == 1 or block_number_x == 7:
                        set_loot_flag(new_block)
                    new_block.rect.centerx = (screen_rect.centerx - screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
                new_block.rect.y = screen_rect.bottom - 1.5 * new_block.rect.height - new_block.rect.height
            elif block_number_y > (number_blocks_y / 2) - 1:
                new_block.rect.y = sb.bg_rect.height + 6 * new_block.rect.height + (new_block.rect.height + 2) * block_number_y
                new_block.rect.centerx = (screen_rect.centerx - screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
                if block_number_x > (number_blocks_x / 2) - 1:
                    block_number_x -= number_blocks_x / 2
                    new_block.rect.centerx = (screen_rect.centerx + screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
            else:
                new_block.rect.centerx = (screen_rect.centerx - screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
                if block_number_x > (number_blocks_x / 2) - 1:
                    block_number_x -= number_blocks_x / 2
                    new_block.rect.centerx = (screen_rect.centerx + screen_rect.width / 4) - (new_block.rect.width + 2) * int(number_blocks_x / 4) + block_number_x * (new_block.rect.width + 2)
                new_block.rect.y = sb.bg_rect.height + 3 * new_block.rect.height + (new_block.rect.height + 2) * block_number_y
            blocks.add(new_block)


def set_loot_flag(new_block):
    """Установка лутфлага блоков при создании уровней"""
    new_block.loot_flag = True
    new_block.get_image()


def loose_try(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info):
    """Потеря попытки"""
    if stats.balls_left > 0:
        stats.balls_left -= 1
        arc_settings.initialize_default_settings()
        platform.reset_platform(arc_settings)
        stats.super_ball = False
        new_ball = Ball(arc_settings, screen, platform, stats, sb)
        balls.add(new_ball)
        guns.guns_active = False
        loots.empty()
        bullets.empty()
        sleep(0.5)
    else:
        stats.lose = True
        balls.empty()
        bullets.empty()
        bullets.update()
        loots.empty()
        blocks.empty()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        sleep(0.5)


def check_level_done(arc_settings, screen, platform, guns, bullets, balls, blocks, loots, stats, sb, info):
    """Проверка прохождения уровня"""
    platform.platform_center()
    for ball in balls:
        ball.reset_ball(arc_settings)
        ball.update()
    bullets.empty()
    bullets.update()
    loots.empty()
    blocks.empty()
    stats.level += 1
    sb.prep_score()
    sleep(0.5)
    if stats.level == 2:
        create_level_2(screen, blocks, sb)
    if stats.level == 3:
        create_level_3(arc_settings, screen, blocks, sb)
    if stats.level == 4:
        create_level_4(screen, blocks, sb)
    if stats.level == 5:
        create_level_5(screen, blocks, sb)
    if stats.level >= 6:
        balls.empty()
        info.prep_last_info()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.last_level_done = True


def score_increase_ball(arc_settings, stats, sb, collided_blocks):
    """Увеличение очков при уничтожении блока мячом"""
    stats.score += arc_settings.block_points * len(collided_blocks)
    sb.prep_score()
    check_high_score(stats, sb)


def score_increase_bullet(arc_settings, stats, sb, colided_blocks):
    """Увеличение очков при уничтожении блока пулей"""
    stats.score += arc_settings.block_points * len(colided_blocks)
    sb.prep_score()
    check_high_score(stats, sb)


def score_increase_loots(arc_settings, stats, sb):
    """Увеличение очков при пойманном лишнем луте"""
    stats.score += arc_settings.loot_points
    sb.prep_score()
    check_high_score(stats, sb)


def check_high_score(stats, sb):
    """Проверка лучшего результата"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score


def load_highest_score(stats):
    """Загрузка лучшего результата"""
    try:
        with open("hs.json", "r") as file_object:
            stats.high_score = json.load(file_object)
    except FileNotFoundError:
        stats.high_score = 0


def save_highest_score(stats):
    """Сохранение лучшего результата"""
    with open("hs.json", "w") as file_object:
        json.dump(stats.high_score, file_object)