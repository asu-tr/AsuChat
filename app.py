from tkinter import *
from tkinter.font import Font
from threading import Thread
import os
import socket


# Changes username when changeButton is clicked
# changeButtton tıklandığında kullanıcı adını değiştirir.
def change_username():
    global username
    global usernameEntry
    global usernameText

    new_username = usernameEntry.get()

    # Checking if there is sth written
    if new_username:
        username = new_username
        usernameEntry.delete(first=0, last=100)
        # My Username
        usernameText.set("Kullanıcı Adım: " + username)


# Function to receive message
# Mesaj almak için fonksiyon
def receive_message():
    global chatText
    global broadcastSocket
    global username

    while True:
        received_message = broadcastSocket.recv(1024)
        received_message_text = str(received_message.decode('utf-8'))

        username_length = len(username)

        if received_message_text.find(':') != -1 and received_message_text[0:username_length:1] != username:
            chatText.insert(END, received_message_text + '\n')


# Function to send message
# Mesaj göndermek için fonksiyon
def send_message():
    global chatText
    global username
    global sendSocket
    global messageEntry

    sendSocket.setblocking(False)

    data = messageEntry.get()

    # exit()
    if data == 'cik()':
        os._exit(1)

    elif data != '' and data != 'cik()':
        message = username + ': ' + data
        sendSocket.sendto(message.encode('utf-8'), ('255.255.255.255', 8080))
        chatText.insert(END, message + '\n')
        messageEntry.delete(first=0, last=999)

    else:
        pass


# GUI
def main_screen():
    root = Tk()
    root.title("AsuChat")
    root.resizable(0, 0)
    root.pack_propagate(0)
    root.geometry("800x600")

    # The font settings used in all texts
    # Tüm metinlerde kullanılan font ayarları
    my_font = Font(family="Arial", size=16)

    topFrame = Frame(root)
    topFrame.pack()

    # Username of user
    # Kullanıcının kullanıcı adı
    global username
    username = "User"

    # Text to be shown in username_label
    # username_label'da görüntülenecek olan metin
    global usernameText
    usernameText = StringVar(root)
    # My Username
    usernameText.set("Kullanıcı Adım: " + username)

    # Label to show username
    # Kullanıcı adının görüntülendiği label
    username_label = Label(topFrame, textvariable=usernameText, font=my_font, width=25)
    username_label.pack(side=LEFT)

    # Text box for new username if user wants to change his/her username
    # Eğer kullanıcı kullanıcı adını değiştirmek isterse yeni kullanıcı adı için metin kutusu
    global usernameEntry
    usernameEntry = Entry(topFrame, font=my_font)
    usernameEntry.pack(side=LEFT)

    # Button for changing username
    # Kullanıcı adı değiştirmek için buton
    # Change Username
    changeButton = Button(topFrame, text="Kullanıcı Adını Değiştir", font=my_font, command=change_username)
    changeButton.pack(side=RIGHT)

    chat_frame = Frame(root)
    chat_frame.pack()

    chat_scroll = Scrollbar(chat_frame)
    chat_scroll.pack(side=RIGHT, fill=Y)

    # Text area to show old messages
    # Eski mesajların görüntülendiği metin alanı
    global chatText
    chatText = Text(chat_frame, width=50, height=20, yscrollcommand=chat_scroll.set, font=my_font)
    chatText.pack(side=LEFT)

    chat_scroll.config(command=chatText.yview)

    bottom_frame = Frame(root)
    bottom_frame.pack()

    # Text to send
    # Gönderilecek mesaj
    global messageEntry
    messageEntry = Entry(bottom_frame, width=40, font=my_font)
    messageEntry.pack(side=LEFT)

    # Send
    send_button = Button(bottom_frame, text="Gönder", width=10, font=my_font, command=send_message)
    send_button.pack(side=RIGHT)

    root.mainloop()


def main():

    global broadcastSocket

    # initializing a socket for working with IPv4 addresses using UDP
    # UDP kullanarak IPv4 adresleriyle çalışmak için bir soket başlatma
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_REUSEADDR indicates that several applications can listen to the socket at once
    # SO_REUSEADDR birçok uygulamanın aynı anda soketi dinleyebileceğini gösterir
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # SO_BROADCAST indicates that the packets will be broadcast
    # SO_BROADCAST paketlerin yayınlanacağını belirtir
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # '0.0.0.0' is for listening to all interfaces
    # '0.0.0.0' tüm arayüzleri dinlemek içindir
    broadcastSocket.bind(('0.0.0.0', 8080))

    global sendSocket

    # initializing a socket for working with IPv4 addresses using UDP
    # UDP kullanarak IPv4 adresleriyle çalışmak için bir soket başlatma
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_BROADCAST indicates that the packets will be broadcast
    # SO_BROADCAST paketlerin yayınlanacağını belirtir
    sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    global receiveThread

    # Thread to receive messages
    # Mesaj almak için thread
    receiveThread = Thread(target=receive_message)
    receiveThread.setDaemon(True)

    global guiThread

    # Thread for GUI
    # GUI için thread
    guiThread = Thread(target=main_screen)
    guiThread.setDaemon(True)

    # Start threads
    # Thread başlangıcı
    receiveThread.start()
    guiThread.start()

    receiveThread.join()
    guiThread.join()


if __name__ == '__main__':
    main()
