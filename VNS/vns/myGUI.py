#!/usr/bin/python
from tkinter import *
import threading

import vns.onlineThread
import vns.offlineThread
import vns.eventDispatcher
import vns.networkHandler

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
        self.event_dispatcher.add_event_listener(vns.eventDispatcher.MyEvent.CONNECTED, self.update)
        self.event_dispatcher.add_event_listener(vns.eventDispatcher.MyEvent.DISCONNECTED, self.update)
        self.event_dispatcher.add_event_listener(vns.eventDispatcher.MyEvent.DONE_CONNECTED, self.update)
        self.event_dispatcher.add_event_listener(vns.eventDispatcher.MyEvent.DONE_DISCONNECTED, self.update)

        self.networkHandler = vns.networkHandler.NetworkHandler("NetworkHandlerThread",self.event_dispatcher)
        self.stoped = True

    # =========================================================
    def run(self):
        self.networkHandler.start()
        # self.networkHandler.join(1)
        self.window.mainloop()

    # =========================================================

    def close_window(self):
        self.stop()
        # self.window.winfo_exists()
        self.window.destroy()

    # =========================================================

    def stop(self):
        self.stoped = True
        #self.stopEvent.set()
        self.networkHandler.pause()

    # =========================================================

    def start(self):

        self.stoped = False
        online_interval = int(self.online.get())
        offline_interval = int(self.offline.get())
        #self.stopEvent = threading.Event()
        self.networkHandler.setIntervals(online_interval, offline_interval)
        #self.networkHandler.setStopEvent(self.stopEvent)

        #self.onlineTherad.run(online_interval)
        self.networkHandler.resume()
        #threading.thread.start_new_thread( self.networkHandler.do_connect(online_interval,))

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

        if event.type == vns.eventDispatcher.MyEvent.CONNECTED:
            self.lbl_status = "Connected"

        if event.type == vns.eventDispatcher.MyEvent.DISCONNECTED:
            self.lbl_status = "Disconnected"

        #if event.type == vns.eventDispatcher.MyEvent.DONE_CONNECTED:
        #    threading.thread.start_new_thread(self.networkHandler.do_disconnect(offline_interval, ))

        #if event.type == vns.eventDispatcher.MyEvent.DONE_DISCONNECTED:
        #    threading.thread.start_new_thread(self.networkHandler.do_connect(online_interval, ))
    # =========================================================