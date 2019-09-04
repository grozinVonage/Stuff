#!/usr/bin/python
from tkinter import *
import threading

import vns.onlinetTread
import vns.offlineThread
import vns.eventDispatcher

# =========================================================


class MyGUI():

    def __init__(self):

        self.window = Tk()
        self.window.title("Vonage QA - Raz is the king")
        self.window.geometry('350x200')
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.lbl_disconnect = Label(self.window, text="Stay online for")
        self.lbl_disconnect.grid(column=0, row=0)

        self.online = Entry(self.window, width=10)
        self.online.grid(column=1, row=0)

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

        # Create and instance of event dispatcher
        # Save event dispatcher reference
        self.event_dispatcher = vns.eventDispatcher.EventDispatcher()

        # Listen for CONNECT & DISCONNECT event type
        self.event_dispatcher.add_event_listener(vns.MyEvent.CONNECTED, self.update)
        self.event_dispatcher.add_event_listener(vns.MyEvent.DISCONNECTED, self.update)

        self.stopFlag = None

        self.onlineTherad = None
        self.offlineTherad = None
        self.stoped = True

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
        self.stoped = True

    # =========================================================

    def start(self):
        self.stoped = False
        online_interval = int(self.online.get())
        offline_interval = int(self.offline.get())

        self.onlineTherad = vns.onlineThread.OnlineThread()
        self.offlineTherad = vns.offlineThread.OfflineThread()

        self.stopFlag = threading.Event()

        self.onlineTherad.run(online_interval)




    # =========================================================
    def clicked(self):
        if self.stoped:
            self.start()
            self.btn["text"] = "Stop"
        else:
            self.stop()
            self.btn["text"] = "Start"

    # =========================================================
    def update(self,event):
        online_interval = int(self.online.get())
        offline_interval = int(self.offline.get())
        if event.data == vns.MyEvent.CONNECTED:

        if event.data == vns.MyEvent.DONE_CONNECTED:
            self.onlineTherad.stop()
            self.offlineTherad.run(offline_interval)
        if event.data == vns.MyEvent.DONE_DISCONNECTED:
            self.offlineTherad.stop()
            self.onlineTherad.start(online_interval)
