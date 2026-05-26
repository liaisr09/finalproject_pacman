from pickle import GLOBAL

import pygame
import time

WIDTH, HEIGHT = 775, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pacman")

BACKGROUND = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30
PLAYER_X, PLAYER_Y = 374, 428
PLAYER_VEL = 2

BORDER_COLOR = WINDOW.get_at((56, 128))

def draw(player):
    WINDOW.blit(BACKGROUND, (0, 0))

    WINDOW.blit(player, (PLAYER_X, PLAYER_Y))

    pygame.display.update()

def game_play():
    global PLAYER_X, PLAYER_Y, WIDTH, HEIGHT
    run = True

    player = pygame.transform.scale(pygame.image.load("player_1.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and PLAYER_X - PLAYER_VEL >= 0: #ADD BORDER RECOGNITION
            PLAYER_X -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and PLAYER_Y + PLAYER_VEL + PLAYER_WIDTH <= WIDTH: #NOT WORKING?
            PLAYER_X += PLAYER_VEL
        if keys[pygame.K_UP] and PLAYER_Y - PLAYER_VEL >= 0:
            PLAYER_Y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and PLAYER_Y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            PLAYER_Y += PLAYER_VEL

        draw(player)

    pygame.quit()

if __name__ == "__main__":
   game_play()
