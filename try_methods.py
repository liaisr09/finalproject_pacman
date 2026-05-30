import pygame
import math

WIDTH, HEIGHT = 775, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pacman")

BACKGROUND = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30
PLAYER_X, PLAYER_Y = 374, 431
PLAYER_VEL = 2

PI = math.pi
COLOR = (6, 7, 139)

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 23, bold=True)
SCORE = 0
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
    [0, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0], #2
    [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0], #3
    [0, 4, 2, 6, 1, 1, 5, 2, 6, 1, 1, 1, 5, 2, 4, 4, 2, 6, 1, 1, 1, 5, 2, 6, 1, 1, 5, 2, 4, 0], #4
    [0, 4, 3, 4, 0, 0, 4, 2, 4, 0, 0, 0, 4, 2, 4, 4, 2, 4, 0, 0, 0, 4, 2, 4, 0, 0, 4, 3, 4, 0], #5
    [0, 4, 2, 7, 1, 1, 8, 2, 7, 1, 1, 1, 8, 2, 7, 8, 2, 7, 1, 1, 1, 8, 2, 7, 1, 1, 8, 2, 4, 0], #6
    [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0], #7
    [0, 4, 2, 6, 1, 1, 5, 2, 6, 5, 2, 6, 1, 1, 1, 1, 1, 1, 5, 2, 6, 5, 2, 6, 1, 1, 5, 2, 4, 0], #8
    [0, 4, 2, 7, 1, 1, 8, 2, 4, 4, 2, 7, 1, 1, 5, 6, 1, 1, 8, 2, 4, 4, 2, 7, 1, 1, 8, 2, 4, 0], #9
    [0, 4, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 4, 0], #10
    [0, 7, 1, 1, 1, 1, 5, 2, 4, 7, 1, 1, 5, 0, 4, 4, 0, 6, 1, 1, 8, 4, 2, 6, 1, 1, 1, 1, 8, 0], #11
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 6, 1, 1, 8, 0, 7, 8, 0, 7, 1, 1, 5, 4, 2, 4, 0, 0, 0, 0, 0, 0], #12
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 2, 4, 0, 0, 0, 0, 0, 0], #13
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 4, 0, 6, 1, 9, 9, 9, 9, 1, 5, 0, 4, 4, 2, 4, 0, 0, 0, 0, 0, 0], #14
    [0, 0, 0, 0, 0, 0, 4, 2, 7, 8, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 7, 8, 2, 4, 0, 0, 0, 0, 0, 0], #15
    [0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 0], #16
    [0, 0, 0, 0, 0, 0, 4, 2, 6, 5, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 6, 5, 2, 4, 0, 0, 0, 0, 0, 0], #17
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 4, 0, 7, 1, 1, 1, 1, 1, 1, 8, 0, 4, 4, 2, 4, 0, 0, 0, 0, 0, 0], #18
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 2, 4, 0, 0, 0, 0, 0, 0], #19
    [0, 0, 0, 0, 0, 0, 4, 2, 4, 4, 0, 6, 1, 1, 1, 1, 1, 1, 5, 0, 4, 4, 2, 4, 0, 0, 0, 0, 0, 0], #20
    [0, 6, 1, 1, 1, 1, 8, 2, 7, 8, 0, 7, 1, 1, 5, 6, 1, 1, 8, 0, 7, 8, 2, 7, 1, 1, 1, 1, 5, 0], #21
    [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0], #22
    [0, 4, 2, 6, 1, 1, 5, 2, 6, 1, 1, 1, 5, 2, 4, 4, 2, 6, 1, 1, 1, 5, 2, 6, 1, 1, 5, 2, 4, 0], #23
    [0, 4, 2, 7, 1, 5, 4, 2, 7, 1, 1, 1, 8, 2, 7, 8, 2, 7, 1, 1, 1, 8, 2, 4, 6, 1, 8, 2, 4, 0], #24
    [0, 4, 3, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 3, 4, 0], #25
    [0, 7, 1, 5, 2, 4, 4, 2, 6, 5, 2, 6, 1, 1, 1, 1, 1, 1, 5, 2, 6, 5, 2, 4, 4, 2, 6, 1, 8, 0], #26
    [0, 6, 1, 8, 2, 7, 8, 2, 4, 4, 2, 7, 1, 1, 5, 6, 1, 1, 8, 2, 4, 4, 2, 7, 8, 2, 7, 1, 5, 0], #27
    [0, 4, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 4, 0], #28
    [0, 4, 2, 6, 1, 1, 1, 1, 8, 7, 1, 1, 5, 2, 4, 4, 2, 6, 1, 1, 8, 7, 1, 1, 1, 1, 5, 2, 4, 0], #29
    [0, 4, 2, 7, 1, 1, 1, 1, 1, 1, 1, 1, 8, 2, 7, 8, 2, 7, 1, 1, 1, 1, 1, 1, 1, 1, 8, 2, 4, 0], #30
    [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0], #31
    [0, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 0], #32
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #33
]

