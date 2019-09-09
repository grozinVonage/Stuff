#!/usr/bin/python
from tkinter import *
import tkinter as tk
import os

import vns.onlineThread
import vns.offlineThread
import vns.eventDispatcher
import vns.networkHandler

# =========================================================


class MyGUI():

    def __init__(self):

        self.window = Tk()
        self.window.title("Vonage QA - Raz is the king")
        self.window.geometry('400x300')
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


        self.btn = Button(self.window, text="Lets Go", command=self.clicked)
        self.btn.grid(column=1, row=2)

        current_path = os.getcwd()
        self.on_file_name = current_path + "/vns/wifi.gif"
        self.wifi_on = tk.PhotoImage(file=self.on_file_name)
        self.off_file_name = current_path + "/vns/wifi_off.gif"
        self.wifi_off = tk.PhotoImage(file=self.off_file_name)
        self.wifi_lable = Label(self.window, compound=tk.LEFT, text="", image=self.wifi_on)
        self.wifi_lable.grid(column=1, row=3)


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
        self.window.mainloop()

    # =========================================================

    def close_window(self):
        #self.stop()
        self.networkHandler.stop()
        # self.window.winfo_exists()
        self.window.destroy()

    # =========================================================

    def stop(self):
        self.stoped = True
        self.networkHandler.pause()

    # =========================================================

    def start(self):

        self.stoped = False
        online_interval = int(self.online.get())
        offline_interval = int(self.offline.get())
        self.networkHandler.set_intervals(online_interval, offline_interval)
        self.networkHandler.resume()

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
            self.wifi_lable.configure(image=self.wifi_on)
            self.wifi_lable.image = self.wifi_on

        if event.type == vns.eventDispatcher.MyEvent.DISCONNECTED:
            self.wifi_lable.configure(image=self.wifi_off)
            self.wifi_lable.image = self.wifi_off

    # =========================================================