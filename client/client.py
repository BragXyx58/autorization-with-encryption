import socket
import jsonpickle


def send_request(action, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 4000))

    request = {"action": action, "username": username, "password": password}
    client_socket.send(jsonpickle.encode(request).encode())

    response = jsonpickle.decode(client_socket.recv(1024).decode())
    print(response["message"])
    client_socket.close()


print("Выберите действие: 1 - Регистрация, 2 - Вход")
choice = input("Ваш выбор: ")

username = input("Введите логин: ")
password = input("Введите пароль: ")

if choice == "1":
    send_request("register", username, password)
elif choice == "2":
    send_request("login", username, password)
else:
    print("Неверный выбор")
