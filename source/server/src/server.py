from http import client
import os
import socket
import tkinter as tk
import buffer

from database import *
from threading import Thread
from PIL import Image, ImageTk
import random


BUFFER_SIZE = 4096
SEPARATOR = "<,>"

# We use random port
PORT = random.randrange(60000, 62000)


class Server:

    db = ContactsDataBase()

    def __init__(self):
        # IP address
        # self.IP = (socket.gethostbyname(socket.gethostname()), PORT)
        self.IP = ('127.0.1.1', PORT)

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

        self.root.lbl_server_address = tk.Label(self.root, text="Address: " + str(self.IP[0]) + ' - ' + str(PORT), width=25,

                                                font=("Consolas 20 bold"), fg="#ff0000")
        self.root.lbl_server_address.place(
            relx=0.5, rely=0.10, anchor=tk.CENTER)

    def run(self):
        self.root.mainloop()

    def turn_on_off(self):
        if self.root.turn_on_off_button["text"] == "OPEN SERVER":
            # config for TCP option
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.server = socket.socket()
            self.server.bind(self.IP)
            self.server.listen(5)
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
            try:
                cmd = self.client.recv(64).decode('utf8')
            except:
                break
            if cmd == 'GETALL 0':
                self.send_all_contacts()
            elif cmd == 'GETALL 1':
                self.send_all_contacts_thumbnail()
            elif cmd == 'QUIT':
                self.client.close()
                break
            else:
                if cmd[:5] == 'GET 0':  # Ex: GET 0 3 -> get id = 3
                    self.send_contact(contact_id=int(cmd[5:]))
                elif cmd[:5] == 'GET 1':  # GET 1 3 -> get_id = 3
                    self.send_contact_avatar(contact_id=int(cmd[5:]))

    def send_all_contacts(self):
        contacts = self.db.get_all_contacts()

        data = SEPARATOR.join(
            [str(contact[0]) + SEPARATOR + str(contact[1]) for contact in contacts])
        self.client.sendall(bytes(str(data), "utf8"))

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

    def send_contact(self, contact_id):
        contact = self.db.get_contact(contact_id)
        data = SEPARATOR.join(
            [str(inf) for inf in contact])
        self.client.sendall(bytes(str(data), "utf8"))

    def send_contact_avatar(self, contact_id):
        sbuf = buffer.Buffer(self.client)
        file_name = self.db.get_contact_avatar(contact_id)

        print(file_name)
        sbuf.put_utf8(file_name)

        file_size = os.path.getsize(file_name)
        sbuf.put_utf8(str(file_size))

        with open(file_name, 'rb') as f:
            sbuf.put_bytes(f.read())
        print('File Sent')


print("SERVER")
app = Server()
app.run()
app.server.close()
