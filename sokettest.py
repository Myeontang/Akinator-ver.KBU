import socket
import mysql.connector
import pandas as pd
import json
import threading

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(user='myeontang', password='03260123kusm', host='198.0.0.1', database='joljak')
csr = db.cursor()
connected_clients = []

def handle_client(client_socket):
    try:
        while True:
            Csql = client_socket.recv(3600).decode()
            print(Csql)
            print(Csql.lower()[:6])
            if Csql.lower()[:6] == 'insert':
                csr.execute(Csql)
                db.commit()
            elif Csql[:18] == 'INSERT INTO admi':
                csr.execute(Csql)
                res = csr.fetchone()
                # print(pd.DacstaFrame(res))
                json_res = json.dumps(res)
                client_socket.send(json_res.encode())
            elif Csql.lower()[:6] == 'delete':
                csr.execute(Csql)
                db.commit()
            elif Csql.lower()[:6] == 'select':
                csr.execute(Csql)
                res = csr.fetchall()
                # print(pd.DataFrame(res))
                json_res = json.dumps(res)
                client_socket.send(json_res.encode())
    except Exception as e:
        print(f"클라이언트 연결 해제: {str(e)}")
    finally:
        # 클라이언트 연결 해제 시 처리
        if client_socket in connected_clients:
            connected_clients.remove(client_socket)
        client_socket.close()


HOST ='192.168.35.27'
PORT = 9500

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("서버 연결 중...")
while True:
    client_socket, addr = server_socket.accept()
    connected_clients.append(client_socket)  # 연결된 클라이언트를 리스트에 추가
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
    print("클라이언트 연결됨")


