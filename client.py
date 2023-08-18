
import socket
import pickle
import time

HOST = 'localhost'
PORT = 12345

# Crearea unui socket pentru client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarea la server
client_socket.connect((HOST, PORT))
print("Conectat la server.")


def get_app_list():
    client_socket.send("list".encode())
    
    app_data = client_socket.recv(1024)
    app_list = pickle.loads(app_data)
    
    return app_list


# Citirea comenzilor de la utilizator
while True:
    command = input("Introduceți o comandă (list -> obține lista de aplicații, download nume_aplicatie -> downloadeaza aplicatia, update nume_aplicatie -> actualizare versiune, refresh -> downloadeaza versiunea actualizata, exit -> închide programul): ")
    
    if command == "list":
        app_list = get_app_list()
        
        print("Lista de aplicatii disponibile:")
        for app_name, app_version in app_list.items():
            print(f"{app_name}: {app_version}")
            
    elif command.startswith("download"):
        _, app_name = command.split(" ", 1)
        client_socket.send(command.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        time.sleep(0.1)
    
    elif command.startswith("update"):
        _, app_name = command.split(" ", 1)
        client_socket.send(command.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        time.sleep(0.1)
        
    elif command.startswith("refresh"):
        _, app_name = command.split(" ", 1)
        client_socket.send(command.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        time.sleep(0.1)
    
    elif command == "exit":
        client_socket.close()
        break
    
    else:
        print("Comandă invalidă. Vă rugăm să încercați din nou.")
