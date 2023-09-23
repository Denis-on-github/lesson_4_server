import socket
import threading

HOST: str = "127.0.0.1"
PORT: int = 12345

def receive_messages(sock: socket.socket) -> None:
    while True:
        try:
            data: bytes = sock.recv(1024)
            if not data:
                print("Server disconnected.")
                break
            print(data.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))

            receive_thread = threading.Thread(target=receive_messages, args=(s,))
            receive_thread.daemon = True
            receive_thread.start()

            username: str = input("Enter your name: ")
            s.sendall(username.encode())

            while True:
                message: str = input()
                if message.lower() == "/exit":
                    s.sendall(message.encode())
                    break
                s.sendall(f"{username}: {message}".encode())

        except Exception as e:
            print(f"Error connecting to the server: {e}")

if __name__ == "__main__":
    main()
