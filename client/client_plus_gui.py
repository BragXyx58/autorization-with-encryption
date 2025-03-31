import socket
import jsonpickle
import tkinter as tk
from tkinter import messagebox


def send_request(action, username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 4000))

    request = {"action": action, "username": username, "password": password}
    client_socket.send(jsonpickle.encode(request).encode())

    response = jsonpickle.decode(client_socket.recv(1024).decode())
    messagebox.showinfo("Ответ", response["message"])
    client_socket.close()


def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        send_request("register", username, password)
    else:
        messagebox.showwarning("Ошибка", "Заполните все поля!")


def login():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        send_request("login", username, password)
    else:
        messagebox.showwarning("Ошибка", "Заполните все поля!")


root = tk.Tk()
root.title("Авторизация")
root.geometry("300x200")

tk.Label(root, text="Логин:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Пароль:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_register = tk.Button(root, text="Регистрация", command=register)
btn_register.pack()

btn_login = tk.Button(root, text="Вход", command=login)
btn_login.pack()

root.mainloop()
