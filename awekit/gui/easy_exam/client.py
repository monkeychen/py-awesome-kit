import tkinter as tk


def login():
    username = username_entry.get()
    password = password_entry.get()
    # Add your login logic here
    print("Username:", username)
    print("Password:", password)
    # If login is successful, close login window and open main client interface
    if username == "admin" and password == "password":
        window.destroy()
        open_main_interface()


def open_main_interface():
    main_window = tk.Tk()
    main_window.title("Main Interface")
    main_window.geometry("800x600")
    # Add your main interface elements here
    main_window.mainloop()


window = tk.Tk()
window.title("Login Window")
window.geometry("400x300")
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()
login_button = tk.Button(window, text="Login", command=login)
login_button.pack()
cancel_button = tk.Button(window, text="Cancel", command=window.quit)
cancel_button.pack()
window.mainloop()
