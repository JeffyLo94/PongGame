import pygame
import sys
import random
from pygame.locals import *
from PongPkg.GameObjects import GameStats
from PongPkg.GameObjects import Ball
from PongPkg.GameObjects import Bumper

# C O N S T A N T S
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CENTER_LINES = 25
CENTER_LINE_WIDTH = 5
CENTER_LINE_GAP = 10
SCORE_TOP = 200
SCORE_OFFSET_CENTER = 100
DARK_GREY = Color('#404040')
WHITE = Color('#FFFFFF')
TEXTCOLOR = WHITE
BACKGROUND_COLOR = DARK_GREY
FPS = 60

LEFT_KEYS = [K_LEFT, K_a]
RIGHT_KEYS = [K_RIGHT, K_d]
UP_KEYS = [K_UP, K_w]
DOWN_KEYS = [K_DOWN, K_s]

BALL_SIZE = 15
V_BUMPER_HT = 110
V_BUMPER_WH = 10
H_BUMPER_HT = 10
H_BUMPER_WH = 110

BALL_SPEED = 5
BUMPER_SPEED = 10

def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_decision():
    pressed = False
    while not pressed:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_n:
                    terminate()
                return


def wait_player_start_game():
    pressed = False
    while not pressed:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN:
                pressed = True
                return pressed


def draw_text( text, font, surface, x, y ):
    textObj = font.render(text, 1, TEXTCOLOR)
    textRect = textObj.get_rect()
    textRect.topleft = x, y
    surface.blit(textObj, textRect)

def ball_hit_objs( targets, ball ):
    for t in targets:
        if t.rect.colliderect(ball.rect):
            return True
    return False

def ball_exit_left( ball ):
    position = ball.get_pos()
    print(str(position))
    if position[0] < 0:
        return True
    if position[0] < WINDOWWIDTH/2 and (position[1] < 0 or position[1] > WINDOWHEIGHT):
        return True
    return False

def ball_exit_right( ball ):
    if ball.get_pos()[0] > WINDOWWIDTH:
        return True
    if ball.get_pos()[0] > WINDOWWIDTH/2 and (ball.get_pos()[1] < 0 or ball.get_pos()[1] > WINDOWHEIGHT):
        return True
    return False

