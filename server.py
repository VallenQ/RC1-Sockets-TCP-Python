import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            broadcast(message, client)

        except:
            break

    clients.remove(client)
    client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        client, addr = server.accept()

        print(f"Nova conexão: {addr}")

        clients.append(client)

        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )

        thread.start()

if __name__ == "__main__":
    start_server()