import socket
import os
import pickle


HOST = 'localhost'
PORT = 12345

# Lista cu numele aplicațiilor executabile disponibile pe server
app_list = {'app1.exe': 1.0, 'app2.exe': 2.0, 'app3.exe': 1.2}
client_app = {} 

# Crearea unui server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asocierea adresei și portului serverului cu server_socket
server_socket.bind((HOST, PORT))

# Ascultarea conexiunilor clientilor
server_socket.listen(1)

print("Serverul este gata pentru a primi conexiuni de la client.")


def send_app_list(client_socket):
    app_data = pickle.dumps(app_list)
    client_socket.send(app_data)


def download_app(client_socket, app_name):
    if app_name in app_list:
        if any(app[0] == app_name for app in client_app.get(client_socket, [])):
            print(f"Aplicația '{app_name}' a fost deja descărcată de către client.")
            client_socket.send(f"Aplicația '{app_name}' a fost deja descărcată.".encode())
        else:
            if client_socket in client_app:
                client_app[client_socket].append((app_name, app_list[app_name]))
            else:
                client_app[client_socket] = [(app_name, app_list[app_name])]
            print(f"Aplicația '{app_name}' a fost descărcată cu succes.")
            print(f"Lista aplicațiilor descărcate de clientul {client_socket.getpeername()}:")
            for app, version in client_app[client_socket]:
                print(f"Nume: {app}, Versiune: {version}")
            client_socket.send(f"Aplicația '{app_name}' a fost descărcată cu succes. S-a downloadat versiunea'{app_list[app_name]}'".encode())
    else:
        print(f"Aplicația '{app_name}' nu există pe server.")
        client_socket.send(f"Aplicația '{app_name}' nu există pe server.".encode())


def update_app_version(app_name):
    if app_name in app_list:
        new_version = app_list[app_name] + 0.1
        app_list[app_name] = new_version
        print(f"Aplicația '{app_name}' a fost actualizată cu succes. Noua versiune: {new_version}.")
        for client_socket, downloaded_apps in client_app.items():
            if app_name in downloaded_apps:
                client_socket.send(f"Noua versiune {new_version} a aplicatiei '{app_name}' e disponibila. Apelati metoda download_update.".encode())
        print("Lista aplicatiilor de pe server:")
        print(app_list)
    else:
        print(f"Aplicația '{app_name}' nu există pe server.")

def update_client_app(app_name):
    if app_name in app_list:
        if any(app[0] == app_name for app in client_app.get(client_socket, [])):
            for app in client_app[client_socket]:
                    if app[1] == app_list[app_name]:
                        client_socket.send(f"Aplicația '{app_name}' are deja ultima versiune instalată.".encode())
                    else:
                        for i, app_tuple in enumerate(client_app[client_socket]):
                            if app_tuple[0] == app_name:
                                updated_app = (app_name, app_list[app_name])
                                client_app[client_socket][i] = updated_app
                                client_socket.send(f"Aplicația '{app_name}' a fost actualizată cu ultima versiune.".encode())
                                print(f"Lista aplicațiilor descărcate de clientul {client_socket.getpeername()}:")
                                for app, version in client_app[client_socket]:
                                    print(f"Nume: {app}, Versiune: {version}")
                    break
        
        else:
            client_socket.send(f"Nu aveți aplicația '{app_name}' instalată. Folosiți comanda 'download' pentru a o descărca.".encode())
    else:
        print(f"Aplicația '{app_name}' nu există pe server.")

while True:
    client_socket, client_address = server_socket.accept()
    print("S-a realizat o conexiune cu clientul:", client_address)

    while True:
        command = client_socket.recv(1024).decode()

        if command == "list":
            send_app_list(client_socket)
        elif command.startswith("download"):
            _, app_name = command.split(" ", 1)
            download_app(client_socket, app_name)
        elif command.startswith("update"):
            _, app_name = command.split(" ", 1)
            update_app_version(app_name)
            client_socket.send(f"Aplicația '{app_name}' a fost actualizată cu succes.".encode())
        elif command.startswith("refresh"):
            _, app_name = command.split(" ", 1)
            update_client_app(app_name)
        elif command == "exit":
            break

    client_socket.close()
