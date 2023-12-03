import tkinter as ttk
import tkinter.ttk
import socket_utils
import sys
import tkinter.messagebox
import pandas as pd


HOST = '198.0.0.1'
PORT = 10000

try:
    client_socket = socket_utils.create_socket(HOST, PORT)
    #print("연결 성공",HOST,PORT)
except Exception as e:
    print("오류가 발생했습니다.\n",e)
    print(HOST,PORT)
    sys.exit()

look_sql = 'SELECT * FROM a_people'
socket_utils.send_data(client_socket,look_sql)
look_data = socket_utils.receive_data(client_socket,10000)

check_sql = 'SELECT * FROM tem_people'
socket_utils.send_data(client_socket,check_sql)
check_data = socket_utils.receive_data(client_socket,3600)

q_sql = 'SELECT * FROM question'
socket_utils.send_data(client_socket,q_sql)
q_data = socket_utils.receive_data(client_socket,3600)



class Adminapp:

    def __init__(self):
        self.T_name = None
        self.T_gender = None
        self.T_major = None
        self.T_job = None
        self.admin = ttk.Toplevel()
        self.admin.geometry("450x350")
        self.admin.title("관리자모드")

        self.notebook = tkinter.ttk.Notebook(self.admin)
        self.notebook.pack()

        self.lookframe = ttk.Frame(self.admin)
        self.notebook.add(self.lookframe,text="등록 인물")
        self.looklist = ttk.Listbox(self.lookframe,width=30,height=10)
        self.looklist.pack()
        for row in look_data:
            P_name, gender, major, job,feat= row
            self.looklist.insert('end', f"{P_name},{gender},{major},{job}")
        self.sendbutton = ttk.Button(self.lookframe, text="제거", command=self.look_delete)
        self.showbutton = ttk.Button(self.lookframe, text="조회", command=self.look_show_detail)
        self.refreshbutton = ttk.Button(self.lookframe, text="새로고침", command=self.look_refresh_data)
        self.sendbutton.pack()
        self.showbutton.pack()
        self.refreshbutton.pack()


        self.checkframe = ttk.Frame(self.admin)
        self.notebook.add(self.checkframe, text="신청대기")
        self.checklist = ttk.Listbox(self.checkframe, width=30, height=10)
        self.checklist.pack()
        for row in check_data:
            T_name, T_gender, T_major, T_job,T_feat= row
            self.checklist.insert('end', f"{T_name},{T_gender},{T_major},{T_job}")
        self.sendbutton = ttk.Button(self.checkframe, text="수정", command=self.show_detail)
        self.refreshbutton = ttk.Button(self.checkframe, text="새로고침", command=self.check_refresh_data)
        self.sendbutton.pack()
        self.refreshbutton.pack()

        self.qframe = ttk.Frame(self.admin)
        self.notebook.add(self.qframe, text="질문목록")
        self.qlist = ttk.Listbox(self.qframe, width=30, height=10)
        self.qlist.pack()
        for row in q_data:
            Q_txt= row[0]
            self.qlist.insert('end', Q_txt)
        self.sendbutton = ttk.Button(self.qframe, text="제거", command=self.q_delete)
        self.refreshbutton = ttk.Button(self.qframe, text="새로고침", command=self.q_refresh_data)
        self.sendbutton.pack()
        self.refreshbutton.pack()


    def look_delete(self):
        selected = self.looklist.get(self.looklist.curselection())
        select_list = selected.split(",")
        sql = "DELETE FROM a_people WHERE P_name = \'{}\' AND gender = \'{}\' and major = \'{}\' and job = \'{}\'"
        sql_query = sql.format(*select_list)
        socket_utils.send_data(client_socket,sql_query)

        selected_index = self.looklist.curselection()[0]
        self.looklist.delete(selected_index)

    def q_delete(self):
        selected = self.qlist.get(self.qlist.curselection())
        sql = f"DELETE FROM question WHERE Q_txt = \'{selected}\'"

        socket_utils.send_data(client_socket,sql)

        selected_index = self.qlist.curselection()[0]
        self.qlist.delete(selected_index)

    def show_detail(self):
        q_sql = 'SELECT * FROM question'
        socket_utils.send_data(client_socket, q_sql)
        q_data = socket_utils.receive_data(client_socket, 3600)
        selected_item = self.checklist.get(self.checklist.curselection())
        select_list = selected_item.split(",")
        check_sql = 'SELECT * FROM tem_people WHERE T_name = \'{}\' AND T_gender = \'{}\' and T_major = \'{}\' and T_job = \'{}\''
        sql_query = check_sql.format(*select_list)
        socket_utils.send_data(client_socket, sql_query)
        check_data = socket_utils.receive_data(client_socket, 3600)

        self.basic_q = [*pd.DataFrame(q_data)[0]][9:]
        self.check = ttk.Toplevel()
        self.check.title("대기자 등록")
        self.featentry =ttk.Entry(self.check)
        self.featlist = ttk.Listbox(self.check,width=30,height=10)
        self.corrbutton = ttk.Button(self.check, text="수정", command=self.update_item)
        self.sendbutton = ttk.Button(self.check, text="등록", command=self.send_db)
        self.featlist.grid(row=2, column=1)
        self.featentry.grid(row=4, column=1)
        self.corrbutton.grid(row=4,column=2)
        self.sendbutton.grid(row=5,column=2)

        for row in check_data:
            T_name,T_gender,T_major,T_job,T_feat = row
            self.T_name = T_name
            self.T_gender = T_gender
            self.T_major = T_major
            self.T_job = T_job
            self.namelabel = ttk.Label(self.check,text=T_name+' '+T_major+' '+T_job+'질문 수정')
            self.namelabel.grid(row=1, column=1)
            self.featlist.insert('end', *T_feat.split(','))
            self.featlist.bind("<ButtonRelease-1>", self.on_select)

    def look_show_detail(self):

        selected_item = self.looklist.get(self.looklist.curselection())
        looks_list = selected_item.split(",")
        looks_sql = 'SELECT * FROM a_people WHERE P_name = \'{}\' AND gender = \'{}\' and major = \'{}\' and job = \'{}\''
        sql_query = looks_sql.format(*looks_list)
        socket_utils.send_data(client_socket, sql_query)
        looks_data = socket_utils.receive_data(client_socket, 3600)

        self.show = ttk.Toplevel()
        self.show.title("등록 조회")
        self.featlist = ttk.Listbox(self.show,width=30,height=10)
        self.sendbutton = ttk.Button(self.show, text="닫기", command=self.show.destroy)
        self.featlist.grid(row=2, column=1)
        self.sendbutton.grid(row=5,column=2)

        for row in looks_data:
            P_name,gender,major,job,feat = row
            self.namelabel = ttk.Label(self.show,text=P_name+' '+major+' '+job+'정보')
            self.namelabel.grid(row=1, column=1)
            self.featlist.insert('end', *feat.split(','))

    def on_select(self,event):
        selected_f = self.featlist.curselection()
        if selected_f:
            selected_feat=[self.featlist.get(index) for index in selected_f]
            combined_feats = ', '.join(selected_feat)
            self.featentry.delete(0,ttk.END)
            self.featentry.insert(0,combined_feats)

    def update_item(self):
        selected_f = self.featlist.curselection()
        new_value = self.featentry.get()

        if selected_f:
            for index in selected_f:
                self.featlist.delete(index)
                self.featlist.insert(index,new_value)

    def send_db(self):
        user_feat = self.featlist.get(0, ttk.END)
        all_feat = ",".join(user_feat)
        new_q = list(set(user_feat).difference(self.basic_q))
        if new_q != None:
            for i in new_q:
                new_q_sql = "INSERT INTO question(Q_txt) VALUES('{}')".format(i)
                socket_utils.send_data(client_socket, new_q_sql)
        resgist_sql = "INSERT INTO a_people(P_name,gender,major,job,feat) VALUES('{}','{}','{}','{}','{}')".format(self.T_name,self.T_gender,self.T_major,self.T_job,all_feat)
        socket_utils.send_data(client_socket,resgist_sql)
        ttk.messagebox.showinfo("등록성공",self.T_name + "등록되었습니다.")
        remove_sql = "DELETE FROM tem_people WHERE T_name = \'{}\' AND T_gender = \'{}\' and T_major = \'{}\' and T_job = \'{}\'".format(self.T_name, self.T_gender, self.T_major, self.T_job)
        socket_utils.send_data(client_socket, remove_sql)
        self.check.destroy()

    def check_refresh_data(self):
        self.checklist.delete(0,'end')
        check_sql = 'SELECT * FROM tem_people'
        socket_utils.send_data(client_socket, check_sql)
        check_data = socket_utils.receive_data(client_socket, 3600)
        for row in check_data:
            T_name, T_gender, T_major, T_job, T_feat = row
            self.checklist.insert('end', f"{T_name},{T_gender},{T_major},{T_job}")

    def look_refresh_data(self):
        self.looklist.delete(0,'end')
        look_sql = 'SELECT * FROM a_people'
        socket_utils.send_data(client_socket, look_sql)
        look_data = socket_utils.receive_data(client_socket, 3600)
        for row in look_data:
            P_name, gender, major, job, feat = row
            self.looklist.insert('end', f"{P_name},{gender},{major},{job}")

    def q_refresh_data(self):
        self.qlist.delete(0,'end')
        q_sql = 'SELECT * FROM question'
        socket_utils.send_data(client_socket, q_sql)
        q_data = socket_utils.receive_data(client_socket, 3600)
        for row in q_data:
            Q_txt = row[0]
            self.qlist.insert('end', Q_txt)






# root = ttk.Tk()
# app = Adminapp()
# root.mainloop()