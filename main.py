import pygame
from random import randrange as rnd
import base
from config import *

screen = base.Window(window.width, window.height, window.title)
screen.load_textures(['bg.jpg'])
screen.set_bg(base.BG_texture, 0)

dx, dy = 1, -1
fps = window.fps
lvl = game.lvl_min

def draw_ball(color1, color2=None):
    if color2 != None:
        pygame.draw.circle(screen.get(), color1, Ball.center, ball.radius)
        bx, by = Ball.x, Ball.y
        for i in range(1, 7):
            Ball.x -= ball.speed * dx
            Ball.y -= ball.speed * dy
            pygame.draw.circle(screen.get(), color2, Ball.center, int(ball.radius - i * 2))

        Ball.x, Ball.y = bx, by
    else:
        pygame.draw.circle(screen.get(), color1, Ball.center, ball.radius)

def generate(lvl):
    Paddle = pygame.Rect(window.width // 2 - paddle.width // 2, window.height - paddle.height - 10, paddle.width, paddle.height)
    Ball = pygame.Rect(rnd(ball.rect, window.width - ball.rect), window.height // 2, ball.rect, ball.rect)

    blocks_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(lvl)]
    colors_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(lvl)]

    return Paddle, Ball, blocks_list, colors_list

Paddle, Ball, blocks_list, colors_list = generate(lvl)

def detect_collision(dx, dy, Ball, rect):
    if dx>0:
        delta_x = Ball.right - rect.left
    else:
        delta_x = rect.right - Ball.left

    if dy > 0:
        delta_y = Ball.bottom - rect.top
    else:
        delta_y = rect.bottom - Ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_x < delta_y:
        dx = -dx

    return dx, dy

started = False
score = 0

def pause():
    global started
    started = not started

screen.keypressed(pygame.K_F1, pause)

def game_over_event(because):
    global fps, Paddle, Ball, blocks_list, colors_list, score, lvl
    print(because)
    print('Your score: ' + str(score))
    fps = window.fps
    if because == 'YOU WIN!':
        if lvl != game.lvl_max:
            lvl += 1
        else:
            lvl = game.lvl_min
        null1, null2, blocks_list, colors_list = generate(lvl)
        Ball.x, Ball.y = Paddle.x, Paddle.y - paddle.height
    else:
        lvl = game.lvl_min
        score = 0
        pause()
        Paddle, Ball, blocks_list, colors_list = generate(lvl)

def body():
    global dx, dy, fps, started, Paddle, Ball, blocks_list, colors_list, score

    # control
    if started:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and Paddle.left > 0:
            Paddle.left -= paddle.speed
        if key[pygame.K_RIGHT] and Paddle.right < window.width:
            Paddle.right += paddle.speed

        # ball movement
        Ball.x += ball.speed * dx
        Ball.y += ball.speed * dy

        # ball collision
        if Ball.centerx < ball.radius or Ball.centerx > window.width - ball.radius:
            dx = -dx
        if Ball.centery < ball.radius:
            dy = -dy

        # game over
        if Ball.bottom > window.height:
            game_over_event('GAME OVER')
        elif not len(blocks_list):
            game_over_event('YOU WIN!')

        # paddle collision
        if Ball.colliderect(Paddle) and dy > 0:
            dy, dy = detect_collision(dx, dy, Ball, Paddle)

        # blocks collision
        hit_index = Ball.collidelist(blocks_list)
        if hit_index != -1:
            hit_rect = blocks_list.pop(hit_index)
            hit_color = colors_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, Ball, hit_rect)

            # special effects
            hit_rect.inflate_ip(Ball.width * 3, Ball.height * 3)
            pygame.draw.rect(screen.get(), hit_color, hit_rect)
            fps += 2
            score+=1

        lvl_score = (fps-window.fps)//2
        if lvl_score >= 15 and lvl_score < 30:
            draw_ball(base.Color.yellow)
        elif lvl_score >= 30 and lvl_score < 45:
            draw_ball(base.Color.orange, base.Color.yellow)
        elif lvl_score >=45:
            draw_ball(base.Color.darkred, base.Color.red)
        else:
            draw_ball(base.Color.white)

    # drawing
    pygame.draw.rect(screen.get(), base.Color.darkred, Paddle)

    [pygame.draw.rect(screen.get(), colors_list[color], block) for color, block in enumerate(blocks_list)]
    screen.set_fps(fps)
    font = pygame.font.SysFont('Roboto', int(window.width*0.04), bold=True)
    pos_view = font.render('Score: '+str(score), 0, base.Color.red)
    screen.get().blit(pos_view, (5, 5))

screen.set_loop(body, window.fps)

screen.create()