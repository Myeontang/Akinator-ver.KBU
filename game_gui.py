import tkinter as ttk
import mysql.connector
import mysql
import pandas as pd
import random
import sys
import socket_utils

def plus_f(o_sqlm,f_noun):
    sqlm = ' and match(feat) against (\'{}*\' in boolean mode)'.format(f_noun)
    return o_sqlm+sqlm

HOST = '198.0.0.1'
PORT = 10000
try:
    client_socket = socket_utils.create_socket(HOST, PORT)
    print("연결 성공",HOST,PORT)
except Exception as e:
    #print("오류가 발생했습니다.\n",e)
    #
    #print(HOST,PORT)
    sys.exit()

gender_q ="SELECT Q_TXT FROM QUESTION WHERE (Q_TXT LIKE \"%여자%\" OR Q_TXT LIKE \"%남자%\")"


major_q ="SELECT Q_TXT FROM QUESTION WHERE Q_TXT LIKE \"%학과%\""


job_q ="SELECT Q_TXT FROM QUESTION WHERE Q_TXT LIKE \"%학생입니까?\" OR Q_TXT LIKE \"%교수입니까?\""


show_q = "SELECT Q_txt FROM question"


class PlayGameApp:

    # global gen_q
    # global maj_q
    # global j_q

    def __init__(self):


        self.game = ttk.Toplevel()
        self.game.geometry("1024x250")
        # self.game.title("아키네이터 ver.성서")
        self.playlabel = ttk.Label(self.game, text='아키네이터 ver.성서 입니다!\n자신이 생각하는 친구나 교수님을 생각하며 질문에 답해보세요\n시작하기를 누르면 시작합니다\n', background='white',width=50,height=5,font=("맑은 고딕",10,"bold"),anchor='center',relief='ridge')
        self.playlabel.pack()
        self.startbutton = ttk.Button(self.game, text="START", command=self.reset)
        self.startbutton.pack()
        self.current_question = None

    def reset(self):
        socket_utils.send_data(client_socket, show_q)
        server_fres = socket_utils.receive_data(client_socket, 3600)
        res = [*pd.DataFrame(server_fres)[0]]
        self.feat_q = res[9:]

        socket_utils.send_data(client_socket, gender_q)
        server_gres = socket_utils.receive_data(client_socket, 3600)
        self.gen_q = [*pd.DataFrame(server_gres)[0]]

        socket_utils.send_data(client_socket, major_q)
        server_mres = socket_utils.receive_data(client_socket, 3600)
        self.maj_q = [*pd.DataFrame(server_mres)[0]]

        socket_utils.send_data(client_socket, job_q)
        server_jres = socket_utils.receive_data(client_socket, 3600)
        self.j_q = [*pd.DataFrame(server_jres)[0]]


        print(self.maj_q)
        self.playlabel.configure(font=("맑은 고딕",15,"bold"))
        self.startbutton.destroy()
        button_frame = ttk.Frame(self.game)
        button_frame.pack(padx=10, pady=10)
        self.yes_button = ttk.Button(button_frame, text="예", command=self.select_yes, width=5,font=('맑은 고딕',10,'bold'),anchor='center',relief='ridge')
        self.no_button = ttk.Button(button_frame, text="아니오", command=self.select_no, width=5,font=('맑은 고딕',10,'bold'),anchor='center',relief='ridge')
        self.yes_button.pack()
        self.no_button.pack()
        self.gen = self.user_c(self.gen_q).lstrip()
        self.maj = self.user_c(self.maj_q)[3:].lstrip()
        self.job = self.user_c(self.j_q).lstrip()
        sqlm = "select * from a_people where gender like \"{}\" and major like \"%{}%\" and job like \"{}\"".format(self.gen,self.maj,self.job)
        while True:
            socket_utils.send_data(client_socket,sqlm)
            res = pd.DataFrame(socket_utils.receive_data(client_socket,3600))
            # print(res)
            #print(len(res))
            if len(res) == 0:
                self.plus_p()
            elif len(res) == 2:
                p1 = res[4][0].split(',')
                p2 = res[4][1].split(',')
                if len(p1) > len(p2):
                    self.feat_q = list(set(p2).difference(p1))
                    hubo = res[0][0]
                    hubo_m = res[2][0]
                    print(self.feat_q)
                else:
                    self.feat_q = list(set(p1).difference(p2))
                    hubo = res[0][1]
                    hubo_m = res[2][1]
                    print(self.feat_q)
                self.feat = self.f_user_c(self.feat_q)
                sqlm = plus_f(sqlm, self.feat)
                if self.feat is None:
                    lastper = hubo
                    lastper_m = hubo_m
                    break
            elif len(res)>2:
                self.feat = self.f_user_c(self.feat_q)
                sqlm = plus_f(sqlm,self.feat)
            elif len(res) == 1:
                lastper = res[0][0]
                lastper_m = res[2][0]
                break

        self.print_a(lastper,lastper_m)

    def user_c(self,q_list):
        while True:
            if len(q_list)!=1:
                question = random.choice(q_list)
                self.playlabel.configure(text=question)
                self.a_num= ttk.StringVar()
                self.game.wait_variable(self.a_num)
                if self.a_num.get() == "1":
                    return question[5:-4].lstrip()
                elif self.a_num.get() == "2":
                    q_list.remove(question)
                else:
                    print("읭")
            elif len(q_list) == 1:
                return q_list[0][5:-4].lstrip()

    def f_user_c(self,q_list):
        while True:
            if len(q_list) != 1:
                self.question = random.choice(q_list)
            elif len(q_list)==1:
                self.question=q_list[0]
            self.playlabel.configure(text=self.question)
            self.a_num = ttk.StringVar()
            self.game.wait_variable(self.a_num)
            if self.a_num.get() == "1":
                res = self.question[6:-4].rstrip()
                q_list.remove(self.question)
                return res
            elif self.a_num.get() == "2":
                q_list.remove(self.question)
                if len(q_list) == 0:
                    return None

    def plus_p(self):
        self.playlabel.configure(text="일치하는 인물이 없습니다.\n 새로 추가 하시겠습니까?")
        self.game.wait_variable(self.a_num)
        if self.a_num.get()=="1":
            self.Done()
        elif self.a_num.get()=="2":
            self.Done()

    def print_a(self,name,major):
        text = "당신이 생각한 인물은 \"{}\" \n \"{}\" 입니다.".format(major,name)
        self.playlabel.configure(text=text)
        self.game.wait_variable(self.a_num)
        if self.a_num.get() == "1":
            self.Done()
        elif self.a_num.get() == "2":
            self.plus_p()


    def select_yes(self):
        self.a_num.set("1")
    def select_no(self):
        self.a_num.set("2")

    def Done(self):
        # socket_utils.close_socket(client_socket)
        self.game.destroy()

# root = ttk.Tk()
# app = PlayGameApp(root)
# root.mainloop()
