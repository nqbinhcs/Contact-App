import re
import os
import socket
from tkinter import *
import tkinter as tk
from tkinter import ttk
from threading import Thread
import buffer
import PIL
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog
import shutil


avatar_path = "source/client/downloads/avatars"
thumbnail_path = "source/client/downloads/thumbnails"
default_img_path = "source/client/assets/default.png"

BUFFER_SIZE = 4096
SEPARATOR = "<,>"

class Client:
    def __init__(self):
        print('--> __init__')
        self.root = tk.Tk()
        self.load_gui()

    def load_gui(self):
        print('--> load gui')
        self.root.geometry('450x250')
        self.root.title('Danh bạ số')

        # Button
        # Connect
        self.root.connect_frame = tk.Frame(self.root)
        self.root.connect_frame.ip_label = tk.Label(
            self.root.connect_frame, text="IP").pack()
        self.root.connect_frame.ip_entry = tk.Entry(self.root.connect_frame)
        self.root.connect_frame.ip_entry.pack()

        self.root.connect_frame.port_label = tk.Label(
            self.root.connect_frame, text="Port").pack()
        self.root.connect_frame.port_entry = tk.Entry(self.root.connect_frame)
        self.root.connect_frame.port_entry.pack()

        self.root.connect_frame.connect_button = tk.Button(self.root.connect_frame, text="CONNECT TO SERVER", bg="#5DADE2",
                                                           font=("Consolas 20 bold"), command=self.connect)
        self.root.connect_frame.connect_button.pack(pady=20)

        self.root.connect_frame.pack()

    def run(self):
        print('--> run')
        self.root.mainloop()

    def connect(self):
        print('--> connect')
        self.ip = self.root.connect_frame.ip_entry.get()
        self.port = self.root.connect_frame.port_entry.get()
        self.root.connect_frame.forget()
        if (self.ip == "") | (self.port == ""):
            self.load_gui()
            tk.Label(self.root.connect_frame,
                     text="IP/Port không được bỏ trống!", fg='red').pack()
        else:
            # Need to check if the connection has been created or not
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(type(self.ip))
            print(type(self.port))
            self.client.connect((self.ip, int(self.port)))
            print('connect successfully!')
            self.show_all_staffs()

    def show_all_staffs(self):
        print('--> show_all_staffs')
        self.root.geometry('450x450')

        self.root.all_staffs_frame = tk.Frame(self.root)

        self.root.all_staffs_frame.title = tk.Label(
            self.root.all_staffs_frame, text="Danh sach nhan vien", font=("Consolas 20 bold")).pack(pady=10)

        self.all_staffs = ttk.Treeview(self.root.all_staffs_frame)
        self.all_staffs['columns'] = ("ID", "NAME")
        
        self.all_staffs.column("#0", anchor="w", width=30, stretch='NO')
        self.all_staffs.column("ID", anchor="center", width=120, stretch='NO')
        self.all_staffs.column("NAME", anchor="w", width=200, stretch='NO')

        self.all_staffs.heading("ID", text="Mã số", anchor="center")
        self.all_staffs.heading("NAME", text="Họ và tên", anchor="w")
        
        self.root.all_staffs_frame.img_temp = []
        self.client.sendall(bytes("GETALL 0", "utf8"))
        self.root.all_staffs_frame.all_staffs = self.receive_all_contact()
        

        for i in range(len(self.root.all_staffs_frame.all_staffs)):
            path = default_img_path
            if os.path.exists(os.path.join(thumbnail_path, "Image_", str(self.root.all_staffs_frame.all_staffs[i][0])+".png")):
                path = os.path.join(thumbnail_path, "Image_", str(self.root.all_staffs_frame.all_staffs[i][0])+".png")

            self.root.all_staffs_frame.img_temp.append(ImageTk.PhotoImage(
                Image.open(path).resize((20, 20), Image.ANTIALIAS)))
            self.all_staffs.insert('', tk.END, image=self.root.all_staffs_frame.img_temp[i], values=(
                self.root.all_staffs_frame.all_staffs[i][0], self.root.all_staffs_frame.all_staffs[i][1]))

        self.all_staffs.pack(pady=20)

        self.root.all_staffs_frame.download_all_ava = tk.Button(
            self.root.all_staffs_frame, text="Tải tất cả ảnh", command=self.change_to_download_all_btn)
        self.root.all_staffs_frame.download_all_ava.pack()

        # Back button
        self.root.all_staffs_frame.back_button = tk.Button(
            self.root.all_staffs_frame, text="Trở về", command=self.change_to_connect)
        self.root.all_staffs_frame.back_button.pack()

        self.root.all_staffs_frame.pack()
        self.all_staffs.bind("<Double-1>", self.show_detail_a_staff)

    def show_detail_a_staff(self, event):
        self.root.all_staffs_frame.forget()
        iid = int(self.all_staffs.focus()[1:])-1
        ID = self.root.all_staffs_frame.all_staffs[iid][0]
        # print(id)
        self.root.staff_detail_frame = tk.Frame(self.root)
        self.root.staff_detail_frame.title = tk.Label(
            self.root.staff_detail_frame, text="Thong tin chi tiet", font=("Consolas 20 bold")).pack(pady=10)

        self.client.sendall(bytes("GET 0" + " " + str(ID), "utf8"))
        infor = self.recieve_contact()

        self.root.staff_detail_frame.id = tk.StringVar()
        self.root.staff_detail_frame.id.set(infor[0])
        self.root.staff_detail_frame.name = tk.StringVar()
        self.root.staff_detail_frame.name.set(infor[1])
        self.root.staff_detail_frame.phone = tk.StringVar()
        self.root.staff_detail_frame.phone.set(infor[2])
        self.root.staff_detail_frame.email = tk.StringVar()
        self.root.staff_detail_frame.email.set(infor[3])

        # Information
        self.root.staff_detail_frame.infor = tk.Frame(
            self.root.staff_detail_frame)
        self.root.staff_detail_frame.infor.id = tk.Label(
            self.root.staff_detail_frame.infor, text="Mã số")
        self.root.staff_detail_frame.infor.id.grid(row=0, column=0)
        self.root.staff_detail_frame.infor.name = tk.Label(
            self.root.staff_detail_frame.infor, text="Họ và tên")
        self.root.staff_detail_frame.infor.name.grid(row=1, column=0)
        self.root.staff_detail_frame.infor.phone = tk.Label(
            self.root.staff_detail_frame.infor, text="Số điện thoại")
        self.root.staff_detail_frame.infor.phone.grid(row=2, column=0)
        self.root.staff_detail_frame.infor.email = tk.Label(
            self.root.staff_detail_frame.infor, text="Email")
        self.root.staff_detail_frame.infor.email.grid(row=3, column=0)
        self.root.staff_detail_frame.infor.id = tk.Entry(
            self.root.staff_detail_frame.infor, textvariable=self.root.staff_detail_frame.id, state='disabled')
        self.root.staff_detail_frame.infor.id.grid(row=0, column=1)
        self.root.staff_detail_frame.infor.name = tk.Entry(
            self.root.staff_detail_frame.infor, textvariable=self.root.staff_detail_frame.name, state='disabled')
        self.root.staff_detail_frame.infor.name.grid(row=1, column=1)
        self.root.staff_detail_frame.infor.phone = tk.Entry(
            self.root.staff_detail_frame.infor, textvariable=self.root.staff_detail_frame.phone, state='disabled')
        self.root.staff_detail_frame.infor.phone.grid(row=2, column=1)
        self.root.staff_detail_frame.infor.email = tk.Entry(
            self.root.staff_detail_frame.infor, textvariable=self.root.staff_detail_frame.email, state='disabled')
        self.root.staff_detail_frame.infor.email.grid(row=3, column=1)
        self.root.staff_detail_frame.infor.pack()

        # Avatar
        path = default_img_path
        if os.path.exists(os.path.join(avatar_path, "Image_", str(id)+".png")):
            path = os.path.join(thumbnail_path, "Image_", str(id)+".png")


        self.root.staff_detail_frame.avt_img = ImageTk.PhotoImage(
            Image.open(path).resize((100, 100), Image.ANTIALIAS))
        self.root.staff_detail_frame.avatar = tk.Label(self.root.staff_detail_frame, image=self.root.staff_detail_frame.avt_img)
        self.root.staff_detail_frame.avatar.pack(pady=10)

        # Download button
        self.root.staff_detail_frame.download_btn = tk.Button(
            self.root.staff_detail_frame, text="Tải ảnh đại diện", command=self.change_to_download_big_avatar)
        self.root.staff_detail_frame.download_btn.pack()

        # Back button
        self.root.staff_detail_frame.back_button = tk.Button(
            self.root.staff_detail_frame, text="Trở về", command=self.change_to_show_all_staffs)
        self.root.staff_detail_frame.back_button.pack()

        self.root.staff_detail_frame.pack()


    def change_to_show_all_staffs(self):
        self.root.staff_detail_frame.forget()
        self.show_all_staffs()

    def change_to_connect(self):
        self.root.all_staffs_frame.forget()
        self.load_gui()

    def change_to_download_big_avatar(self):
        id = str(self.root.staff_detail_frame.id.get())
        # location = os.path.join(avatar_path, "Image_"+id+".png")
        # print(location)
        # print(self.root.staff_detail_frame.avatar)
        # print(type(self.root.staff_detail_frame.avatar))
        self.client.sendall(bytes("GET 1 " + id, "utf8"))
        self.root.staff_detail_frame.avt_img = self.recieve_contact_avatar()
        tk.Label(self.root.staff_detail_frame, image=self.root.staff_detail_frame.avt_img).pack()
        self.root.staff_detail_frame.avatar.config(image=self.root.staff_detail_frame.avt_img)
        self.root.staff_detail_frame.avt_img.save(avatar_path+"/Image_"+id+".png")

    def change_to_download_all_btn(self):
        location = filedialog.askdirectory()
        des = location + '/all_small_ava/'
        if not os.path.exists(des):
            os.mkdir(des)
        for i in range(self.root.size_staffs):
            shutil.copy(staffs[i][5], des)

    def receive_all_contact(self):  # Feature 1
        print("recieve_all_contact #1")
        data = self.client.recv(BUFFER_SIZE).decode("utf8").split(SEPARATOR)
        print("recieve_all_contact #2")
        print([(data[i], data[i+1]) for i in range(0, len(data), 2)])
        return [(data[i], data[i+1]) for i in range(0, len(data), 2)]

    def receive_all_contact_thumbnail(self):  # Feature 4

        connbuf = buffer.Buffer(self.client)

        while True:
            file_name = connbuf.get_utf8()
            if not file_name:
                break
            file_name = os.path.join(
                'source/client/downloads/thumbnails', os.path.basename(file_name))
            print('file name: ', file_name)

            file_size = int(connbuf.get_utf8())
            print('file size: ', file_size)

            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = connbuf.get_bytes(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
                if remaining:
                    print('File incomplete.  Missing', remaining, 'bytes.')
                else:
                    print('File received successfully.')


    def recieve_contact(self):  # Feature 2
        data = self.client.recv(BUFFER_SIZE).decode("utf8").split(SEPARATOR)
        print(data)
        return data


    def recieve_contact_avatar(self):  # Feature 5
        connbuf = buffer.Buffer(self.client)

        while True:
            file_name = connbuf.get_utf8()
            if not file_name:
                break
            file_name = os.path.join(
                'source/client/downloads/avatars', os.path.basename(file_name))
            print('file name: ', file_name)

            file_size = int(connbuf.get_utf8())
            print('file size: ', file_size)

            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = connbuf.get_bytes(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
                if remaining:
                    print('File incomplete.  Missing', remaining, 'bytes.')
                else:
                    print('File received successfully.')

        return 0


    # DEMO PROGRAM
    # def client_program():
    #     HOST = '127.0.1.1'  # The server's hostname or IP address
    #     PORT = int(input("ENter Port:"))        # The port used by the server
    #     # Create a TCP/IP socket
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # s = socket.socket()
    #     server_address = (HOST, PORT)
    #     print('connecting to %s port ' + str(server_address))
    #     s.connect(server_address)

    #     try:
    #         while True:
    #             cmd = input('Client: ')
    #             s.sendall(bytes(cmd, "utf8"))

    #             if cmd == 'GETALL 0':  # Get (id, name) of all contacts
    #                 receive_all_contact(s)
    #             elif cmd == 'GETALL 1':  # Get thumbnails of all contacts
    #                 receive_all_contact_thumbnail(s)
    #             elif cmd == 'QUIT':
    #                 break
    #             else:
    #                 # Get (id, name, phone, email) of contact,  Ex: GET 0 3 -> get id = 3
    #                 if cmd[:5] == 'GET 0':
    #                     recieve_contact(s)
    #                 elif cmd[:5] == 'GET 1':  # Get avatar of contact, Ex: GET 1 3 -> get id = 3
    #                     recieve_contact_avatar(s)

    #             print("Completed")

    #     finally:
    #         print('closing socket')
    #         s.close()


print('Client')
client = Client()
client.run()