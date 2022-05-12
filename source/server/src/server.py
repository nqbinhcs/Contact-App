import os
import socket
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk


def client_program():

    print('CLIENT')

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


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
        self.root.geometry('450x150')
        self.root.title('Server')

        # Button
        self.root.turn_on_off_button = tk.Button(self._root, text="OPEN SERVER", bg="#5DADE2",
                                                 width=200, anchor=tk.CENTER,
                                                 font=("Consolas 20 bold"), command=self.open_close_server,
                                                 compound=tk.TOP)



    def run(self):
        self.root.mainloop()

    def turn_server(self):
        if self.root.turn_on_off_button["text"] = "OPEN SERVER":
            self.server =  socket.socket()

            self.server.bind(self.IP)
            self.server.listen(1)
            print("SERVER ADDRESS:", self.server.address)


    def accept_connect(self):
        while True:
            self.client, addr = self.server.accept()
            print("Connected by", addr)
            handle_client_thread = Thread(
                target=self.handle_client, daemon=True)
            handle_client_thread.start()





    

    


    


