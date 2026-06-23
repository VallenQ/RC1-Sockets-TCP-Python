import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

window = tk.Tk()
window.title("Chat TCP")

chat_area = scrolledtext.ScrolledText(
    window,
    width=60,
    height=20
)

chat_area.pack(padx=10, pady=10)

name_frame = tk.Frame(window)
name_frame.pack()

tk.Label(name_frame, text="Nome:").pack(side=tk.LEFT)

name_entry = tk.Entry(name_frame)
name_entry.pack(side=tk.LEFT)

message_entry = tk.Entry(window, width=50)
message_entry.pack(pady=5)

def send_message():
    name = name_entry.get()

    message = message_entry.get()

    if name and message:
        full_message = f"{name}: {message}"

        client.send(full_message.encode())

        chat_area.insert(tk.END, f"Você: {message}\n")

        message_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            chat_area.insert(
                tk.END,
                message + "\n"
            )

        except:
            break

send_button = tk.Button(
    window,
    text="Enviar",
    command=send_message
)

send_button.pack()

thread = threading.Thread(
    target=receive_messages,
    daemon=True
)

thread.start()

window.mainloop()