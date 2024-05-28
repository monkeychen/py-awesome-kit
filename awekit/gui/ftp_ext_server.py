import socket
import tkinter as tk
from tkinter import filedialog


def receive_file(conn):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(file_path, "wb") as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    print("文件接收完成！")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8888))
    server_socket.listen(1)
    print("等待客户端连接...")
    conn, addr = server_socket.accept()
    print("客户端已连接：", addr)
    receive_file(conn)
    conn.close()
    server_socket.close()


# 创建GUI窗口
window = tk.Tk()
window.title("文件接收服务端")

# 创建开始按钮
start_button = tk.Button(window, text="开始接收", command=start_server)
start_button.pack()

# 运行GUI主循环
window.mainloop()