DIRECTION = 0
CNT = 0
FLICK = False

PLAYER1_IMAGES = [pygame.transform.scale(pygame.image.load("p1_1.png"), (40, 40)), pygame.transform.scale(pygame.image.load("p1_2.png"), (40, 40)),
                  pygame.transform.scale(pygame.image.load("p1_3.png"), (40, 40)), pygame.transform.scale(pygame.image.load("p1_4.png"), (40, 40))]
orange_ghost = pygame.transform.scale(pygame.image.load("orange.png"), (40, 40))
red_ghost = pygame.transform.scale(pygame.image.load("red.png"), (40, 40))
pink_ghost = pygame.transform.scale(pygame.image.load("pink.png"), (40, 40))
teal_ghost = pygame.transform.scale(pygame.image.load("teal.png"), (40, 40))

powerup = False
power_cnt = 0
eaten_ghosts = [False, False, False, False]
moving = False
startup_counter = 0
lives = 3

def draw_board():
    num1 = (HEIGHT // 33)
    num2 = (WIDTH // 29)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                pygame.draw.line(WINDOW, COLOR, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 *num1)), 4)
            if board[i][j] == 2:
                pygame.draw.circle(WINDOW, 'white', (j * num2 +(0.5*num2), i * num1 + (0.5 * num1)), 4)
            if board[i][j] == 3 and not FLICK:
                pygame.draw.circle(WINDOW, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if board[i][j] == 4:
                pygame.draw.line(WINDOW, COLOR, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 4)
            if board[i][j] == 5:
                pygame.draw.arc(WINDOW, COLOR, [(j*num2 - (num2*0.5)), (i * num1 +(0.5 * num1)), num2, num1,], 0, PI/2, 4)
            if board[i][j] == 6:
                pygame.draw.arc(WINDOW, COLOR, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI /2, PI, 4)
            if board[i][j] == 7:
                pygame.draw.arc(WINDOW, COLOR, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 4)
            if board[i][j] == 8:
                pygame.draw.arc(WINDOW, COLOR, [(j * num2 - (num2 * 0.4) - 2), (i * num1 - (0.4 * num1)), num2, num1], 3*PI /2, 2*PI, 4)
            if board[i][j] == 9:
                pygame.draw.line(WINDOW, 'white', (j * num2, i * num1 + (0.5*num2)), (j * num2 + num2, i * num1 + (0.5* num1)), 4)


def draw_player1():
    # 0-right, 1-left, 2-up, 3-down
    if DIRECTION == 0:
        WINDOW.blit(PLAYER1_IMAGES[CNT // 5], (PLAYER_X, PLAYER_Y))
    elif DIRECTION == 1:
        WINDOW.blit(pygame.transform.flip(PLAYER1_IMAGES[CNT // 5], True, False), (PLAYER_X, PLAYER_Y))
    elif DIRECTION == 2:
        WINDOW.blit(pygame.transform.rotate(PLAYER1_IMAGES[CNT // 5], 90), (PLAYER_X, PLAYER_Y))
    elif DIRECTION == 3:
        WINDOW.blit(pygame.transform.rotate(PLAYER1_IMAGES[CNT // 5], 270), (PLAYER_X, PLAYER_Y))

def draw_additions():
    WINDOW.blit(FONT.render(f"score: {SCORE}", True, 'white'), (15, 10))
    for i in range(lives):
        WINDOW.blit(pygame.transform.scale(PLAYER1_IMAGES[0], (20, 20)), (50 + i * 30, 770))
    if powerup:
        pygame.draw.circle(WINDOW, 'blue', (155, 780), 15)

def can_move(center_x, center_y):
    num1 = HEIGHT // 33
    num2 = WIDTH // 29
    row = center_y // num1
    col = center_x // num2

    return board[row][col] not in [1, 4, 5, 6, 7, 8, 9]


def check_points(x, y, powerup, power_cnt, eaten_ghosts):
    global SCORE
    num1 = HEIGHT // 33
    num2 = WIDTH // 29
    if board[y // num1][x // num2] == 2:
        SCORE += 10
        board[y // num1][x // num2] = 0
    if board[y // num1][x // num2] == 3:
        SCORE += 50
        board[y // num1][x // num2] = 0
        powerup = True
        power_cnt = 0
        eaten_ghosts = [False, False, False, False]
    return powerup, power_cnt, eaten_ghosts


def game_play():
    global PLAYER_X, PLAYER_Y, SCORE, PLAYER_VEL, CNT, DIRECTION, FLICK, moving, powerup, power_cnt, eaten_ghosts, startup_counter
    run = True
    clock = pygame.time.Clock()

    requested_direction = DIRECTION
    while run:
        clock.tick(60)
        if CNT < 19:
            CNT += 1
            if CNT > 2:
                FLICK = False
        else:
            CNT = 0
            FLICK = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if powerup and power_cnt < 600:
            power_cnt += 1
        elif powerup and power_cnt >= 600:
            power_cnt = 0
            powerup = False
            eaten_ghosts = [False, False, False, False]
        if startup_counter < 60:
            moving = False
            startup_counter += 1
        else:
            moving = True

        WINDOW.fill("black")
        draw_board()
        draw_player1()
        draw_additions()

        if moving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                requested_direction = 0
            elif keys[pygame.K_LEFT]:
                requested_direction = 1
            elif keys[pygame.K_UP]:
                requested_direction = 2
            elif keys[pygame.K_DOWN]:
                requested_direction = 3

            if requested_direction == 0 and can_move(PLAYER_X + PLAYER_VEL + 20, PLAYER_Y + 20):
                DIRECTION = 0
            elif requested_direction == 1 and can_move(PLAYER_X - PLAYER_VEL + 20, PLAYER_Y + 20):
                DIRECTION = 1
            elif requested_direction == 2 and can_move(PLAYER_X + 20, PLAYER_Y - PLAYER_VEL + 20):
                DIRECTION = 2
            elif requested_direction == 3 and can_move(PLAYER_X + 20, PLAYER_Y + PLAYER_VEL + 20):
                DIRECTION = 3

            if DIRECTION == 0 and can_move(PLAYER_X + PLAYER_VEL + 20, PLAYER_Y + 20):
                PLAYER_X += PLAYER_VEL
            elif DIRECTION == 1 and can_move(PLAYER_X - PLAYER_VEL + 20, PLAYER_Y + 20):
                PLAYER_X -= PLAYER_VEL
            elif DIRECTION == 2 and can_move(PLAYER_X + 20, PLAYER_Y - PLAYER_VEL + 20):
                PLAYER_Y -= PLAYER_VEL
            elif DIRECTION == 3 and can_move(PLAYER_X + 20, PLAYER_Y + PLAYER_VEL + 20):
                PLAYER_Y += PLAYER_VEL
        powerup, power_cnt, eaten_ghosts = check_points(PLAYER_X + 20, PLAYER_Y + 20, powerup, power_cnt, eaten_ghosts)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_play()