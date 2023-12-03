import asyncio
import tkinter as ttk
import tkinter.messagebox
from biblebot import LmsAPI
from client import game_app
import socket_utils
import sys
import hashlib
from test import Adminapp

admin_id = '관리자'
admin_pw = '0326'
HOST = '198.0.0.1'
PORT = 10000

try:
    client_socket = socket_utils.create_socket(HOST, PORT)
    #print("연결 성공",HOST,PORT)
except Exception as e:
    print("오류가 발생했습니다.\n",e)
    #print(HOST,PORT)
    sys.exit()

async def lms(userid, pw):
    response = await LmsAPI.Login.fetch(userid, pw)
    result = LmsAPI.Login.parse(response)
    if str(result)[:9] == "ResourceD":
        cookie = result.data["cookies"]
        Presponse = await LmsAPI.Profile.fetch(cookie)
        NaME = LmsAPI.Profile.parse_name(Presponse)
        App.name = str(NaME)[28:31]
        ttk.messagebox.showinfo("로그인성공", App.name+"님 어서오세용~")
        game_app(App.name)
    elif str(result)[:9] == "ErrorData":
        ttk.messagebox.showerror("로그인실패", "아이디와 비밀번호가 일치하지 않습니다.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def admin_login(id,password):
    hashed_password = hash_password(password)
    admin_sql = "SELECT * FROM admins WHERE username = \'{}\' AND password =\'{}\'".format(id,hashed_password)
    socket_utils.send_data(client_socket,admin_sql)
    admin = socket_utils.receive_data(client_socket,3600)
    return admin is not None


class App:

    def __init__(self,master):
        self.master = master
        self.userid, self.pw = ttk.StringVar(), ttk.StringVar()
        self.name = None
        self.master.title("아키네이터 ver.성서")
        ttk.Label(self.master,text="아이디").grid(row=1,column=1)
        ttk.Label(self.master, text="비밀번호 : ").grid(row=2, column=1)
        ttk.Entry(self.master, textvariable=self.userid).grid(row=1, column=2)
        ttk.Entry(self.master, textvariable=self.pw,show="*").grid(row=2, column=2)
        ttk.Button(self.master, text="로그인",command=self.submit).grid(row=3, column=2)
        ttk.Button(self.master, text="관리자로그인", command=self.admin_submit).grid(row=3, column=1)
        ttk.Button(self.master, text="종료", command=self.Done, overrelief="sunken").grid(row=4)

    def submit(self):
        userid = self.userid.get()
        pw = self.pw.get()
        asyncio.run(lms(userid,pw))

    def admin_submit(self):
        adminid = self.userid.get()
        adminpw = self.pw.get()
        if adminid == admin_id and adminpw == adminpw:
            ttk.messagebox.showinfo("관리자로그인성공", "관리자모드 실행합니다.")
            Adminapp()
        else:
            ttk.messagebox.showerror("로그인실패", "아이디와 비밀번호가 일치하지 않습니다.")

    def Done(self):
        socket_utils.close_socket(client_socket)
        self.master.quit()


root = ttk.Tk()
app = App(root)
root.mainloop()

