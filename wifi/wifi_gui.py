#!/usr/bin/python
from tkinter import *
import os.path
import threading

import sys
import mythread

# =========================================================

stopFlag = None
myThread = None


# =========================================================

def close_window():
    stop()
    window.winfo_exists()
    sys.exit()


# =========================================================

def stop():
    global stopFlag
    stopFlag.set()
    myThread.stopped = True
    myThread.do_connect()


# =========================================================


def run(disconnect_interval, offline_time):
    global myThread
    global stopFlag

    stopFlag = threading.Event()
    myThread = mythread.MyThread(stopFlag)

    myThread.set(disconnect_interval, offline_time)
    myThread.start()


# =========================================================
def clicked():
    print('click')
    disconnect_interval = int(disconnect.get())
    offline_time = int(offline.get())
    run(disconnect_interval, offline_time)


# =========================================================

if __name__ == '__main__':
    window = Tk()
    window.title("Vonage QA - Raz is the king")
    window.geometry('350x200')
    window.protocol("WM_DELETE_WINDOW", close_window)

    lbl_disconnect = Label(window, text="Disconnect Every")
    lbl_disconnect.grid(column=0, row=0)

    disconnect = Entry(window, width=10)
    disconnect.grid(column=1, row=0)

    lbl_sec = Label(window, text="sec")
    lbl_sec.grid(column=2, row=0)

    lbl_offline = Label(window, text="Stay offline for")
    lbl_offline.grid(column=0, row=1)

    offline = Entry(window, width=10)
    offline.grid(column=1, row=1)

    lbl_sec_offline = Label(window, text="sec")
    lbl_sec_offline.grid(column=2, row=1)

    btn = Button(window, text="Lets Go", command=clicked)
    btn.grid(column=1, row=2)

    window.mainloop()

# ===========================================================
