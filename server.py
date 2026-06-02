__author__: 'Lia Israeli'

import socket
import threading
import pickle
from AsyncMessages import AsyncMessages
import hashlib
import os
import secrets
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import math
import traceback
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import struct

USERS_FILE = "users.pkl"
PEPPER_FILE = "pepper.bin"
keys_by_user = {}
PRIVATE_KEY_FILE = "private.pem"
PUBLIC_KEY_FILE = "public.pem"

if os.path.exists(PEPPER_FILE):
    with open(PEPPER_FILE, "rb") as f:
        PEPPER = f.read()
else:
    PEPPER = secrets.token_bytes(32)
    with open(PEPPER_FILE, "wb") as f:
        f.write(PEPPER)

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

WIDTH, HEIGHT = 775, 800
PLAYER_VEL = 2
waiting_players = []
PLAYERS = {}
WALLS = [1, 4, 5, 6, 7, 8, 9]
SCORE = 0
lives = 3
powerup = False
power_cnt = 0
GHOST_RELEASE_COUNTER = 0
POWERUP_COUNTER = 0

async_msgs = AsyncMessages()
user_by_sock = {}
game_lock = threading.Lock()
waiting_lock = threading.Lock()

def count_initial_points():
    count = 0
    for row in board:
        for cell in row:
            if cell == 2 or cell == 3:
                count += 1
    return count

TOTAL_POINTS_ON_BOARD = count_initial_points()

GAME_POSITIONS = {
    "p1_x": 414, "p1_y": 431, "p1_score": 0, "p1_lives": 3, "p1_dir": 0,
    "p2_x": 334, "p2_y": 431, "p2_score": 0, "p2_lives": 3, "p2_dir": 0,
    "game_over": False,
    "winner": None,
    "reason": "",
    "ghosts": {
        "red": {"x": 365, "y": 275},
        "teal": {"x": 315, "y": 340},
        "pink": {"x": 365, "y": 340},
        "orange": {"x": 415, "y": 340}
}}
spawn_positions = [(365, 340), (315, 340), (365, 340), (415, 340)]

class Ghost:
    def __init__(self, x, y, id, direction, is_dead, in_box, released):
        self.x = x
        self.y = y
        self.center_x = self.x + 22
        self.center_y = self.y + 22
        self.direction = direction
        self.is_dead = is_dead
        self.in_box = in_box
        self.turns = self.check_turns()
        self.released = released
        self.speed = 2
        self.id = id
        self.target = (374, 431)

    def check_turns(self):
        turns = [False, False, False, False]
        num1 = HEIGHT // 33
        num2 = WIDTH // 29
        row = self.center_y // num1
        col = self.center_x // num2

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

    def update_target_and_move(self):
        p1_x = GAME_POSITIONS["p1_x"]
        p1_y = GAME_POSITIONS["p1_y"]
        p2_x = GAME_POSITIONS["p2_x"]
        p2_y = GAME_POSITIONS["p2_y"]

        dist_to_p1 = math.sqrt((self.x - p1_x) ** 2 + (self.y - p1_y) ** 2)
        dist_to_p2 = math.sqrt((self.x - p2_x) ** 2 + (self.y - p2_y) ** 2)
        if dist_to_p1 < dist_to_p2:
            self.target = (p1_x, p1_y)
        else:
            self.target = (p2_x, p2_y)

    def move(self):
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
                self.released = True
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


ghosts_list = [
    Ghost(365, 275, 0, 0, False, False, False),
    Ghost(315, 340, 1, 2, False, True, False),
    Ghost(365, 340, 2, 2, False, True, False),
    Ghost(415, 340, 3, 2, False, True, False)
]

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

def check_ghost_collisions(which_player):
    global GAME_POSITIONS
    px = GAME_POSITIONS[which_player + "_x"]
    py = GAME_POSITIONS[which_player + "_y"]

    for ghost in ghosts_list:
        distance = math.sqrt(((px + 20) - (ghost.x + 20)) ** 2 + ((py + 20) - (ghost.y + 20)) ** 2)
        if distance < 20:
            if GAME_POSITIONS.get("powerup"):
                if not ghost.is_dead:
                    ghost.is_dead = True
                    GAME_POSITIONS[which_player + "_score"] += 200
            else:
                GAME_POSITIONS[which_player + "_lives"] -= 1
                reset_positions_server(which_player)
                check_game_status()
                break

