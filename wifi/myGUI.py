#!/usr/bin/python
from tkinter import *
import threading
import mythread


# =========================================================


class MyGUI():

    def __init__(self):
        self.window = Tk()
        self.window.title("Vonage QA - Raz is the king")
        self.window.geometry('350x200')
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

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

        self.btn = Button(self.window, text="Lets Go", command=self.clicked)
        self.btn.grid(column=1, row=2)

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
        if self.myThread == None:
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
        self.myThread = mythread.MyThread(self.stopFlag)
        self.myThread.start()

        self.myThread.set(disconnect_interval, offline_time)



    # =========================================================
    def clicked(self):

        if self.myThread == None:
            self.start()
            self.btn["text"] = "Stop"
        else:
            self.stop()
            self.btn["text"] = "Start"
