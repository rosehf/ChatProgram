import base64
import socket
import threading

import encrypt
import server


def receive_key(client_socket, filename='private.txt'):
    """Receives the private key file from the server and saves it."""
    with open(filename, "wb") as file:
        key_data = client_socket.recv(1024)  # Receiving key file content
        file.write(key_data)
    print("Key received and saved.")


def listen_for_messages(client_socket):
    """Listens for incoming messages, decrypts them, and displays them."""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decrypted_message = encrypt.decryptMesg(message)
            read_message = encrypt.xorDecrypt(decrypted_message)
            print(f"Received: {read_message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def start_client(server_host='127.0.0.1', server_port=12345):
    """Connects to the server, receives the key, and starts message exchange."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    receive_key(client_socket)  # Download and save the key
    encrypt.load_key()  # Ensure encryption module loads the key

    listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listen_thread.start()
    
    messCount = 0
    while True:
        print("Whats the message you want to send?")
        message = input()
        messCount +=1
        if message.lower() == "exit":
            break  # Allow user to exit cleanly
        if(messCount == 4):
            server.keyGen()
        new_message = encrypt.xorEncript(message)
        encrypted_message = encrypt.encryptMesg(new_message)
        client_socket.sendall(encrypted_message.encode())  # Ensure proper encoding
        print(f"Sent: {encrypted_message}")

    client_socket.close()


if __name__ == "__main__":
    start_client()