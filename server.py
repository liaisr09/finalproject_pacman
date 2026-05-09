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
import pygame

USERS_FILE = "users.pkl"
PEPPER_FILE = "pepper.bin"
keys_by_user = {}
PRIVATE_KEY_FILE = "private.pem"
PUBLIC_KEY_FILE = "public.pem"

async_msgs = AsyncMessages()

if os.path.exists(PEPPER_FILE):
    with open(PEPPER_FILE, "rb") as f:
        PEPPER = f.read()
else:
    PEPPER = secrets.token_bytes(32)
    with open(PEPPER_FILE, "wb") as f:
        f.write(PEPPER)

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
        clt_sock.send(pickle.dumps({"status": "error", "message": "User already exists"}))
        return
    salt = secrets.token_bytes(32)
    hashed_password = hash_password(password, salt)
    users[email] = {"password": hashed_password, "salt": salt}
    save_pickle(users)
    clt_sock.send(pickle.dumps({"status": "ok"}))



def login(request, clt_sock):
    users = build_pickle()
    email = request["username"]
    password = request["password"]
    if email not in users:
        clt_sock.send(pickle.dumps({"status": "error"}))
        return
    user = users[email]
    hashed = hash_password(password, user["salt"])

    if hashed == user["password"]:
        async_msgs.sock_by_user[email] = clt_sock
        clt_sock.send(pickle.dumps({"status": "ok"}))
    else:
        clt_sock.send(pickle.dumps({"status": "error"}))


def send_msg(request):
    print("SERVER GOT:", request["msg"])
    to_user = request["to"]
    from_user = request["from"]
    msg = request["msg"]
    print("SERVER GOT:", request["msg"])
    message_data = {"from": from_user,"msg": msg, "iv": request.get("iv")}
    async_msgs.put_msg_by_user(message_data, to_user)


def handle_request(request, clt_sock):
    todo = request["action"]
    if todo == "signup":
        signup(request, clt_sock)
    elif todo == "login":
        login(request, clt_sock)
    elif todo == "send_msg":
        print("FULL REQUEST:", request)
        print("SERVER GOT MSG:", request.get("msg"))
        print("SERVER GOT IV:", request.get("iv"))
        send_msg(request)
    elif todo == "send_key":
        encrypted_key = request["key"]
        aes_key = private_key.decrypt(encrypted_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
        keys_by_user[clt_sock] = aes_key
        print("Encrypted AES key received and decrypted")
    elif todo == "get_public_key":
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        clt_sock.send(pickle.dumps({"status": "public_key", "key": pem}))


def handle_client(clt_sock):
    async_msgs.add_new_socket(clt_sock)
    while True:
        try:
            data = clt_sock.recv(1024)
            if data == b'':
                break
            request = pickle.loads(data)
            handle_request(request, clt_sock)
            msgs = async_msgs.get_async_messages_to_send(clt_sock)
            for msg in msgs:
                clt_sock.send(pickle.dumps(msg))
        except Exception as e:
            print("SERVER ERROR:", e)
            break
    async_msgs.delete_socket(clt_sock)
    clt_sock.close()


def main():
    print("Server started")
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(('0.0.0.0', 8080))
    srv_sock.listen(10)
    while True:
        clt_sock, addr = srv_sock.accept()
        threading.Thread(target=handle_client, args=(clt_sock,)).start()

if __name__ == '__main__':
    main()
