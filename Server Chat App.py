from tkinter import *
from socket import *
import _thread

# initial server
def initialize_server():
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
    port = 1234
    # initialize server
    s.bind((host, port))
    # set no. of clients
    s.listen(1)
    # accept the connection from client
    conn, addr = s.accept()

    return conn

# update the chat log
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    # update the message in the window
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'OTHER: ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages only
    chatlog.yview(END)

# function to send message
def send():
    global textbox
    # get the message
    msg = textbox.get("0.0", END)
    # update the chatlog
    update_chat(msg, 0)
    # send the message
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

# function to receive message
def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

# GUI function
def GUI():
    global chatlog
    global textbox

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Server Chat")
    # set size for the window
    gui.geometry("400x470")

    # text space to display messages
    chatlog = Text(gui, bg='grey97')
    chatlog.config(state=DISABLED)

    # button to send messages
    sendbutton = Button(gui, bg='green', fg='black', text='SEND', command=send)

    # textbox to type messages
    textbox = Text(gui, bg='grey97')

    # place the components in the window
    chatlog.place(x=6, y=6, height=397, width=370)
    textbox.place(x=6, y=421, height=20, width=285)
    sendbutton.place(x=305, y=421, height=20, width=70)

    # bind textbox to use ENTER Key
    textbox.bind("<KeyRelease-Return>", press)

    # create thread to capture messages continuously
    _thread.start_new_thread(receive, ())

    # to keep the window in loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    conn = initialize_server()
    GUI()