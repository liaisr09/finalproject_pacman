_author__: 'Lia Israeli'

import tkinter as tk
from tkinter import ttk
import socket
import pickle
import threading
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pygame
import math
import struct


clt_sock = socket.socket()
clt_sock.connect(("192.168.1.125", 65432))
curr_user = None
username_var = None
password_var = None
status_label = None
to_var = None
send_msg_var = None
text_box = None
sign_up_username_var = None
sign_up_password_var = None
aes_key = None
server_public_key = None
PLAYER_ID = None
waiting_root = None

positions_lock = threading.Lock()

GAME_POSITIONS = {"p1_x": 414, "p1_y": 431, "p1_score": 0, "p1_lives": 3, "p1_dir": 0,
    "p2_x": 334, "p2_y": 431, "p2_score": 0, "p2_lives": 3, "p2_dir": 0,}
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

PLAYER1_IMAGES = []
PLAYER2_IMAGES = []
orange_img = None
red_img = None
pink_img = None
teal_img = None
vulnerable_img = None
dead_img = None

WIDTH, HEIGHT = 775, 800
WINDOW = None
PI = math.pi
COLOR = (6, 7, 139)
FLICK = False
DIRECTION = 0
CNT = 0


def send_packet(sock, obj):
    data = pickle.dumps(obj)
    header = struct.pack("!I", len(data))
    sock.sendall(header + data)

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data

def recv_packet(sock):
    header = recv_exact(sock, 4)
    if header is None:
        return None
    length = struct.unpack("!I", header)[0]
    payload = recv_exact(sock, length)
    if payload is None:
        return None
    return pickle.loads(payload)

