import os
import socket
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk


def server_program():

    print('SERVER')

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


class Server:
    def __init__(self):
        # IP address
        self.IP = (socket.gethostbyname(socket.gethostname()), 54321)

        # Intialize UI
        self.root = tk.Tk()
        self.root.geometry('450x250')
        self.root.title('Server')

        # Button
        self.root.turn_on_off_button = tk.Button(self.root, text="OPEN SERVER", bg="#5DADE2",
                                                 width=200, anchor=tk.CENTER,
                                                 font=("Consolas 20 bold"), command=self.turn_on_off,
                                                 compound=tk.TOP)

        self.root.turn_on_off_button.place(
            relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.root.lbl_server_address = tk.Label(self.root, text="IP: " + str(self.IP[0]), width=25,

                                                font=("Consolas 20 bold"), fg="#ff0000")
        self.root.lbl_server_address.place(
            relx=0.5, rely=0.10, anchor=tk.CENTER)

    def run(self):
        self.root.mainloop()

    def turn_on_off(self):
        if self.root.turn_on_off_button["text"] == "OPEN SERVER":
            self.server = socket.socket()

            self.server.bind(self.IP)
            self.server.listen(1)
            print("SERVER ADDRESS:", self.IP)

            self.root.turn_on_off_button.configure(text="OPENING")

            Thread(target=self.accept_connect, daemon=True).start()

    def accept_connect(self):
        while True:
            self.client, addr = self.server.accept()
            print("Connected by", addr)
            handle_client_thread = Thread(
                target=self.handle_client, daemon=True)
            handle_client_thread.start()

    def handle_client(self):
        while True:
            cmd = self.client.recv(16).decode('utf8')
            print('REQUEST:', cmd)
            if cmd == 'close':
                self.client.close()


print("SERVER")
app = Server()
app.run()
