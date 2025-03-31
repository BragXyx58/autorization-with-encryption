import hashlib
import socket
import pyodbc
import jsonpickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 4000))
server_socket.listen(5)

server = 'localhost\\SQLEXPRESS'
database = 'db_passwords'
dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(dsn)
cursor = conn.cursor()

print("Сервер запущен")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone():
        return {"status": "error", "message": "Пользователь уже существует"}

    password_hash = hash_password(password)
    cursor.execute("INSERT INTO Users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    return {"status": "success", "message": "Регистрация успешна"}


def login(username, password):
    password_hash = hash_password(password)
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password_hash = ?", (username, password_hash))
    return {"status": "success", "message": "Вход выполнен"} if cursor.fetchone() else {"status": "error",
                                                                                        "message": "Ошибка входа"}


while True:
    client_socket, _ = server_socket.accept()
    data = client_socket.recv(1024).decode()
    request = jsonpickle.decode(data)

    if request["action"] == "register":
        response = register(request["username"], request["password"])
    elif request["action"] == "login":
        response = login(request["username"], request["password"])
    else:
        response = {"status": "error", "message": "Неизвестное действие"}

    client_socket.send(jsonpickle.encode(response).encode())
    client_socket.close()
