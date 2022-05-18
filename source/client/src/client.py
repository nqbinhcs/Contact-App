import re
import os
import socket
from tkinter import *
import tkinter as tk
from tkinter import ttk
from threading import Thread
import PIL
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog
import shutil


staffs = [[1, 'Nguyen Quang Binh', '077xxxxxxx', '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt1.png'],
          [2, 'Nguyen Trong Hieu', '078xxxxxxx', '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt2.png'],
          [3, 'Nguyen Bao Tin', '079xxxxxxx', '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt.png']]

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
        self.root.connect_frame.ip_label = tk.Label(self.root.connect_frame, text="IP").pack()
        self.root.connect_frame.ip_entry = tk.Entry(self.root.connect_frame)
        self.root.connect_frame.ip_entry.pack()

        self.root.connect_frame.port_label = tk.Label(self.root.connect_frame, text="Port").pack()
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
            tk.Label(self.root.connect_frame, text="IP/Port không được bỏ trống!", fg='red').pack()
        else:
            # Need to check if the connection has been created or not
            self.client = socket.socket()
            self.client.connect((self.ip, int(self.port)))
            self.show_all_staffs()

    def show_all_staffs(self):
        print('--> show_all_staffs')
        self.root.geometry('450x450')
        self.root.all_staffs_frame = tk.Frame(self.root)
        self.root.all_staffs_frame.title = tk.Label(self.root.all_staffs_frame, text="Danh sach nhan vien", font=("Consolas 20 bold")).pack(pady=10)
        self.all_staffs = ttk.Treeview(self.root.all_staffs_frame)
        self.all_staffs['columns'] = ("ID", "NAME")
        # self.all_staffs.column("AVATAR", anchor="center", width=100)
        self.all_staffs.column("#0", anchor="w", width=30, stretch='NO')
        self.all_staffs.column("ID", anchor="center", width=120, stretch='NO')
        self.all_staffs.column("NAME", anchor="w", width=200, stretch='NO')

        # self.all_staffs.heading("AVATAR", text="Avatar", anchor="center")
        self.all_staffs.heading("ID", text="Mã số", anchor="center")
        self.all_staffs.heading("NAME", text="Họ và tên", anchor="w")
        # Test
        self.root.size_staffs = int(len(staffs[0])/len(staffs))+1
        for i in range(self.root.size_staffs):
            self.root.all_staffs_frame.img = ImageTk.PhotoImage(Image.open(staffs[i][5]).resize((20,20), Image.ANTIALIAS))
            self.all_staffs.insert('', tk.END, image=self.root.all_staffs_frame.img, values=(staffs[i][0], staffs[i][1]))
        # self.all_staffs.insert('', tk.END, values=staffs[0][0:2])
        # self.all_staffs.insert('', tk.END, values=staffs[1][0:2])
        # self.all_staffs.insert('', tk.END, values=staffs[2][0:2])
        # Test
        self.all_staffs.pack(pady=20)

        self.root.all_staffs_frame.download_all_ava = tk.Button(self.root.all_staffs_frame, text="Tải tất cả ảnh", command=self.change_to_download_all_btn)
        self.root.all_staffs_frame.download_all_ava.pack()

        # Back button
        self.root.all_staffs_frame.back_button = tk.Button(self.root.all_staffs_frame, text="Trở về", command=self.change_to_connect)
        self.root.all_staffs_frame.back_button.pack()

        self.root.all_staffs_frame.pack()
        self.all_staffs.bind("<Double-1>", self.show_detail_a_staff)

    def show_detail_a_staff(self, event):
        self.root.all_staffs_frame.forget()
        iid = int(self.all_staffs.focus()[1:])-1
        self.root.iid_staffs = iid
        self.root.staff_detail_frame = tk.Frame(self.root)
        self.root.staff_detail_frame.title =tk.Label(self.root.staff_detail_frame, text="Thong tin chi tiet", font=("Consolas 20 bold")).pack(pady=10)

        # _infor = self.all_staffs.item(iid, 'values')
        # print(_infor)
        print(staffs[iid])
        id = tk.StringVar()
        id.set(staffs[iid][0])
        name = tk.StringVar()
        name.set(staffs[iid][1])
        phone = tk.StringVar()
        phone.set(staffs[iid][2])
        email = tk.StringVar()
        email.set(staffs[iid][3])
        # path = tk.StringVar()
        # path.set(staffs[iid][4])

        # Information
        self.root.staff_detail_frame.infor = tk.Frame(self.root.staff_detail_frame)
        self.root.staff_detail_frame.infor.id = tk.Label(self.root.staff_detail_frame.infor, text="Mã số")
        self.root.staff_detail_frame.infor.id.grid(row=0, column=0)
        self.root.staff_detail_frame.infor.name = tk.Label(self.root.staff_detail_frame.infor, text="Họ và tên")
        self.root.staff_detail_frame.infor.name.grid(row=1, column=0)
        self.root.staff_detail_frame.infor.phone = tk.Label(self.root.staff_detail_frame.infor, text="Số điện thoại")
        self.root.staff_detail_frame.infor.phone.grid(row=2, column=0)
        self.root.staff_detail_frame.infor.email = tk.Label(self.root.staff_detail_frame.infor, text="Email")
        self.root.staff_detail_frame.infor.email.grid(row=3, column=0)
        self.root.staff_detail_frame.infor.id = tk.Entry(self.root.staff_detail_frame.infor, textvariable=id, state='disabled')
        self.root.staff_detail_frame.infor.id.grid(row=0, column=1)
        self.root.staff_detail_frame.infor.name = tk.Entry(self.root.staff_detail_frame.infor, textvariable=name, state='disabled')
        self.root.staff_detail_frame.infor.name.grid(row=1, column=1)
        self.root.staff_detail_frame.infor.phone = tk.Entry(self.root.staff_detail_frame.infor, textvariable=phone, state='disabled')
        self.root.staff_detail_frame.infor.phone.grid(row=2, column=1)
        self.root.staff_detail_frame.infor.email = tk.Entry(self.root.staff_detail_frame.infor, textvariable=email, state='disabled')
        self.root.staff_detail_frame.infor.email.grid(row=3, column=1)
        self.root.staff_detail_frame.infor.pack()

        # Avatar
        self.root.staff_detail_frame.avatar = ImageTk.PhotoImage(Image.open(staffs[iid][5]).resize((100,100), Image.ANTIALIAS))
        tk.Label(self.root.staff_detail_frame, image=self.root.staff_detail_frame.avatar).pack(pady=10)

        # Download button
        self.root.staff_detail_frame.download_btn = tk.Button(self.root.staff_detail_frame, text="Tải ảnh đại diện", command=self.change_to_download_big_avatar)
        self.root.staff_detail_frame.download_btn.pack()

        # Back button
        self.root.staff_detail_frame.back_button = tk.Button(self.root.staff_detail_frame, text="Trở về", command=self.change_to_show_all_staffs)
        self.root.staff_detail_frame.back_button.pack()

        self.root.staff_detail_frame.pack()

    def change_to_show_all_staffs(self):
        self.root.staff_detail_frame.forget()
        self.show_all_staffs()

    def change_to_connect(self):
        self.root.all_staffs_frame.forget()
        self.load_gui()

    def change_to_download_big_avatar(self):
        location =  filedialog.askdirectory()
        print (location)
        print(self.root.staff_detail_frame.avatar)
        print(type(self.root.staff_detail_frame.avatar))

        shutil.copy(staffs[self.root.iid_staffs][5], location)

    def change_to_download_all_btn(self):
        location =  filedialog.askdirectory()
        des = location + '/all_small_ava/'
        if not os.path.exists(des):
            os.mkdir(des) 
        for i in range(self.root.size_staffs):
            shutil.copy(staffs[i][5], des)


print('Client')
client = Client()
client.run()