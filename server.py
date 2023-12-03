import socket

# 서버의 IP 주소와 포트 번호를 지정합니다.
HOST = 'localhost'
PORT = 9000

# 소켓 객체를 생성합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # window 10048
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 소켓 객체를 사용하기 위한 IP 주소와 포트 번호를 바인딩합니다.
server_socket.bind((HOST, PORT))

# 서버 소켓을 리스닝 모드로 변경합니다.
server_socket.listen()

# 클라이언트가 접속할 때까지 대기합니다.
print('Server is listening...')

# 클라이언트와 연결이 성공하면 새로운 소켓 객체를 생성합니다.
client_socket, addr = server_socket.accept()

# 클라이언트가 접속했다는 메시지를 출력합니다.
print(f'Connected by {addr}')

# 클라이언트와 데이터를 주고받습니다.
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print(f'Received from {addr}: {data.decode()}')
    client_socket.sendall(data)

# 소켓 객체를 닫습니다.
client_socket.close()
server_socket.close()
