from tkinter import *

root = Tk()
root.title("AsuChat")

room = "NO ROOM"
roomLabelText = "You're in " + room
roomLabel = Label(root, text=roomLabelText)
roomLabel.grid(row=0, column=1, columnspan=8)

chatScroll = Scrollbar(root)
chatScroll.grid(row=1, column=8, rowspan=8)

chatText = Text(root, width=50)
chatText.grid(row=1, column=1, rowspan=12, columnspan=4)

chatScroll.config(command=chatText.yview)
chatText.config(yscrollcommand=chatScroll.set)


usernameLabel = Label(root, text="My Username:")
usernameLabel.grid(row=1, column=0, padx=5, pady=5)

username = "User"
myUsernameLabel = Label(root, text=username)
myUsernameLabel.grid(row=2, column=0, padx=5, pady=5)

changeButton = Button(root, text="Change Username")
changeButton.grid(row=3, column=0, padx=5, pady=5)

generalButton = Button(root, text="GENERAL ROOM")
generalButton.grid(row=4, column=0, padx=5, pady=5)

# others label
# others list

messageEntry = Entry(root)
messageEntry.grid(row=13, column=1, columnspan=10)

sendButton = Button(root, text="Send")
sendButton.grid(row=13, column=7, columnspan=2)

root.mainloop()