def play():
    pygame.init()
    main_clock = pygame.time.Clock()
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('PONG - NO WALLS')
    pygame.mouse.set_visible(False)

    font = pygame.font.Font(None, 48)

    # SOUNDS
    game_over_sound = pygame.mixer.Sound('gameover.wav')
    win_sound = pygame.mixer.Sound('win.wav')
    lose_sound = pygame.mixer.Sound('lose.wav')
    ls_bump_sound = pygame.mixer.Sound('pong-blip.wav')
    rs_bump_sound = pygame.mixer.Sound('pong-blip2.wav')

    # IMAGES
    ls_bump_img = pygame.image.load('left-bumper.png')
    ls_bump_horiz_img = pygame.image.load('left-bumper-horiz.png')
    rs_bump_img = pygame.image.load('right-bumper.png')
    rs_bump_horiz_img = pygame.image.load('right-bumper-horiz.png')
    ball_img = pygame.image.load('ball.png')

    surface.fill(BACKGROUND_COLOR)

    draw_text('PONG', font, surface, WINDOWWIDTH/2-50, WINDOWHEIGHT/3)
    draw_text('Press a key to start.', font, surface, WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 3 + 50)
    pygame.display.update()
    wait_for_player_decision()

    #Main Game Loop
    play_game_again = True

    #Match stats
    gamestats = GameStats.GameStats()

    # Outer game loop
    while play_game_again:
        surface.fill(BACKGROUND_COLOR)

        #Match loop
        has_match_winner = False
        count = 1
        displayMsg = 'Game ' + str(count)
        while not has_match_winner:
            print(displayMsg)
            draw_text(displayMsg, font, surface, WINDOWWIDTH / 2-50, WINDOWHEIGHT / 3)
            draw_text('Press a key to start.', font, surface, WINDOWWIDTH / 2 - 150, WINDOWHEIGHT / 3 + 50)
            pygame.display.update()
            wait_player_start_game()

            # reset game_board state
            move_left = move_right = move_up = move_down = False
            ball = Ball.Ball(ball_img, BALL_SIZE, BALL_SPEED, WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            ls_bumper_top = Bumper.Bumper(ls_bump_horiz_img, WINDOWWIDTH/4, 0, H_BUMPER_WH, H_BUMPER_HT)
            ls_bumper_bot = Bumper.Bumper(ls_bump_horiz_img, WINDOWWIDTH/4, WINDOWHEIGHT, H_BUMPER_WH, H_BUMPER_HT)
            ls_bumper_side = Bumper.Bumper(ls_bump_img, 0, WINDOWHEIGHT/2, V_BUMPER_WH, V_BUMPER_HT)
            rs_bumper_top = Bumper.Bumper(rs_bump_horiz_img, WINDOWWIDTH/4 + WINDOWWIDTH/2, 0, H_BUMPER_WH, H_BUMPER_HT)
            rs_bumper_bot = Bumper.Bumper(rs_bump_horiz_img, WINDOWWIDTH/4 + WINDOWWIDTH/2, WINDOWHEIGHT, H_BUMPER_WH, H_BUMPER_HT)
            rs_bumper_side = Bumper.Bumper(rs_bump_img, WINDOWWIDTH, WINDOWHEIGHT/2, V_BUMPER_WH, V_BUMPER_HT)

            bumpers = [ls_bumper_bot, ls_bumper_top, ls_bumper_side, rs_bumper_bot, rs_bumper_top, rs_bumper_side]

            # Game loop
            play_game = True
            while play_game:
                for e in pygame.event.get():
                    if e.type == QUIT:
                        terminate()

                    if e.type == KEYDOWN:
                        move_left = e.key in LEFT_KEYS
                        move_right = e.key in RIGHT_KEYS
                        move_up = e.key in UP_KEYS
                        move_down = e.key in DOWN_KEYS

                    if e.type == KEYUP:
                        if e.key == K_ESCAPE:
                            terminate()

                        move_left = move_left and e.key in LEFT_KEYS
                        move_right = move_right and e.key in RIGHT_KEYS
                        move_up = move_up and e.key in UP_KEYS
                        move_down = move_down and e.key in DOWN_KEYS
                    #end for

                surface.fill(BACKGROUND_COLOR)

                # center line
                cr_height = WINDOWHEIGHT / (CENTER_LINES + CENTER_LINE_GAP)
                cr_width = CENTER_LINE_WIDTH
                cr_left = WINDOWWIDTH/2 - (CENTER_LINE_WIDTH/2)
                print('drawing center')
                for i in range(CENTER_LINES):
                    if i == 0:
                        cr = pygame.Rect(cr_left, i, cr_width, cr_height)
                        pygame.draw.rect(surface, WHITE, cr)
                    else:
                        cr = pygame.Rect(cr_left, (i*(cr_height+CENTER_LINE_GAP)), cr_width, cr_height)
                        pygame.draw.rect(surface, WHITE, cr)

                # ls score
                draw_text(str(gamestats.pLeftScore), font, surface, WINDOWWIDTH/2 - SCORE_OFFSET_CENTER, SCORE_TOP)
                # rs score
                draw_text(str(gamestats.pRightScore), font, surface, WINDOWWIDTH / 2 + SCORE_OFFSET_CENTER - 24,
                          SCORE_TOP)

                # Ball
                ball.update_pos()
                surface.blit(ball.surface, ball.rect)

                # Bumper Movement
                if move_left and rs_bumper_top.rect.left > WINDOWWIDTH/2:
                    rs_bumper_top.rect.move_ip(-1 * BUMPER_SPEED, 0)
                    rs_bumper_bot.rect.move_ip(-1 * BUMPER_SPEED, 0)
                if move_right and rs_bumper_top.rect.right < WINDOWWIDTH:
                    rs_bumper_top.rect.move_ip(1 * BUMPER_SPEED, 0)
                    rs_bumper_bot.rect.move_ip(1 * BUMPER_SPEED, 0)
                if move_up  and rs_bumper_side.rect.top > 0:
                    rs_bumper_side.rect.move_ip(0, -1 * BUMPER_SPEED)
                if move_down and rs_bumper_side.rect.bottom < WINDOWHEIGHT :
                    rs_bumper_side.rect.move_ip(1 * BUMPER_SPEED, 0)

                # COM movement
                ball_pos = ball.get_pos()
                if (ball_pos[0] < ls_bumper_top.rect.left) and (ls_bumper_top.rect.left > 0):
                    ls_bumper_top.rect.move_ip(-1 * BUMPER_SPEED, 0)
                    ls_bumper_bot.rect.move_ip(-1 * BUMPER_SPEED, 0)
                if (ball_pos[0] > ls_bumper_top.rect.right) and (ls_bumper_top.rect.right < WINDOWWIDTH/2):
                    ls_bumper_top.rect.move_ip(1 * BUMPER_SPEED, 0)
                    ls_bumper_bot.rect.move_ip(1 * BUMPER_SPEED, 0)
                if (ball_pos[1] < ls_bumper_side.rect.top) and (ls_bumper_side.rect.top > 0):
                    ls_bumper_side.rect.move_ip(0, -1 * BUMPER_SPEED)
                if (ball_pos[1] > ls_bumper_side.rect.bottom) and (ls_bumper_side.rect.bottom < WINDOWHEIGHT):
                    ls_bumper_side.rect.move_ip(0, 1 * BUMPER_SPEED)

                # collisions


                # Bumpers
                surface.blit(ls_bumper_top.surface, ls_bumper_top.rect)
                surface.blit(ls_bumper_bot.surface, ls_bumper_bot.rect)
                surface.blit(ls_bumper_side.surface, ls_bumper_side.rect)
                surface.blit(rs_bumper_top.surface, rs_bumper_top.rect)
                surface.blit(rs_bumper_bot.surface, rs_bumper_bot.rect)
                surface.blit(rs_bumper_side.surface, rs_bumper_side.rect)

                # check for ball position
                if ball_hit_objs( bumpers, ball):
                    print( 'bounce detected' )

                if ball_exit_left(ball):
                    print('rs gain point')
                    gamestats.increment_player_score('PR')
                    win_sound.play()
                    ball.reset()
                elif ball_exit_right(ball):
                    print('ls gain point')
                    gamestats.increment_player_score('PL')
                    lose_sound.play()
                    ball.reset()

                pygame.display.update()

                # check if game has winner
                print('game stats: ' + str(gamestats.has_game_winner()))
                if gamestats.has_game_winner()[0]:
                    print('ending game')
                    play_game = False
                    gamestats.reset_game()

                # wait_player_start_game()
                main_clock.tick(FPS)
                # end game loop
            count += 1
            displayMsg = 'Game ' + str(count)
            print(displayMsg)

            surface.fill(BACKGROUND_COLOR)

            # check if match has winner
            if gamestats.has_match_winner()[0]:
                has_match_winner = True
                print(has_match_winner)

            # end match loop

play()