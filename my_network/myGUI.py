#!/usr/bin/python
from tkinter import *
from PIL import Image, ImageDraw, ImageTk, ImageFont
import threading
import mythread


# =========================================================


class MyGUI():

    def __init__(self):

        self.window = Tk()
        self.window.title("Vonage QA - Raz is the king")
        self.window.geometry('350x200')
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        '''
        image = Image.open("bg.jpg")
        photo = ImageTk.PhotoImage(image)
        
        #image = ImageTk.PhotoImage(Image.open("bg.jpg"))
        width =  photo.width()
        height = photo.height()

        self.window.resizable(width=False, height=False)
        self.window.geometry("%sx%s" % (width, height))
        # draw = ImageDraw.Draw(image)

        #photoimage = ImageTk.PhotoImage(image)
        label = Label(self.window, image=photo)
        label.place(x=0, y=0)
        # label.image = photo  # keep a reference!
        label.pack()

        #entry_pady = 7
        # Entry(self.window, background="white").place(x=text_x, y=text_y + height_text + entry_pady)


        #self.C = Canvas(self.window, bg="white", height=200, width=300)
        #filename = ImageTk.PhotoImage(Image.open("bg.png"))
        #background_label = Label(self.window, image=filename)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #self.C.create_image(20, 20, anchor=NW, image=filename)
        '''
        self.lbl_disconnect = Label(self.window, text="Disconnect Every")
        self.lbl_disconnect.grid(column=0, row=0)

        self.disconnect = Entry(self.window, width=10)
        self.disconnect.grid(column=1, row=0)

        self.lbl_sec = Label(self.window, text="sec")
        self.lbl_sec.grid(column=2, row=0)

        self.lbl_offline = Label(self.window, text="Stay offline for")
        self.lbl_offline.grid(column=0, row=1)

        self.offline = Entry(self.window, width=10)
        self.offline.grid(column=1, row=1)

        self.lbl_sec_offline = Label(self.window, text="sec")
        self.lbl_sec_offline.grid(column=2, row=1)

        self.lbl_status = Label(self.window, text="Connected")
        self.lbl_status.grid(column=1, row=2)

        self.btn = Button(self.window, text="Lets Go", command=self.clicked)
        self.btn.grid(column=2, row=3)
        
  
        self.stopFlag = None
        self.myThread = None

    # =========================================================
    def run(self):

        self.window.mainloop()

    # =========================================================

    def close_window(self):
        self.stop()
        # self.window.winfo_exists()
        self.window.destroy()

    # =========================================================

    def stop(self):
        if self.myThread is None:
            return
        self.stopFlag.set()
        self.myThread.do_connect()
        self.myThread = None
        self.stopFlag = None

    # =========================================================

    def start(self):
        disconnect_interval = int(self.disconnect.get())
        offline_time = int(self.offline.get())

        self.stopFlag = threading.Event()
        self.myThread = mythread.MyThread(self.stopFlag,self)
        self.myThread.start()

        self.myThread.set(disconnect_interval, offline_time)



    # =========================================================
    def clicked(self):
        if self.myThread is None:
            self.start()
            self.btn["text"] = "Stop"
        else:
            self.stop()
            self.btn["text"] = "Start"

    # =========================================================
    def update(self,status):
        self.lbl_status["text"] = status