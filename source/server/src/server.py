from http import client
import os
import socket
import tkinter as tk
import buffer

from database import *
from threading import Thread
from PIL import Image, ImageTk
import random


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


BUFFER_SIZE = 1024
SEPARATOR = "<SEPERATOR>"

PORT = random.randrange(60000, 62000)


class Server:

    db = ContactsDataBase()

    def __init__(self):
        # IP address
        self.IP = (socket.gethostbyname(socket.gethostname()), PORT)

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
            # config for TCP option
            # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = socket.socket()
            self.server.bind(self.IP)
            self.server.listen(1)
            print("SERVER ADDRESS:", self.IP)

            self.root.turn_on_off_button.configure(text="OPENING")

            # Thread(target=self.accept_connect, daemon=True).start()
            self.accept_connect()

    def accept_connect(self):
        while True:
            self.client, addr = self.server.accept()
            print("Connected by", addr)
            handle_client_thread = Thread(
                target=self.handle_client, daemon=True)
            handle_client_thread.start()

    def handle_client(self):
        while True:
            try:
                cmd = self.client.recv(64).decode('utf8')
            except:
                break
            if cmd == 'GETALL 0':
                self.send_all_contacts()
            elif cmd == 'GETALL 1':
                self.send_all_contacts_thumbnail()
            elif cmd == 'GET':
                self.shutdown()
            elif cmd == 'QUIT':
                self.client.close()
                break

        # cmd = self.client.recv(64).decode('utf8')
        # if cmd == 'GETALL 1':
        #     self.send_all_contacts_thumbnail()

    def send_file(self, file_name):
        file_size = os.path.getsize(file_name)

        self.client.sendall(
            f"{file_name}{SEPARATOR}{file_size}".encode())

        with open(file_name, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                self.client.sendall(bytes_read)

    def send_all_contacts(self):
        result = self.db.get_all_contacts()
        print(result)
        number_of_contacts = len(result)
        self.client.sendall(bytes(str(number_of_contacts), "utf8"))

        for i in range(number_of_contacts):
            print(f'Sending contact {i + 1}:')
            data = SEPARATOR.join([str(x) for x in result[i]])
            self.client.sendall(bytes(data, "utf8"))

    def send_all_contacts_thumbnail(self):
        sbuf = buffer.Buffer(self.client)
        files_to_send = self.db.get_all_contacts_thumbnail()

        for file_name in files_to_send:
            print(file_name)
            sbuf.put_utf8(file_name)

            file_size = os.path.getsize(file_name)
            sbuf.put_utf8(str(file_size))

            with open(file_name, 'rb') as f:
                sbuf.put_bytes(f.read())
            print('File Sent')

        
        # number_of_contacts = len(result)
        # print('Sending number of contacts')
        # self.client.sendall(bytes(str(number_of_contacts), "utf8"))
        # self.client.sendall(bytes(str(number_of_contacts), "utf8"))
        # for i in range(number_of_contacts):
        #     print(f'Sending thumbnail contact {i + 1}:')

        #     # print("Sending ID")
        #     # self.client.sendall(bytes(str(result[i][0]), "utf8"))

        #     print("Sending thumbnail")
        #     self.send_file(result[i][1])


print("SERVER")
app = Server()
app.run()
app.server.close()
