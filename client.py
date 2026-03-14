import socket
import json
import os

def login(client_socket):
    username = input("Enter your username to login: ")
    client_socket.send(username.encode())

    response = client_socket.recv(1024).decode()
    if response == "1":
        print("Login successful.")
        return True
    else:
        print("Login failed. User does not exist.")
        return False

def sign_up(client_socket):
    new_username = input("Enter a new username to sign up: ")
    client_socket.send(new_username.encode())
    print("Sign-up successful (assumed). You can now log in.")

def my_Filelist():
    if not os.path.exists(r"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\my_folder"):
        return []

    return os.listdir(r"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\my_folder")

def print_list(list): #  print the list of files
    for x in list:
        print(x)
    return

def check_list(client_sock):   #  check the file exist or not 
    check_msg = client_sock.recv(4096).decode()

    if check_msg == "1":
        return 1
    else:
        return 0

def check_file(list, file_name):
    for x in list:
        if file_name == x:
            return 1
    return 0

def send_file(cl_socket, file_name):
    file = open(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\my_folder\{file_name}", "rb")
    data = file.read()

    cl_socket.sendall(data)
    cl_socket.send(b"<END>")

def recv_file(cl_socket, f_name):  #  recive the file
    file = open(rf"C:\BTech_IT_6th_sem\Distributed_Lab\DISTRIBUTED_Project\my_folder\{f_name}", "wb")     #  create file
    data = b""
    while True:
        chunk = cl_socket.recv(1024)
        data += chunk
        if b"<END>" in data:
            data = data.replace(b"<END>", b"")  # remove the marker
            break
    file.write(data)   #  write the data
    file.close()
    print("file downloaded")

    return

def handle_command(client_socket):
    
    while True:
        msg = input("You: ")
        client_socket.send(msg.encode())

        if msg.lower() == "close":
            print("connection closed")
            break
        elif msg.lower() == "list":
            recv_msg = client_socket.recv(4096).decode()
            file_list = json.loads(recv_msg)
            print_list(file_list)
        elif msg.lower() == "download":
            tem_list = json.loads(client_socket.recv(4096).decode())
            print_list(tem_list)
            dwnl_file = input("Enter the name of the file from the above: ")
            client_socket.send(dwnl_file.encode())
            if check_list(client_socket) == 1:
                recv_file(client_socket, dwnl_file)
            else:
                print(f"Error {dwnl_file} not found")
        elif msg.lower() == "upload":
            my_list = my_Filelist()
            print_list(my_list)
            upld_file = input("Enter the file name from above: ")
            if check_file(my_list, upld_file) == 1:
                client_socket.send("1".encode())
                client_socket.send(upld_file.encode())
                send_file(client_socket, upld_file)
                print(f"{upld_file} uploaded")
            else:
                client_socket.send("0".encode())
                print(f"Error {upld_file} doesnot found")
        elif msg.lower() == "delete":
            temp_list = json.loads(client_socket.recv(4096).decode())
            print_list(temp_list)
            del_file = input("Enter the name of the file from the above(to delete): ")
            client_socket.send(del_file.encode())
            suc =client_socket.recv(1024).decode()
            if suc == "1":
                print("File Deleted..")
            else:
                print("Error Occured File doesnot delete!")
        else:
            recv_msg = client_socket.recv(4096).decode()
            print(f"server: {recv_msg}")

    return

def start_client():
    server_ip_port = ("127.0.0.1",5050)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_ip_port)

    choice = input("type S for sign up & L for log in: ")
    client_socket.send(choice.encode())

    if choice.lower() == "l":
        if login(client_socket):
            print("Access granted. Proceeding to commands...")
            handle_command(client_socket)
        else:
            client_socket.close()
        print("connection closed")


    elif choice.lower() == "s":
        sign_up(client_socket)
        if login(client_socket):
            print("Access granted. Proceeding to commands...")
            handle_command(client_socket)
        else:
            client_socket.close()
            print("connection closed")


    else:
        print("Invalid choice.")
        client_socket.close()
        print("connection closed")

        return
            
    client_socket.close()
    return

start_client()