def reset_positions_server(player_prefix=None):
    global GAME_POSITIONS, ghosts_list, POWERUP_COUNTER, GHOST_RELEASE_COUNTER
    GHOST_RELEASE_COUNTER = 0
    POWERUP_COUNTER = 0
    ghosts_list[0].x, ghosts_list[0].y = 365, 275
    ghosts_list[1].x, ghosts_list[1].y = 315, 340
    ghosts_list[2].x, ghosts_list[2].y = 365, 340
    ghosts_list[3].x, ghosts_list[3].y = 415, 340
    GAME_POSITIONS["powerup"] = False

    for i, ghost in enumerate(ghosts_list):
        ghost.is_dead = False
        ghost.direction = 0 if i == 0 else 2
        ghost.in_box = True if i > 0 else False
        ghost.released = True if i == 0 else False
    for ghost in ghosts_list:
        ghost.center_x = ghost.x + 22
        ghost.center_y = ghost.y + 22
    if player_prefix == "p1" or player_prefix is None:
        GAME_POSITIONS["p1_x"], GAME_POSITIONS["p1_y"] = 414, 431
    if player_prefix == "p2" or player_prefix is None:
        GAME_POSITIONS["p2_x"], GAME_POSITIONS["p2_y"] = 334, 431


def check_points(x, y, which_player):
    global TOTAL_POINTS_ON_BOARD, POWERUP_COUNTER
    num1 = HEIGHT // 33
    num2 = WIDTH // 29
    if board[y // num1][x // num2] == 2:
        board[y // num1][x // num2] = 0
        GAME_POSITIONS[which_player + "_score"] += 10
        TOTAL_POINTS_ON_BOARD -= 1
    if board[y // num1][x // num2] == 3:
        board[y // num1][x // num2] = 0
        GAME_POSITIONS[which_player + "_score"] += 50
        TOTAL_POINTS_ON_BOARD -= 1
        GAME_POSITIONS["powerup"] = True
        POWERUP_COUNTER = 0
    check_game_status()


def check_game_status():
    global GAME_POSITIONS
    p1_lives = GAME_POSITIONS["p1_lives"]
    p2_lives = GAME_POSITIONS["p2_lives"]
    p1_score = GAME_POSITIONS["p1_score"]
    p2_score = GAME_POSITIONS["p2_score"]
    if p1_lives <= 0 and p2_lives > 0:
        GAME_POSITIONS["game_over"] = True
        GAME_POSITIONS["winner"] = "Player 2"
        GAME_POSITIONS["reason"] = "Player 1 lost all lives!"
        return
    if p2_lives <= 0 and p1_lives > 0:
        GAME_POSITIONS["game_over"] = True
        GAME_POSITIONS["winner"] = "Player 1"
        GAME_POSITIONS["reason"] = "Player 2 lost all lives!"
        return
    if TOTAL_POINTS_ON_BOARD <= 0:
        GAME_POSITIONS["game_over"] = True
        if p1_score > p2_score:
            GAME_POSITIONS["winner"] = "Player 1"
            GAME_POSITIONS["reason"] = "All points cleared! P1 has more points."
        elif p2_score > p1_score:
            GAME_POSITIONS["winner"] = "Player 2"
            GAME_POSITIONS["reason"] = "All points cleared! P2 has more points."
        else:
            GAME_POSITIONS["winner"] = "Tie"
            GAME_POSITIONS["reason"] = "All points cleared! It's a tie!"
        return


def load_or_create_keys():
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(PUBLIC_KEY_FILE, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        print("RSA keys loaded")
    else:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        with open(PRIVATE_KEY_FILE, "wb") as f:
            f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption()))
        with open(PUBLIC_KEY_FILE, "wb") as f:
            f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
        print("RSA keys created")
    return private_key, public_key

private_key, public_key = load_or_create_keys()

def build_pickle():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'rb') as f:
        return pickle.load(f)

def save_pickle(users):
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users, f)

def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    return hashlib.sha256(salt + PEPPER + password_bytes).digest()


def signup(request, clt_sock):
    users = build_pickle()
    email = request["username"]
    password = request["password"]
    if email in users:
        send_encrypted(clt_sock,{"status":"error", "message":"User already exists"})
        return
    salt = secrets.token_bytes(32)
    hashed_password = hash_password(password, salt)
    users[email] = {"password": hashed_password, "salt": salt}
    save_pickle(users)
    send_encrypted(clt_sock, {"status": "signup_ok"})



def login(request, clt_sock):
    users = build_pickle()
    email = request["username"]
    password = request["password"]
    if email not in users:
        send_encrypted(clt_sock, {"status": "error"})
        return
    user = users[email]
    hashed = hash_password(password, user["salt"])
    if hashed == user["password"]:
        async_msgs.sock_by_user[email] = clt_sock
        user_by_sock[clt_sock] = email
        send_encrypted(clt_sock, {"status": "ok"})
    else:
        send_encrypted(clt_sock, {"status": "error"})


def send_msg(request):
    to_user = request["to"]
    from_user = request["from"]
    msg = request["msg"]
    message_data = {"from": from_user,"msg": msg, "iv": request.get("iv")}
    async_msgs.put_msg_by_user(message_data, to_user)

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    plaintext = pickle.dumps(data)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext, cipher.iv

def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pickle.loads(plaintext)

def send_encrypted(sock, data):
    if sock not in keys_by_user:
        return
    aes_key = keys_by_user[sock]
    ciphertext, iv = encrypt(data, aes_key)
    packet = {"encrypted": ciphertext, "iv": iv}
    send_packet(sock, packet)

def handle_request(request, clt_sock):
    global GHOST_RELEASE_COUNTER, POWERUP_COUNTER
    if GAME_POSITIONS["game_over"]:
        return
    todo = request["action"]
    if todo == "signup":
        signup(request, clt_sock)
        return
    elif todo == "login":
        login(request, clt_sock)
        return
    elif todo == "send_msg":
        send_msg(request)
        return
    elif todo == "send_key":
        encrypted_key = request["key"]
        aes_key = private_key.decrypt(encrypted_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
        keys_by_user[clt_sock] = aes_key
        print("Encrypted AES key received and decrypted")
        return
    elif todo == "get_public_key":
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        send_packet(clt_sock, {"status": "public_key", "key": pem})
        return
    elif todo == "join_game":
        with waiting_lock:
            waiting_players.append(clt_sock)
            if len(waiting_players) < 2:
                send_encrypted(clt_sock, {"status": "waiting"})
            else:
                PLAYERS[waiting_players[0]] = 1
                PLAYERS[waiting_players[1]] = 2
                send_encrypted(waiting_players[0], {"status": "game_start", "player_id": 1})
                send_encrypted(waiting_players[1], {"status": "game_start", "player_id": 2})
                waiting_players.clear()
        return
    elif todo == "move":
        with game_lock:
            direction = request["direction"]
            if clt_sock not in PLAYERS:
                return
            player_num = PLAYERS[clt_sock]
            if player_num == 1:
                which_player = "p1"
            else:
                which_player = "p2"
            curr_x = GAME_POSITIONS[which_player + "_x"]
            curr_y = GAME_POSITIONS[which_player + "_y"]
            new_x, new_y = curr_x, curr_y
            if direction == "right":
                GAME_POSITIONS[which_player + "_dir"] = 0
                new_x += PLAYER_VEL
            elif direction == "left":
                GAME_POSITIONS[which_player + "_dir"] = 1
                new_x -= PLAYER_VEL
            elif direction == "up":
                GAME_POSITIONS[which_player + "_dir"] = 2
                new_y -= PLAYER_VEL
            elif direction == "down":
                GAME_POSITIONS[which_player + "_dir"] = 3
                new_y += PLAYER_VEL

            center_x = new_x + 22
            center_y = new_y + 22
            num1 = HEIGHT // 33
            num2 = WIDTH // 29
            row = center_y // num1
            col = center_x // num2

            WALLS = [1, 4, 5, 6, 7, 8, 9]
            if 0 <= row < len(board) and 0 <= col < len(board[0]):
                if board[row][col] not in WALLS:
                    GAME_POSITIONS[which_player + "_x"] = new_x
                    GAME_POSITIONS[which_player + "_y"] = new_y
            center_x = GAME_POSITIONS[which_player + "_x"] + 22
            center_y = GAME_POSITIONS[which_player + "_y"] + 22
            check_points(center_x, center_y, which_player)
    elif todo == "update":
        return


def game_loop():
    global GHOST_RELEASE_COUNTER, POWERUP_COUNTER

    while True:
        time.sleep(1 / 60)
        with game_lock:
            if len(PLAYERS) < 2:
                continue
            if GAME_POSITIONS["game_over"]:
                continue

            GHOST_RELEASE_COUNTER += 1
            if GHOST_RELEASE_COUNTER >= 300:
                ghosts_list[1].released = True
            if GHOST_RELEASE_COUNTER >= 600:
                ghosts_list[2].released = True
            if GHOST_RELEASE_COUNTER >= 900:
                ghosts_list[3].released = True

            if GAME_POSITIONS.get("powerup", False):
                POWERUP_COUNTER += 1
                if POWERUP_COUNTER >= 600:
                    GAME_POSITIONS["powerup"] = False
                    POWERUP_COUNTER = 0

            for ghost in ghosts_list:
                ghost.update_target_and_move()
                ghost.move()

            check_ghost_collisions("p1")
            check_ghost_collisions("p2")

            GAME_POSITIONS["ghosts"] = {
                "red": {"x": ghosts_list[0].x, "y": ghosts_list[0].y, "dead": ghosts_list[0].is_dead},
                "teal": {"x": ghosts_list[1].x, "y": ghosts_list[1].y, "dead": ghosts_list[1].is_dead},
                "pink": {"x": ghosts_list[2].x, "y": ghosts_list[2].y, "dead": ghosts_list[2].is_dead},
                "orange": {"x": ghosts_list[3].x, "y": ghosts_list[3].y, "dead": ghosts_list[3].is_dead}
            }
            for sock in PLAYERS:
                async_msgs.put_msg_in_async_msgs({"status": "position", "position": GAME_POSITIONS, "board": board}, sock)


def handle_client(clt_sock):
    async_msgs.add_new_socket(clt_sock)
    while True:
        try:
            request = recv_packet(clt_sock)
            if request is None:
                break
            if request is not None:
                if "encrypted" in request:
                    if clt_sock not in keys_by_user:
                        continue
                    aes_key = keys_by_user[clt_sock]
                    request = decrypt(request["encrypted"], aes_key, request["iv"])
                handle_request(request, clt_sock)
        except socket.timeout:
            pass
        except Exception:
            print("SERVER ERROR:")
            traceback.print_exc()
            break
        msgs = async_msgs.get_async_messages_to_send(clt_sock)
        for msg in msgs:
            send_encrypted(clt_sock, msg)
    if clt_sock in PLAYERS:
        GAME_POSITIONS["game_over"] = True
        GAME_POSITIONS["winner"] = "Remaining Player"
        GAME_POSITIONS["reason"] = "Opponent disconnected"
    async_msgs.delete_socket(clt_sock)
    if clt_sock in PLAYERS:
        del PLAYERS[clt_sock]
    if clt_sock in keys_by_user:
        del keys_by_user[clt_sock]
    if clt_sock in user_by_sock:
        del user_by_sock[clt_sock]
    if clt_sock in waiting_players:
        waiting_players.remove(clt_sock)
    clt_sock.close()

def main():
    print("Server started")
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(("0.0.0.0", 65432))
    srv_sock.listen(10)
    threading.Thread(target=game_loop, daemon=True).start()
    while True:
        clt_sock, addr = srv_sock.accept()
        clt_sock.settimeout(0.01)
        print("CONNECTED:", addr)
        threading.Thread(target=handle_client, args=(clt_sock,), daemon=True).start()

if __name__ == '__main__':
    main()
