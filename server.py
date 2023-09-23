import socket
import threading
from typing import List

HOST: str = "127.0.0.1"
PORT: int = 12345

connected_clients: List[socket.socket] = []
lock: threading.Lock = threading.Lock()

def broadcast_message(message: bytes, sender: socket.socket) -> None:
    with lock:
        for client in connected_clients:
            if client != sender:
                try:
                    client.sendall(message)
                except Exception as e:
                    print(f"Error sending message: {e}")
                    # Delete client if error
                    connected_clients.remove(client)

def handle_client(connection: socket.socket, address: str) -> None:
    with connection:
        print(f"Client connected: {address}")
        with lock:
            connected_clients.append(connection)

        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break

                print(f"Received from {address}: {data.decode()}")
                broadcast_message(data, connection)
            except Exception as e:
                print(f"Error receiving data from client {address}: {e}")
                break

        with lock:
            connected_clients.remove(connection)
            print(f"Client {address} disconnected")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
