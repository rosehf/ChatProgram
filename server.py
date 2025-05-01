import base64
import os
import socket
import threading


def keyGen():
    """Generates a private key and saves it to a file."""
    key = os.urandom(32)
    privKey = base64.b64encode(key).decode()
    filename = 'private.txt'
    with open(filename, "w") as file:
        file.write(privKey)
        
    send_file(12345,"private.txt")
    return filename


def send_file(client_socket, filename):
    """Sends the private key file to the connected client."""
    try:
        with open(filename, "rb") as file:
            data = file.read()
            client_socket.sendall(data)
    except FileNotFoundError:
        print("File not found.")


def handle_client(client_socket, client_address, filename):
    """Handles communication with a client."""
    print(f"New connection from {client_address}")
    try:
        send_file(client_socket, filename)  # Send encryption key first

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message from {client_address}: {message.decode()}")  # Log raw message
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {client_address} disconnected.")
    finally:
        client_socket.close()


def start_server(host='0.0.0.0', port=12345):
    """Starts the server and listens for connections."""
    filename = keyGen()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, filename))
        client_handler.start()


if __name__ == "__main__":
    start_server()
