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
                     text="Port must not be empty!", fg='red').pack()
        else:
            # Need to check if the connection has been created or not
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(type(self.ip))
            print(type(self.port))
            self.client.connect((self.ip, int(self.port)))
            print('connect successfully!')
            self.root.check_thumbnail_loaded = False
            self.show_all_staffs()

    def show_all_staffs(self):
        # Check if thumbnails have been loaded ?
        # - True: auto refresh frame with thumbnails
        # - False: display every single thumbnail as a default photo
        if self.root.check_thumbnail_loaded:
            self.root.all_staffs_frame.destroy()
            print('--> show_all_staffs_reload')
        else:
            print('--> show_all_staffs')

        self.root.geometry('450x450')

        self.root.all_staffs_frame = tk.Frame(self.root)

        self.root.all_staffs_frame.title = tk.Label(
            self.root.all_staffs_frame, text="Staff list", font=("Consolas 20 bold"))
        self.root.all_staffs_frame.title.grid(row=0, column=0, columnspan=3)

        self.all_staffs = ttk.Treeview(self.root.all_staffs_frame)
        self.all_staffs['columns'] = ("ID", "NAME")
        
        self.all_staffs.column("#0", anchor="w", width=30, stretch='NO')
        self.all_staffs.column("ID", anchor="center", width=120, stretch='NO')
        self.all_staffs.column("NAME", anchor="w", width=200, stretch='NO')

        self.all_staffs.heading("ID", text="Id", anchor="center")
        self.all_staffs.heading("NAME", text="Full name", anchor="w")
        
        self.root.all_staffs_frame.img_temp = []
        self.client.sendall(bytes("GETALL 0", "utf8"))
        self.root.all_staffs_frame.all_staffs = self.receive_all_contact()
        

        for i in range(len(self.root.all_staffs_frame.all_staffs)):
            temp_path = default_img_path

            # Check if thumbnails have been loaded ?
            # - True: temp_path = thumbnail_path
            # - False: temp_path = default_img_path
            if self.root.check_thumbnail_loaded:
                temp_path = thumbnail_path
                
            path = os.getcwd()+ "/" + temp_path
            if os.path.exists(path+"/Image_"+str(self.root.all_staffs_frame.all_staffs[i][0])+".png"):
                path = path+"/Image_"+str(self.root.all_staffs_frame.all_staffs[i][0])+".png"

            self.root.all_staffs_frame.img_temp.append(ImageTk.PhotoImage(
                Image.open(path).resize((20, 20), Image.ANTIALIAS)))
            self.all_staffs.insert('', tk.END, image=self.root.all_staffs_frame.img_temp[i], values=(
                self.root.all_staffs_frame.all_staffs[i][0], self.root.all_staffs_frame.all_staffs[i][1]))

        # self.all_staffs.pack(pady=20)
        self.all_staffs.grid(row=1, column=0, columnspan=3)

        self.root.all_staffs_frame.download_all_ava = tk.Button(
            self.root.all_staffs_frame, text="Load all thumbnail photos", command=self.change_to_download_all_btn)
        self.root.all_staffs_frame.download_all_ava.grid(column=0, row=2)

        # Show img button
        self.root.all_staffs_frame.show_thumbnail_btn = tk.Button(
            self.root.all_staffs_frame, text="Show thumbnail", command=self.display_thumbnails)
        self.root.all_staffs_frame.show_thumbnail_btn.grid(column=1, row=2)

        # Back button
        self.root.all_staffs_frame.back_button = tk.Button(
            self.root.all_staffs_frame, text="Back", command=self.change_to_connect)
        self.root.all_staffs_frame.back_button.grid(column=2, row=2)

        self.root.all_staffs_frame.pack()
        self.all_staffs.bind("<Double-1>", self.show_detail_a_staff)

    def show_detail_a_staff(self, event):
        self.root.all_staffs_frame.forget()
        iid = int(self.all_staffs.focus()[1:])-1
        ID = self.root.all_staffs_frame.all_staffs[iid][0]
        # print(id)
        self.root.staff_detail_frame = tk.Frame(self.root)
        self.root.staff_detail_frame.title = tk.Label(
            self.root.staff_detail_frame, text="Detail information", font=("Consolas 20 bold"))

        self.root.staff_detail_frame.title.grid(column=0, row=0, columnspan=3)
        self.client.sendall(bytes("GET 0" + " " + str(ID), "utf8"))
        infor = self.receive_contact()

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
            self.root.staff_detail_frame.infor, text="ID")
        self.root.staff_detail_frame.infor.id.grid(row=0, column=0)
        self.root.staff_detail_frame.infor.name = tk.Label(
            self.root.staff_detail_frame.infor, text="Full name")
        self.root.staff_detail_frame.infor.name.grid(row=1, column=0)
        self.root.staff_detail_frame.infor.phone = tk.Label(
            self.root.staff_detail_frame.infor, text="Phone number")
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
        self.root.staff_detail_frame.infor.grid(column=0, row=1, columnspan=3)

        # Avatar
        path = os.getcwd()+ "/" + default_img_path
        if os.path.exists(os.getcwd()+"/"+avatar_path+"/Image_"+str(ID)+".png"):
            path = os.getcwd()+"/"+avatar_path+"/Image_"+str(ID)+".png"


        self.root.staff_detail_frame.avt_img = ImageTk.PhotoImage(
            Image.open(path).resize((100, 100), Image.ANTIALIAS))
        self.root.staff_detail_frame.avatar = tk.Label(self.root.staff_detail_frame, image=self.root.staff_detail_frame.avt_img)
        self.root.staff_detail_frame.avatar.grid(column=0,row=2,columnspan=3)

        # Download button
        self.root.staff_detail_frame.download_btn = tk.Button(
            self.root.staff_detail_frame, text="Load avatar", command=self.change_to_download_big_avatar)
        self.root.staff_detail_frame.download_btn.grid(column=0, row=3)

        # Display button
        self.root.staff_detail_frame.download_btn = tk.Button(
            self.root.staff_detail_frame, text="Show avatar", command=self.display_avatar)
        self.root.staff_detail_frame.download_btn.grid(column=1, row=3)

        # Back button
        self.root.staff_detail_frame.back_button = tk.Button(
            self.root.staff_detail_frame, text="Back", command=self.change_to_show_all_staffs)
        self.root.staff_detail_frame.back_button.grid(column=2, row=3)

        self.root.staff_detail_frame.pack()


    def change_to_show_all_staffs(self):
        self.root.staff_detail_frame.forget()
        self.show_all_staffs()

    def change_to_connect(self):
        self.root.all_staffs_frame.forget()
        self.load_gui()

    def change_to_download_big_avatar(self):
        id = str(self.root.staff_detail_frame.id.get())
        self.client.sendall(bytes("GET 1 " + id, "utf8"))
        self.receive_contact_avatar()
        self.root.staff_detail_frame.avt_img = ImageTk.PhotoImage(
            Image.open(os.getcwd()+"/"+avatar_path+"/Image_"+id+".png").resize((100, 100), Image.ANTIALIAS))
        self.root.staff_detail_frame.avatar.config(image=self.root.staff_detail_frame.avt_img)

    def change_to_download_all_btn(self):
        self.client.sendall(bytes("GETALL 1", "utf8"))
        self.receive_all_contact_thumbnail()
        for i in range(len(self.root.all_staffs_frame.all_staffs)):
            path = os.getcwd()+"/"+default_img_path
            if os.path.exists(os.getcwd()+"/"+thumbnail_path+"Image_"+str(self.root.all_staffs_frame.all_staffs[i][0])+".png"):
                path = os.getcwd()+"/"+thumbnail_path+"Image_"+str(self.root.all_staffs_frame.all_staffs[i][0])+".png"
        self.root.check_thumbnail_loaded = True
        self.show_all_staffs()

    def display_avatar(self):
        self.root.avatar_display = Toplevel(self.root)
        self.root.avatar_display.title("Show avatar")
 
        # sets the geometry of toplevel
        self.root.avatar_display.geometry("200x200")

        iid = int(self.all_staffs.focus()[1:])-1

        self.root.avatar_display.img_temp = ImageTk.PhotoImage(Image.open(os.getcwd()+ "/" + avatar_path+"/Image_"+str(self.root.all_staffs_frame.all_staffs[iid][0])+".png").resize((180, 180), Image.ANTIALIAS))
        tmp = tk.Label(self.root.avatar_display,image=self.root.avatar_display.img_temp)
        tmp.pack()

    def display_thumbnails(self):
        self.root.thumbnail_display = Toplevel(self.root)
        self.root.thumbnail_display.title("Show thumbnails")
 
        # sets the geometry of toplevel (should be 450 x 300)
        self.root.thumbnail_display.geometry("260x100")

        self.root.thumbnail_display.img_temp = []
        self.root.thumbnail_display.size = len(self.root.all_staffs_frame.all_staffs)
        for i in range(int(self.root.thumbnail_display.size / 5)+1):
            if i == int(self.root.thumbnail_display.size/5):
                loop_inside = self.root.thumbnail_display.size % 5
            else:
                loop_inside = 5
            print("i = " + str(i))
            print("loop = " + str(loop_inside))
            for j in range(loop_inside):
                    print("i, j = " + str(i) + ", " + str(j))
                    self.root.thumbnail_display.img_temp.append(ImageTk.PhotoImage(Image.open(os.getcwd()+ "/" + thumbnail_path+"/Image_"+str(self.root.all_staffs_frame.all_staffs[j+i*5][0])+".png").resize((80, 80), Image.ANTIALIAS)))
                    tmp = tk.Label(self.root.thumbnail_display,image=self.root.thumbnail_display.img_temp[-1])
                    tmp.grid(column=j,row=i)
                
    def receive_all_contact(self):  # Feature 1
        print("receive_all_contact #1")
        data = self.client.recv(BUFFER_SIZE).decode("utf8").split(SEPARATOR)
        print("receive_all_contact #2")
        print([(data[i], data[i+1]) for i in range(0, len(data), 2)])
        return [(data[i], data[i+1]) for i in range(0, len(data), 2)]

    def receive_all_contact_thumbnail(self):  # Feature 4
        # Refresh all_staffs_frame
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


    def receive_contact(self):  # Feature 2
        data = self.client.recv(BUFFER_SIZE).decode("utf8").split(SEPARATOR)
        print(data)
        return data


    def receive_contact_avatar(self):  # Feature 5
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
    #                     receive_contact(s)
    #                 elif cmd[:5] == 'GET 1':  # Get avatar of contact, Ex: GET 1 3 -> get id = 3
    #                     receive_contact_avatar(s)

    #             print("Completed")

    #     finally:
    #         print('closing socket')
    #         s.close()


print('Client')
client = Client()
client.run()