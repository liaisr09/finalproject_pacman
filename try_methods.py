import pygame
import math

WIDTH, HEIGHT = 775, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pacman")

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
WALLS = [1, 4, 5, 6, 7, 8, 9]
FLICK = False

PLAYER1_IMAGES = [pygame.transform.scale(pygame.image.load("p1_1.png"), (40, 40)), pygame.transform.scale(pygame.image.load("p1_2.png"), (40, 40)),
                  pygame.transform.scale(pygame.image.load("p1_3.png"), (40, 40)), pygame.transform.scale(pygame.image.load("p1_4.png"), (40, 40))]
orange_img = pygame.transform.scale(pygame.image.load("orange.png"), (50, 50))
red_img = pygame.transform.scale(pygame.image.load("red.png"), (50, 50))
pink_img = pygame.transform.scale(pygame.image.load("pink.png"), (50, 50))
teal_img = pygame.transform.scale(pygame.image.load("teal.png"), (50, 50))
vulnerable_img = pygame.transform.scale(pygame.image.load("vulnerable.png"), (40, 40))
dead_img = pygame.transform.scale(pygame.image.load("dead.png"), (50, 50))

red_x, red_y, red_direction = 365, 275, 0
teal_x, teal_y, teal_direction = 315, 340, 2
pink_x, pink_y, pink_direction = 365, 340, 2
orange_x, orange_y, orange_direction = 415, 340, 2
released_red= False
released_pink = False
released_teal = False
released_orange = False

powerup = False
power_cnt = 0
eaten_ghosts = [False, False, False, False]
targets = [(PLAYER_X, PLAYER_Y), (PLAYER_X, PLAYER_Y), (PLAYER_X, PLAYER_Y), (PLAYER_X, PLAYER_Y)]
red_dead, teal_dead, pink_dead, orange_dead = False, False, False, False
red_box, teal_box, pink_box, orange_box = False, True, True, True
ghost_speed = 2
moving = False
startup_counter = 0
ghost_release_timer = 0
lives = 3
spawn_positions = [(365, 340), (315, 340), (365, 340), (415, 340)]

