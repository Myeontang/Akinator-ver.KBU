import tkinter as ttk
import tkinter.ttk
import tkinter.messagebox
import mysql.connector
import mysql
import pandas as pd
from game_gui import PlayGameApp
import socket_utils
import sys
import tkinter.messagebox

HOST = '198.0.0.1'
PORT = 10000
show_q = "SELECT Q_txt FROM question"


try:
    client_socket = socket_utils.create_socket(HOST, PORT)
    # print("연결 성공",HOST,PORT)
except Exception as e:
    # print("오류가 발생했습니다.\n",e)
    # print(HOST,PORT)
    sys.exit()

socket_utils.send_data(client_socket,show_q)
server_res = socket_utils.receive_data(client_socket,3600)
res = [*pd.DataFrame(server_res)[0]][9:]
res.append('직접입력')
class game_app:

    def __init__(self,uname):
        self.name = uname
        self.i = 0

        self.mast = ttk.Toplevel()
        self.mast.title("게임창")
        self.mast.geometry("450x235")
        self.labelcomement = ttk.Label(self.mast, background='white', width=50,height=3, text="아키네이터 ver.성서",font=("맑은 고딕", 25, "bold"),anchor='center',relief='ridge')
        self.labelcomement.pack()
        self.welcomement=ttk.Label(self.mast, background='white',width=50,text="%s 님 어서오세요"%self.name,font=("맑은 고딕",10))
        self.welcomement.pack()
        self.onebutton = ttk.Button(self.mast,text="인물등록",command=self.register)
        self.onebutton.pack()
        self.gamestart = ttk.Button(self.mast,text="게임시작",command=PlayGameApp)
        self.gamestart.pack()

    def register(self):
        self.featlist = []
        self.feat = []
        self.new_q = []
        self.Name, self.gender, self.major, self.job = ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar()
        self.root = ttk.Toplevel()
        self.root.geometry("190x500")

        self.root.title("인물등록")

        # Create a Frame to hold the widgets and scrollbar
        frame = ttk.Frame(self.root)
        frame.pack(fill='both', expand=True)

        # Create a Canvas widget
        canvas = tkinter.Canvas(frame)
        canvas.pack(side='left', fill='both', expand=True)

        # Create a Scrollbar widget
        scrollbar = ttk.Scrollbar(frame, command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        # Configure the Canvas to use the Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a Frame inside the Canvas to hold the widgets
        self.inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.infolabel = ttk.Label(self.inner_frame,text="등록할 인물의 정보를 입력해주세요!\n원활한 게임플레이를 위하여 특징은 5개 이상 등록 부탁드리겠습니다!",font=("맑은 고딕", 10,"bold"))

        self.namelabel = ttk.Label(self.inner_frame, text="이름을 입력하세요")
        self.nameentry = ttk.Entry(self.inner_frame, textvariable=self.Name)
        self.genderselect = tkinter.ttk.Combobox(self.inner_frame, values=['남자', '여자'], textvariable=self.gender,
                                                 state="readonly")
        self.genderselect.set("성별")
        self.majorselect = tkinter.ttk.Combobox(self.inner_frame,
                                                values=['성서학과', '사회복지학과', '영유아보육학과', '컴퓨터소프트웨어학과', '간호학과'],
                                                textvariable=self.major, state="readonly")
        self.majorselect.set("학과")
        self.jobselect = tkinter.ttk.Combobox(self.inner_frame, values=['학생', '교수'], textvariable=self.job,
                                              state="readonly")
        self.jobselect.set("직업")

        self.infolabel.pack(pady=30)
        self.namelabel.pack(pady=10)
        self.nameentry.pack(pady=10)
        self.genderselect.pack(pady=10)
        self.majorselect.pack(pady=10)
        self.jobselect.pack(pady=10)

        self.Fplusbutton = ttk.Button(self.inner_frame, text="특징추가", command=self.makecolum)
        self.sendbutton = ttk.Button(self.inner_frame, text="등록", command=self.register_db)
        self.Fplusbutton.pack(side='bottom', pady=15)
        self.sendbutton.pack(side='bottom', pady=15)
        # Update the scroll region of the Canvas
        self.inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

        # Bind the Scrollbar to the Canvas
        canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units'))

    def register_db(self):
        check_sql = "select * from a_people where p_name like \"{}\" and gender like \"{}\" and major like \"%{}%\" and job like \"{}\"".format(self.Name.get(), self.gender.get(), self.major.get(), self.job.get())
        #client_socket.send(check_sql.encode())
        socket_utils.send_data(client_socket,check_sql)
        server_res = socket_utils.receive_data(client_socket,3600)
        r_res = pd.DataFrame(server_res)
        if len(r_res) == 0:
            user_feat_list = [combobox.get() for combobox in self.featlist]
            all_feat = ','.join(i for i in user_feat_list)
            new_q = list(set(user_feat_list).difference(res))
            check_multi_people = " AND ".join([f"feat LIKE '%{condition}%'" for condition in user_feat_list])
            check_multi_sql = f"SELECT * FROM a_people WHERE {check_multi_people}"
            socket_utils.send_data(client_socket,check_multi_sql)
            multi_res = socket_utils.receive_data(client_socket,3600)
            if new_q != None:
                for i in new_q:
                    new_q_sql = "INSERT INTO question(Q_txt) VALUES('{}')".format(i)
                    socket_utils.send_data(client_socket,new_q_sql)
                    # csr.execute(new_q_sql)
                    # db.commit()
            if len(user_feat_list)<5:
                ttk.messagebox.showerror("등록 실패", "특징을 5개 이상 등록해주세요")
            else:
                if len(multi_res) > 1:
                    ttk.messagebox.showerror("등록 실패", "특징이 중복되어있는 인물이 있습니다\n특징을 더 추가해주세요")
                else:
                    sql = "INSERT INTO tem_people(T_name,T_gender,T_major,T_job,T_feat) VALUES('{}','{}','{}','{}','{}')".format(self.Name.get(), self.gender.get(), self.major.get(), self.job.get(),all_feat)
                    #print(sql)
                    socket_utils.send_data(client_socket,sql)
                    #client_socket.send(sql.encode())
                    # csr.execute(sql)
                    # db.commit()
                    ttk.messagebox.showinfo("등록 완료","%s님이 등록되었습니다."%self.Name.get())
                    self.root.destroy()
        else:
            ttk.messagebox.showerror("오류", "이미 등록되어있는 인물입니다.")

    # def makecolum(self):
    #     csr.execute("SHOW COLUMNS FROM a_people")
    #     cols = [col[0] for col in csr.fetchall()]
    #     setattr(self, 'featv{}'.format(self.i), ttk.StringVar())
    #     if 'feat{}'.format(self.i) not in cols:
    #         sql = "Alter TABLE a_people ADD feat{} varchar(100)".format(self.i)
    #         csr.execute(sql)
    #         db.commit()
    #         self.qcombobox = tkinter.ttk.Combobox(self.root, values=res,textvariable=getattr(self, 'featv{}'.format(self.i)))
    #         self.qcombobox.set("특징 선택")
    #         self.qcombobox.pack()
    #         self.featlist.append(self.qcombobox)
    #         self.i += 1  # i를 1 증가시키기
    #
    #     elif 'feat{}'.format(self.i) in cols:
    #         self.qcombobox = tkinter.ttk.Combobox(self.root, values=res, textvariable=getattr(self, 'featv{}'.format(self.i)))
    #         self.qcombobox.set("특징 선택")
    #         self.qcombobox.pack()
    #         self.featlist.append(self.qcombobox)
    #         self.i += 1

    def makecolum(self):
        self.feat_list = ttk.StringVar()
        self.qcombobox = tkinter.ttk.Combobox(self.inner_frame, values=res , textvariable= self.feat_list,state="readonly")
        self.qcombobox.set("특징 선택")
        self.qcombobox.pack()
        # for widget in self.featlist:
        #     widget.pack_configure(pady=10)
        self.qcombobox.bind("<<ComboboxSelected>>", self.combobox_selected)
        self.featlist.append(self.qcombobox)


    def combobox_selected(self, event):
        selected_value = self.feat_list.get()
        if selected_value == "직접입력":
            self.qcombobox.configure(state="normal")  # 수정 가능한 상태로 설정
            self.qcombobox.delete(0, "end")  # 기존 값 삭제
            self.qcombobox.focus_set()  # 콤보박스에 포커스 설정
            if selected_value not in res:
                self.new_q.append(self.feat_list.get())

        else:
            self.qcombobox.configure(state="readonly")  # 읽기 전용으로 설정
    def Done(self):
        socket_utils.close_socket(client_socket)
        self.mast.destroy()