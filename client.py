from customtkinter import *
from PIL import Image
from random import randint
import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('0.tcp.jp.ngrok.io', 16881))
    print("Connected!")
except Exception as e:
    print("Connection error:", e)
    exit()


image = Image.open('send.png')
send = CTkImage(light_image = image,size = (32,20))
image = Image.open('avatar.png')
avatar = CTkImage(light_image = image,size = (50,50))
image = Image.open("back.jpg")
bg = CTkImage(light_image = image,size = (800,550))

main = CTk()
main.geometry('800x550')
main.title("LogiTalk")

main.resizable(0,0)

Account_frame =  CTkFrame(main,width = 270, height = 350, fg_color = "#1e1e1e",corner_radius= 20)
Chat_frame = CTkFrame(main,width=500,height=370,fg_color = "#1e1e1e",corner_radius= 20)


color = 0




def settings_spawn():
    global settings_button
    global avatar_photo

    avatar_photo = CTkButton(main,
                             image=avatar,
                             width = 70,
                             height = 90,
                             text = "",
                             corner_radius=20,
                             fg_color="#9f2fa3",
                             hover_color="#9f2fa3",
                             state="disabled",
                             bg_color = "#1e1e1e")
    avatar_photo.place(x = 100, y = 190)


    settings_label = CTkLabel(main,
                              text = "Налаштування",
                              font = ("Areal",20,"bold"),
                              bg_color = "#1e1e1e").place(x=80,y=300)


    settings_label_theme = CTkLabel(main,
                                    text = "Тема:",
                                    font = ("Areal",20,"bold"),
                                    bg_color = "#1e1e1e").place(x=80,y=350)


    settings_button = CTkButton(main,
                                text = "",
                                height = 40,
                                width = 40,
                                fg_color = "#9f2fa3",
                                hover_color = "#9f2fa3",
                                corner_radius= 25,
                                command = change_color,
                                bg_color = "#1e1e1e")

    settings_button.place(x=150,y=345)


def colorchange(col):
    global Name
    global entry
    global textbox
    global Send_button

    Name.configure(fg_color = col,hover_color=col)
    entry.configure(border_color = col)
    Send_button.configure(border_color = col,fg_color = col,hover_color = col)
    textbox.configure(border_color = col)
    settings_button.configure(hover_color = col,fg_color = col)
    avatar_photo.configure(hover_color = col,fg_color = col)

colors = ["#9f2fa3", #Фіолетовий
          "#ed264a", #Червоний
          "#e6a030", #Помаранчевий
          "#d1c956", #Жовтий
          "#3295c9", #Голубий
          "#2cd4c3", #Бірюзовий
          "#1dcf46", #Світлозелений
          "#318238", #Темнозелений
          "#3051e6", #Синій
          "#5132c9", #Темносиній
          "#787878", #Сірий
          "#404040"] #Чорний


def change_color():
    global color
    color +=1
    if color > len(colors) - 1:
        color = 0
    colorchange(colors[color])


def register():
    global username
    global register_name
    global textbox
    global Send_button
    username = register_name.get()
    client_socket.send(f"TEXT@{username}@joined".encode("utf-8"))
    if 0 < len(username) < 11:

        if not (any(char.isdigit() for char in username) or any(char.isalpha() for char in username)):
            username = "Анонім"

        register_name.destroy()
        register_button.destroy()
        register_label.destroy()
        CTkLabel(main,text=f"Привіт {username}!",font=("Areal",20,"bold"),bg_color = "#1e1e1e").place(x=100-(len(username)*4),y=150)
        textbox.configure(width=450,height=300,corner_radius=20,bg_color = "#1e1e1e")
        entry.configure(width=375,corner_radius=10,bg_color = "#1e1e1e")
        Send_button.configure(width = 70,height = 28 ,corner_radius=10,bg_color = "#1e1e1e",border_width= 0)
        textbox.place(x=315,y=150)
        Send_button.place(x = 695, y = 455)
        entry.place(x=315, y=455)
        Account_frame.configure(width=250, height=370)
        Account_frame.place(x=30, y=130)
        Chat_frame.place(x=290, y=130)
        settings_spawn()

    elif len(username) == 0:
        register_label.configure(text="Ваше ім'я пусте!")
        register_name.delete(0, END)

    elif len(username) > 11:
        register_label.configure(text="Ваше ім'я задовге!")
        register_name.delete(0, END)
    threading.Thread(target=get_message, daemon=True).start()


def send_message():
    message = entry.get().strip()

    if message == "":
        return

    packet = f"TEXT@{username}@{message}"
    try:
        client_socket.send(packet.encode("utf-8"))
    except:
        print("Помилка на сервері!")
    textbox.configure(state="normal")
    textbox.insert("end", f"{username}: {message}" + "\n")
    textbox.configure(state="disabled")


    entry.delete(0, END)
pos = [[0,0],[800,0],[0,550],[800,550]]
for i in range(4):
    CTkFrame(main,width=100,height=100,fg_color = "#1e1e1e",corner_radius=50).place(x=pos[i][0]-50,y=pos[i][1]-50)



Name = CTkButton(main, text = "LogiTalk",
                font = ("Areal", 30, "bold"),
                width=50,
                height=100,
                corner_radius= 30,
                fg_color = "#9f2fa3",
                hover_color = "#9f2fa3")


entry = CTkEntry(main,width = 225,
                 border_color="#9f2fa3",
                 border_width=2,
                 corner_radius=1,
                 placeholder_text="Введіть повідомлення",
                 font=("Areal",15,"bold"))


textbox = CTkTextbox(main,width = 300,
                     height = 350,
                     state = 'disabled',
                     border_color="#9f2fa3",
                     border_width=2,
                     corner_radius=20,
                     font=("Areal",15,"bold"))


Send_button = CTkButton(main,text = "",
                        font = ("Areal", 20, "bold"),
                        width = 75,
                        height = 27,
                        corner_radius=1,
                        border_color="#9f2fa3",
                        border_width=1,
                        hover_color="#9f2fa3",
                        fg_color="#9f2fa3",
                        border_spacing = 1,
                        image=send,
                        command=send_message)


register_name = CTkEntry(main,
                         width = 225,
                         border_color="#9f2fa3",
                         border_width=2,
                         corner_radius=10,
                         placeholder_text="Введіть ваше ім'я",
                         bg_color = "#1e1e1e")


register_label = CTkLabel(main,text = "Введіть ваше ім'я",
                          font = ("Areal", 20, "bold"),
                          bg_color = "#1e1e1e")


register_button = CTkButton(main,text = "Вхід",
                            width = 100,
                            height = 25,
                            font = ("Areal", 20, "bold"),
                            fg_color = "#9f2fa3",
                            hover_color = "#9f2fa3",

                            command = register)


entry.bind("<Return>", lambda e: send_message())


def get_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()


            if not message:
                break

            textbox.configure(state='normal')
            textbox.insert("end", message + "\n")
            textbox.configure(state='disabled')
            textbox.see("end")

        except:
            break




Account_frame.place(x = 80, y = 150)
Chat_frame.place(x = 29000, y = 130)

Name.place(y = 10,x =300)

textbox.place(x = 450, y = 150)

register_name.place(x = 100, y = 300)

register_label.place(x = 115, y = 250)

register_button.place(x = 155, y = 350)

main.mainloop()