def listen_server():
    global curr_user, server_public_key, PLAYER_ID, GAME_POSITIONS, aes_key, GAME_POSITIONS, board
    while True:
        try:
            msg = recv_packet(clt_sock)
            if msg is None:
                break
            if "encrypted" in msg:
                msg = decrypt(msg["encrypted"], aes_key, msg["iv"])
            status = msg.get("status")
            if status == "ok":
                curr_user = msg.get("username", curr_user)
                login_root.after(0, login_success)
            elif status == "signup_ok":
                print("Registration successful")
            elif status == "error":
                error_msg = msg.get("message", "Operation failed")
                print(f"Error: {error_msg}")
            elif status == "public_key":
                server_public_key = serialization.load_pem_public_key(msg["key"])
                aes_key = secrets.token_bytes(32)
                encrypted_key = server_public_key.encrypt(aes_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
                send_packet(clt_sock, {"action": "send_key", "key": encrypted_key})
            elif status == "waiting":
                print("Waiting for second player")
            elif status == "game_start":
                PLAYER_ID = msg["player_id"]
                login_root.after(0, close_tk_and_start_game)
            elif status == "position":
                with positions_lock:
                    GAME_POSITIONS = msg["position"]
                    if "board" in msg:
                        board = msg["board"]
        except Exception as e:
            print("Listen error:", e)
            break

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

def request_public_key():
    data = {"action": "get_public_key"}
    send_packet(clt_sock, data)

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    plaintext = pickle.dumps(data)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext, cipher.iv

def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pickle.loads(plaintext)

def login_success():
    login_root.withdraw()
    waiting_room_screen()


def try_login():
    data = {"action": "login", "username": username_var.get(), "password": password_var.get()}
    send_encrypted(data)


def waiting_room_screen():
    global waiting_root
    waiting_root = tk.Toplevel()
    waiting_root.geometry("400x200")
    waiting_root.title("Waiting Room")
    waiting_root.configure(bg="blue")
    tk.Label(waiting_root,text="Waiting for second player...", font=("Fixedsys", 15, "bold"), bg="yellow").pack(pady=50)
    send_encrypted({"action": "join_game"})

def close_tk_and_start_game():
    global waiting_root
    if waiting_root and waiting_root.winfo_exists():
        waiting_root.destroy()
    login_root.destroy()
    start_game()

def start_game():
    global CNT, DIRECTION, WINDOW, FLICK, PLAYER1_IMAGES, PLAYER2_IMAGES, orange_img, red_img, pink_img, teal_img, vulnerable_img, dead_img
    pygame.init()
    pygame.font.init()

    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pacman")
    FONT = pygame.font.SysFont("Fixedsys", 22, bold=True)
    BIG_FONT = pygame.font.SysFont("Fixedsys", 40, bold=True)
    PLAYER1_IMAGES = [pygame.transform.scale(pygame.image.load("p1_1.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p1_2.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p1_3.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p1_4.png"), (40, 40))]
    PLAYER2_IMAGES = [pygame.transform.scale(pygame.image.load("p2_1.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p2_2.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p2_3.png"), (40, 40)),
                      pygame.transform.scale(pygame.image.load("p2_4.png"), (40, 40))]
    orange_img = pygame.transform.scale(pygame.image.load("orange.png"), (50, 50))
    red_img = pygame.transform.scale(pygame.image.load("red.png"), (50, 50))
    pink_img = pygame.transform.scale(pygame.image.load("pink.png"), (50, 50))
    teal_img = pygame.transform.scale(pygame.image.load("teal.png"), (50, 50))
    vulnerable_img = pygame.transform.scale(pygame.image.load("vulnerable.png"), (40, 40))
    dead_img = pygame.transform.scale(pygame.image.load("dead.png"), (50, 50))

    current_dir = None
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WINDOW.fill('black')

        if GAME_POSITIONS.get("game_over", False):
            winner = GAME_POSITIONS.get("winner", "None")
            reason = GAME_POSITIONS.get("reason", "")
            txt_game_over = BIG_FONT.render("GAME OVER", True, (255, 0, 0))
            txt_winner = FONT.render(f"Winner: {winner}", True, (255, 255, 255))
            txt_reason = FONT.render(reason, True, (200, 200, 200))
            WINDOW.blit(txt_game_over, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            WINDOW.blit(txt_winner, (WIDTH // 2 - 80, HEIGHT // 2 + 10))
            WINDOW.blit(txt_reason, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_dir = "right"
                    DIRECTION = 0
                elif event.key == pygame.K_LEFT:
                    current_dir = "left"
                    DIRECTION = 1
                elif event.key == pygame.K_UP:
                    current_dir = "up"
                    DIRECTION = 2
                elif event.key == pygame.K_DOWN:
                    current_dir = "down"
                    DIRECTION = 3
        if current_dir:
            send_encrypted({"action": "move", "direction": current_dir})
        CNT += 1
        if CNT >= 20:
            CNT = 0
            FLICK = not FLICK

        with positions_lock:
            draw_board()
            draw_player1()
            draw_player2()
            draw_ghosts()

        p1_stats = f"P1 Score: {GAME_POSITIONS.get('p1_score', 0)}  Lives: {GAME_POSITIONS.get('p1_lives', 0)}"
        p2_stats = f"P2 Score: {GAME_POSITIONS.get('p2_score', 0)}  Lives: {GAME_POSITIONS.get('p2_lives', 0)}"
        txt_p1 = FONT.render(p1_stats, True, (255, 255, 0))
        txt_p2 = FONT.render(p2_stats, True, (248, 121, 198))
        WINDOW.blit(txt_p1, (15, 15))
        WINDOW.blit(txt_p2, (WIDTH - 280, 15))
        pygame.display.flip()
    pygame.quit()

def draw_player1():
    # 0-right, 1-left, 2-up, 3-down
    p1_x = GAME_POSITIONS.get("p1_x", 414)
    p1_y = GAME_POSITIONS.get("p1_y", 431)
    direction = GAME_POSITIONS.get("p1_dir", 0)
    if direction == 0:
        WINDOW.blit(PLAYER1_IMAGES[CNT // 5], (p1_x, p1_y))
    elif direction == 1:
        WINDOW.blit(pygame.transform.flip(PLAYER1_IMAGES[CNT // 5], True, False), (p1_x, p1_y))
    elif direction == 2:
        WINDOW.blit(pygame.transform.rotate(PLAYER1_IMAGES[CNT // 5], 90), (p1_x, p1_y))
    elif direction == 3:
        WINDOW.blit(pygame.transform.rotate(PLAYER1_IMAGES[CNT // 5], 270), (p1_x, p1_y))

def draw_player2():
    # 0-right, 1-left, 2-up, 3-down
    p2_x = GAME_POSITIONS.get("p2_x", 334)
    p2_y = GAME_POSITIONS.get("p2_y", 431)
    direction = GAME_POSITIONS.get("p2_dir", 0)
    if direction == 0:
        WINDOW.blit(PLAYER2_IMAGES[CNT // 5], (p2_x, p2_y))
    elif direction == 1:
        WINDOW.blit(pygame.transform.flip(PLAYER2_IMAGES[CNT // 5], True, False), (p2_x, p2_y))
    elif direction == 2:
        WINDOW.blit(pygame.transform.rotate(PLAYER2_IMAGES[CNT // 5], 90), (p2_x, p2_y))
    elif direction == 3:
        WINDOW.blit(pygame.transform.rotate(PLAYER2_IMAGES[CNT // 5], 270), (p2_x, p2_y))


def draw_ghosts():
    ghosts_data = GAME_POSITIONS.get("ghosts", {})
    red = ghosts_data.get("red")
    pink = ghosts_data.get("pink")
    teal = ghosts_data.get("teal")
    orange = ghosts_data.get("orange")
    if red:
        if red["dead"]:
            WINDOW.blit(dead_img, (red["x"], red["y"]))
        elif GAME_POSITIONS.get("powerup"):
            WINDOW.blit(vulnerable_img, (red["x"], red["y"]))
        else:
            WINDOW.blit(red_img, (red["x"], red["y"]))
    if pink:
        if pink["dead"]:
            WINDOW.blit(dead_img, (pink["x"], pink["y"]))
        elif GAME_POSITIONS.get("powerup"):
            WINDOW.blit(vulnerable_img, (pink["x"], pink["y"]))
        else:
            WINDOW.blit(pink_img, (pink["x"], pink["y"]))
    if teal:
        if teal["dead"]:
            WINDOW.blit(dead_img, (teal["x"], teal["y"]))
        elif GAME_POSITIONS.get("powerup"):
            WINDOW.blit(vulnerable_img, (teal["x"], teal["y"]))
        else:
            WINDOW.blit(teal_img, (teal["x"], teal["y"]))
    if orange:
        if orange["dead"]:
            WINDOW.blit(dead_img, (orange["x"], orange["y"]))
        elif GAME_POSITIONS.get("powerup"):
            WINDOW.blit(vulnerable_img, (orange["x"], orange["y"]))
        else:
            WINDOW.blit(orange_img, (orange["x"], orange["y"]))


def send_encrypted(data):
    global aes_key, clt_sock
    if aes_key is None:
        print("AES key not ready")
        return
    ciphertext, iv = encrypt(data, aes_key)
    packet = {"encrypted": ciphertext, "iv": iv}
    send_packet(clt_sock, packet)

def signup():
    send_encrypted({"action": "signup", "username": sign_up_username_var.get(), "password": sign_up_password_var.get()})


def open_signup():
    global sign_up_username_var, sign_up_password_var
    signup_root = tk.Toplevel()
    signup_root.geometry('300x250')
    signup_root.title('Sign Up')
    signup_root.configure(bg="blue")

    tk.Label(signup_root,text='Username', font=("Fixedsys", 15, "bold"), bg="yellow").pack(pady=10)

    sign_up_username_var = tk.StringVar()
    ttk.Entry(signup_root, textvariable=sign_up_username_var).pack(pady=5)

    tk.Label(signup_root,text='Password', font=("Fixedsys", 15, "bold"), bg="pink").pack(pady=10)

    sign_up_password_var = tk.StringVar()
    ttk.Entry(signup_root, show="*", textvariable=sign_up_password_var).pack(pady=5)

    tk.Button(signup_root, text="Register", font=("Fixedsys", 10, "bold"), command=signup).pack(pady=10)




def opening_screen():
    global username_var, password_var, status_label, login_root
    login_root = tk.Tk()
    login_root.geometry('400x400')
    login_root.title('start game')
    login_root.configure(bg="blue")

    tk.Label(login_root, text='TWO PLAYER PAC-MAN', font=("Fixedsys", 20, "bold"), fg="yellow", bg="blue").pack(pady=20)

    tk.Label(login_root, text='Username:', font=("Fixedsys", 15, "bold"), bg="pink").pack(pady=20)
    username_var = tk.StringVar()
    ttk.Entry(login_root, width=27, textvariable=username_var).pack(pady=2)

    tk.Label(login_root, text='Password:', font=("Fixedsys", 15, "bold"), bg="yellow").pack(pady=15)
    password_var = tk.StringVar()
    ttk.Entry(login_root, width=27, show='*', textvariable=password_var).pack(pady=10)

    tk.Button(login_root, width=18, text="Login", font=("Fixedsys", 10, "bold"), command=try_login).pack(pady=7)

    tk.Button(login_root, width=18, text="Sign Up", font=("Fixedsys", 10, "bold"), command=open_signup).pack(pady=7)

    threading.Thread(target=listen_server,daemon=True).start()
    request_public_key()
    login_root.mainloop()

if __name__ == "__main__":
    opening_screen()