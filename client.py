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


clt_sock = socket.socket()
clt_sock.connect(("127.0.0.1", 8080))
curr_user = None
email_var = None
password_var = None
status_label = None
to_var = None
send_msg_var = None
text_box = None
sign_up_email_var = None
sign_up_password_var = None
aes_key = None
server_public_key = None


def listen_server():
    global curr_user
    global server_public_key
    while True:
        try:
            data = clt_sock.recv(4096)
            if not data:
                break
            msg = pickle.loads(data)
            print("SERVER SENT:", msg)
            if "from" in msg:
                decrypted = decrypt(msg["msg"], aes_key, msg["iv"])
                text_box.after(0, lambda m=msg, d=decrypted: text_box.insert(tk.END, f'{m["from"]}: {d}\n'))
            status = msg.get("status")
            if status == "ok":
                curr_user = msg.get("username", curr_user)
                login_root.after(0, login_success)
            elif status == "error":
                error_msg = msg.get("message", "Operation failed")
                print(f"Error: {error_msg}")
            if status == "public_key":
                server_public_key = serialization.load_pem_public_key(msg["key"])
                print("Public key received")
        except Exception as e:
            print("Listen error:", e)
            break

def request_public_key():
    data = {"action": "get_public_key"}
    clt_sock.send(pickle.dumps(data))

def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    cipher_text = cipher.encrypt(pad(msg.encode(), AES.block_size))
    return cipher_text, iv

def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plain_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plain_text.decode()

def login_success():
    global aes_key
    aes_key = secrets.token_bytes(32)
    encrypted_key = server_public_key.encrypt(aes_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    data = {"action": "send_key","key": encrypted_key}
    clt_sock.send(pickle.dumps(data))
    login_root.withdraw()
    start_game_screen()


def try_login():
    data = {"action": "login", "username": email_var.get(), "password": password_var.get()}
    clt_sock.send(pickle.dumps(data))

def start_game():
    pass


def start_game_screen():
    global to_var, send_msg_var, text_box
    root = tk.Tk()
    root.geometry('300x200')
    root.title('wait to start')

    tk.Button(root, text="press to start", command=start_game).pack(pady=10)
    threading.Thread(target=listen_server, daemon=True).start()
    root.mainloop()


def signup():
    print(sign_up_email_var)
    data={"action":"signup","username":sign_up_email_var.get(), "password":sign_up_password_var.get()}
    clt_sock.send(pickle.dumps(data))


def open_signup():
    global sign_up_email_var, sign_up_password_var
    signup_root = tk.Toplevel()
    signup_root.geometry('300x250')
    signup_root.title('Sign Up')
    ttk.Label(signup_root,text='Username').pack()

    sign_up_email_var = tk.StringVar()
    ttk.Entry(signup_root, textvariable=sign_up_email_var).pack()

    ttk.Label(signup_root,text='Password').pack()

    sign_up_password_var = tk.StringVar()
    ttk.Entry(signup_root, show="*", textvariable=sign_up_password_var).pack()

    tk.Button(signup_root, text="Register", command=signup).pack()



def opening_screen():
    global email_var, password_var, status_label, login_root
    login_root = tk.Tk()
    login_root.geometry('300x250')
    login_root.title('start game')

    ttk.Label(login_root, text='Username:').pack(pady=2)
    email_var = tk.StringVar()
    ttk.Entry(login_root, textvariable=email_var).pack(pady=5)

    ttk.Label(login_root, text='Password:').pack(pady=2)

    password_var = tk.StringVar()
    ttk.Entry(login_root, show='*', textvariable=password_var).pack(pady=5)

    status_label = ttk.Label(login_root, text='')
    status_label.pack()

    tk.Button(login_root, text="Login", command=try_login).pack(pady=10)

    tk.Button(login_root, text="Sign Up", command=open_signup).pack(pady=5)

    threading.Thread(target=listen_server,daemon=True).start()
    request_public_key()
    login_root.mainloop()

if __name__ == "__main__":
    opening_screen()