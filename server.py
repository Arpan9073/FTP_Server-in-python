import socket
import threading
import os
import json

user_list = []

def user_login(client_socket):
    username = client_socket.recv(1024).decode().strip()

    if username not in user_list:
        client_socket.send("0".encode())
        client_socket.close()
        return False

    client_socket.send("1".encode())
    return True

def sign_up(client_socket):
    new_user = client_socket.recv(1024).decode()
    user_list.append(new_user)

def list_files():
    folder_path = r"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\public"
    if not os.path.exists(folder_path):
        return []

    return os.listdir(folder_path)

def check_file(list, file_name):
    for x in list:
        if file_name == x:
            return 1
    return 0
   
def check_list(client_sock):   #  check the file exist or not 
    check_msg = client_sock.recv(4096).decode()

    if check_msg == "1":
        return 1
    else:
        return 0
    
def delete_file(file_name):
        if os.path.exists(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\public\{file_name}"):
            os.remove(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\public\{file_name}")
            return True
        else:
            return False

def send_file(cl_socket, file_name):
    file = open(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\public\{file_name}", "rb")
    data = file.read()

    cl_socket.sendall(data)
    cl_socket.send(b"<END>")

    return

def recv_file(cl_socket, f_name):  #  recive the file
    file = open(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\public\{f_name}", "wb")     #  create file
    data = b""
    while True:
        chunk = cl_socket.recv(1024)
        data += chunk
        if b"<END>" in data:
            data = data.replace(b"<END>", b"")  # remove the marker
            break
    file.write(data)   #  write the data
    file.close()

    return

def handle_command(client_socket, address):
    while True:
        data = client_socket.recv(4096).decode()

        if data.lower() == "close":
            print(f"connection {address[0]} {address[1]} closed")
            break
        elif data.lower() == "list":
            file_list = json.dumps(list_files())
            client_socket.send(file_list.encode())
        elif data.lower() == "download":
            tem_list = list_files()
            client_socket.send(json.dumps(tem_list).encode())
            file_name = client_socket.recv(4096).decode()
            if check_file(tem_list, file_name) == 1:
                client_socket.send("1".encode())
                send_file(client_socket, file_name)
            else:
                client_socket.send("0".encode())
        elif data.lower() == "upload":
            if check_list(client_socket) == 1:
                upld_file = client_socket.recv(4096).decode()
                recv_file(client_socket, upld_file)
            else:
                pass
        elif data.lower() == "delete":
            tem_list = list_files()
            client_socket.send(json.dumps(tem_list).encode())
            delfile_name = client_socket.recv(4096).decode()
            if delete_file(delfile_name):
                client_socket.send("1".encode())
            else:
                client_socket.send("0".encode())
        else:
            client_socket.send("Error command".encode())
    
    return
    

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    ls_msg = client_socket.recv(1024).decode()

    if ls_msg.lower() == "l":
        if not user_login(client_socket):
            print(f"Login failed. Connection closed from {address[0]}, {address[1]}")
            return
        
        print("Client logged in. Ready to receive commands...")
        handle_command(client_socket, address)
    elif ls_msg.lower() == "s":
        sign_up(client_socket)
        if not user_login(client_socket):
            print(f"Login failed. Connection closed from {address[0]}, {address[1]}")
            return
        
        print("Client logged in. Ready to receive commands...")
        handle_command(client_socket, address)
    else:
        client_socket.send("Error".encode())

    client_socket.close()
    print(f"connection closed of {address[0]}, {address[1]}")
    return
    
def start_server():
    ip_port = ("127.0.0.1", 5050)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ip_port)

    server.listen()
    print(f"Server is listening on {ip_port}")

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

start_server()