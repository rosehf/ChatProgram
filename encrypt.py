import base64
import os

import server
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

publicKey = "securepassword1"


def load_key(filename="private.txt"):
    global private_key
    with open(filename, "r") as file:
        key = base64.b64decode(file.read().strip())
    if len(key) not in [16, 24, 32]:  # Ensure key length is valid for AES
        raise ValueError("Invalid AES key length.")
    private_key = key
    

def xorEncript(message):
    return ''.join(f'{ord(c) ^ ord(publicKey[i % len(publicKey)]):02x}' for i, c in enumerate(message))

def xorDecrypt(encryptedMesg):
    cipher_bytes = bytes.fromhex(encryptedMesg)
    decrypted_bytes = bytes([cipher_bytes[i] ^ ord(publicKey[i % len(publicKey)]) for i in range(len(cipher_bytes))])
    return decrypted_bytes.decode(errors='ignore')

def encryptMesg(message):
    key = load_key()
    cipher = AES.new(key, AES.MODE_CBC)
    cypText = cipher.encrypt(pad(message.encode(),AES.block_size))
    sendMESG = base64.b64encode(cipher.iv + cypText).decode()
    with open("Mesg.txt", "w") as file:
        file.write(sendMESG)
    return sendMESG

def decryptMesg(encryptedMesg):
    key = load_key()
    encryptedData = base64.b64decode(encryptedMesg)
    iv = encryptedData[:16]  # Extract IV
    cyptext = encryptedData[16:]  # Extract only the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(cyptext), AES.block_size).decode()



