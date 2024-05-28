import socket
import tkinter as tk
from tkinter import filedialog


def send_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, "rb") as file:
        data = file.read()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8888))
    client_socket.sendall(data)
    client_socket.close()
    print("文件发送完成！")


# 创建GUI窗口
window = tk.Tk()
window.title("文件发送客户端")

# 创建发送按钮
send_button = tk.Button(window, text="选择文件并发送", command=send_file)
send_button.pack()

# 运行GUI主循环
window.mainloop()