class Ghost:
    def __init__(self, x, y, target, speed, img, direction, is_dead, in_box, id, released):
        self.x = x
        self.y = y
        self.center_x = self.x + 22
        self.center_y = self.y + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.is_dead = is_dead
        self.in_box = in_box
        self.id = id
        self.released = released
        self.turns = self.check_turns()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.is_dead) or (eaten_ghosts[self.id] and powerup and not self.is_dead):
            WINDOW.blit(self.img, (self.x, self.y))
        elif powerup and not self.is_dead and not eaten_ghosts[self.id]:
            WINDOW.blit(vulnerable_img, (self.x, self.y))
        else:
            WINDOW.blit(dead_img, (self.x, self.y))
        ghost_rect = pygame.rect.Rect((self.center_x - 25, self.center_y - 25), (50,50))
        return ghost_rect

    def check_turns(self):
        turns = [False, False, False, False]
        num1 = HEIGHT // 33
        num2 = WIDTH // 29
        row = (self.y + 4) // num1
        col = (self.x + 4) // num2

        allowed_walls = [1, 4, 5, 6, 7, 8] if self.is_dead else WALLS
        if col + 1 < len(board[0]) and board[row][col + 1] not in allowed_walls:
            turns[0] = True
        if col - 1 >= 0 and board[row][col - 1] not in allowed_walls:
            turns[1] = True
        if row - 1 >= 0 and board[row - 1][col] not in allowed_walls:
            turns[2] = True
        if row + 1 < len(board) and board[row + 1][col] not in allowed_walls:
            turns[3] = True
        return turns

    def move(self):
        global eaten_ghosts
        num1 = HEIGHT // 33
        num2 = WIDTH // 29
        row = (self.y + 4) // num1
        col = (self.x + 4) // num2
        if not self.released:
            return
        if self.is_dead:
            self.speed = 4
            if abs(self.x - 365) > self.speed:
                if self.x < 365:
                    self.x += self.speed
                else:
                    self.x -= self.speed
            elif self.y > 272:
                self.x = 365
                self.y -= self.speed
            else:
                self.x, self.y = spawn_positions[self.id]
                self.is_dead = False
                self.in_box = True
                self.direction = 2
                eaten_ghosts[self.id] = False
            self.center_x = self.x + 22
            self.center_y = self.y + 22
            return

        if self.in_box:
            if self.y > 275:
                if abs(self.x - 365) <= self.speed:
                    self.x = 365
                    self.y -= self.speed
                elif self.x < 365:
                    self.x += self.speed
                elif self.x > 365:
                    self.x -= self.speed
            else:
                self.in_box = False
                self.direction = 0
            self.center_x = self.x + 22
            self.center_y = self.y + 22
            return

        exact_center_x = col * num2 + (num2 // 2)
        exact_center_y = row * num1 + (num1 // 2)

        is_at_center_x = abs(self.center_x - exact_center_x) < self.speed
        is_at_center_y = abs(self.center_y - exact_center_y) < self.speed
        is_blocked = not self.check_turns()[self.direction]

        if (is_at_center_x and is_at_center_y) or is_blocked:
            self.turns = self.check_turns()
            best_direction = self.direction
            min_distance = float('inf')
            for d in range(4):
                if self.turns[d]:
                    if not is_blocked:
                        if (d == 0 and self.direction == 1) or (d == 1 and self.direction == 0) or \
                                (d == 2 and self.direction == 3) or (d == 3 and self.direction == 2):
                            continue
                    next_col = col + (1 if d == 0 else -1 if d == 1 else 0)
                    next_row = row + (1 if d == 3 else -1 if d == 2 else 0)
                    next_x = next_col * num2 + (num2 // 2)
                    next_y = next_row * num1 + (num1 // 2)
                    distance = math.sqrt((next_x - self.target[0]) ** 2 + (next_y - self.target[1]) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = d

            if not self.check_turns()[best_direction]:
                for d in range(4):
                    if self.check_turns()[d]:
                        best_direction = d
                        break
            self.direction = best_direction

        turns_available = self.check_turns()
        if self.direction == 0 and turns_available[0]:
            self.x += self.speed
        elif self.direction == 1 and turns_available[1]:
            self.x -= self.speed
        elif self.direction == 2 and turns_available[2]:
            self.y -= self.speed
        elif self.direction == 3 and turns_available[3]:
            self.y += self.speed

        self.center_x = self.x + 22
        self.center_y = self.y + 22



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
    pygame.draw.circle(WINDOW, 'red', (305, 328), 5)
    pygame.draw.circle(WINDOW, 'red', (480, 328), 5)
    pygame.draw.circle(WINDOW, 'red', (305, 418), 5)
    pygame.draw.circle(WINDOW, 'red', (480, 418), 5)

def can_move(center_x, center_y):
    num1 = HEIGHT // 33
    num2 = WIDTH // 29
    row = center_y // num1
    col = center_x // num2
    return board[row][col] not in WALLS

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


def reset_positions():
    global PLAYER_X, PLAYER_Y, DIRECTION, startup_counter, moving, ghost_release_timer
    global red_x, red_y, red_direction, red_box, red_dead
    global teal_x, teal_y, teal_direction, teal_box, teal_dead
    global pink_x, pink_y, pink_direction, pink_box, pink_dead
    global orange_x, orange_y, orange_direction, orange_box, orange_dead
    global released_pink, released_teal, released_orange, released_red

    PLAYER_X, PLAYER_Y = 374, 431
    DIRECTION = 0

    red_x, red_y, red_direction = 365, 275, 0
    teal_x, teal_y, teal_direction = 315, 340, 2
    pink_x, pink_y, pink_direction = 365, 340, 2
    orange_x, orange_y, orange_direction = 415, 340, 2

    red_dead, teal_dead, pink_dead, orange_dead = False, False, False, False
    red_box, teal_box, pink_box, orange_box = False, True, True, True

    released_red = False
    released_pink = False
    released_teal = False
    released_orange = False

    startup_counter = 0
    ghost_release_timer = 0
    moving = False


def game_play():
    global PLAYER_X, PLAYER_Y, SCORE, PLAYER_VEL, CNT, DIRECTION, FLICK, moving, powerup, power_cnt, eaten_ghosts, startup_counter, ghost_release_timer
    global red_x, red_y, red_direction, red_box, red_dead, teal_x, teal_y, teal_direction, teal_box, teal_dead, \
        pink_x, pink_y, pink_direction, pink_box, pink_dead, orange_x, orange_y, orange_direction, orange_box, orange_dead, lives, \
        released_pink, released_teal, released_orange, released_red
    run = True
    clock = pygame.time.Clock()
    ghosts_in_powerup = 0
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
            ghosts_in_powerup = 0
            power_cnt = 0
            powerup = False
            eaten_ghosts = [False, False, False, False]
        if startup_counter < 60:
            moving = False
            startup_counter += 1
        else:
            moving = True
        if moving:
            ghost_release_timer += 1

        WINDOW.fill("black")
        draw_board()
        draw_player1()

        num1 = HEIGHT // 33
        num2 = WIDTH // 29
        target_red = (PLAYER_X + 20, PLAYER_Y + 20)
        target_teal = (PLAYER_X + 20 + (num2 * 2), PLAYER_Y + 20)
        target_pink = (PLAYER_X + 20, PLAYER_Y + 20 - (num1 * 2))
        distance_to_pacman = math.sqrt((orange_x - PLAYER_X) ** 2 + (orange_y - PLAYER_Y) ** 2)
        if distance_to_pacman > num2 * 5:
            target_orange = (PLAYER_X + 20, PLAYER_Y + 20)
        else:
            target_orange = (num2, HEIGHT - num1 - 2)
        targets = [target_red, target_teal, target_pink, target_orange]

        if ghost_release_timer > 100 and not released_red:
            red_box = True
            released_red = True
        if ghost_release_timer > 220 and not released_pink:
            pink_box = True
            released_pink = True
        if ghost_release_timer > 340 and not released_teal:
            teal_box = True
            released_teal = True
        if ghost_release_timer > 460 and not released_orange:
            orange_box = True
            released_orange = True

        red = Ghost(red_x, red_y, targets[0], ghost_speed, red_img, red_direction, red_dead, red_box, 0, released_red)
        teal = Ghost(teal_x, teal_y, targets[1], ghost_speed, teal_img, teal_direction, teal_dead, teal_box, 1, released_teal)
        pink = Ghost(pink_x, pink_y, targets[2], ghost_speed, pink_img, pink_direction, pink_dead, pink_box, 2, released_pink)
        orange = Ghost(orange_x, orange_y, targets[3], ghost_speed, orange_img, orange_direction, orange_dead, orange_box, 3, released_orange)
        if moving:
            red.move()
            red_x, red_y, red_direction, red_box, red_dead = red.x, red.y, red.direction, red.in_box, red.is_dead
            teal.move()
            teal_x, teal_y, teal_direction, teal_box, teal_dead = teal.x, teal.y, teal.direction, teal.in_box, teal.is_dead
            pink.move()
            pink_x, pink_y, pink_direction, pink_box, pink_dead = pink.x, pink.y, pink.direction, pink.in_box, pink.is_dead
            orange.move()
            orange_x, orange_y, orange_direction, orange_box, orange_dead = orange.x, orange.y, orange.direction, orange.in_box, orange.is_dead

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

        PLAYER_RECT = pygame.Rect(PLAYER_X, PLAYER_Y, 40, 40)
        if moving:
            if PLAYER_RECT.colliderect(red.rect):
                if powerup:
                    if not red.is_dead and not eaten_ghosts[0]:
                        ghosts_in_powerup += 1
                        red_dead = True
                        eaten_ghosts[0] = True
                        SCORE += 200 * ghosts_in_powerup
                else:
                    lives -= 1
                    reset_positions()
            if PLAYER_RECT.colliderect(teal.rect):
                if powerup:
                    if not teal.is_dead and not eaten_ghosts[1]:
                        ghosts_in_powerup += 1
                        teal_dead = True
                        eaten_ghosts[1] = True
                        SCORE += 200 * ghosts_in_powerup
                else:
                    lives -= 1
                    reset_positions()
            if PLAYER_RECT.colliderect(pink.rect):
                if powerup:
                    if not pink.is_dead and not eaten_ghosts[2]:
                        ghosts_in_powerup += 1
                        pink_dead = True
                        eaten_ghosts[2] = True
                        SCORE += 200 * ghosts_in_powerup
                else:
                    lives -= 1
                    reset_positions()
            if PLAYER_RECT.colliderect(orange.rect):
                if powerup:
                    if not orange.is_dead and not eaten_ghosts[3]:
                        ghosts_in_powerup += 1
                        orange_dead = True
                        eaten_ghosts[3] = True
                        SCORE += 200 * ghosts_in_powerup
                else:
                    lives -= 1
                    reset_positions()

        draw_additions()
        powerup, power_cnt, eaten_ghosts = check_points(PLAYER_X + 20, PLAYER_Y + 20, powerup, power_cnt, eaten_ghosts)

        if lives <= 0:
            run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_play()