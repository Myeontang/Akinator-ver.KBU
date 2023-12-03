# socket_utils.py
import socket
import json


def create_socket(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def send_data(socket, data):
    socket.send(data.encode())

def receive_data(socket, buffer_size=1024):
    res = json.loads(socket.recv(buffer_size).decode())
    return res

def close_socket(socket):
    socket.close()
