#!/usr/bin/python
import os
import time
#import wx
import webview
import threading
# =========================================================


def do_connect():
    os.system("networksetup -setairportpower airport on")
    print("Connected : %s" % time.ctime())


# =========================================================


def do_disconnect():
    os.system("networksetup -setairportpower airport off")
    print("Disconnected : %s" % time.ctime())


# =========================================================
def change_url():
    # wait a few seconds before changing url:
    time.sleep(10)

    # change url:
    webview.load_url("https://pywebview.flowrl.com/hello")
    do_disconnect()
    print('=====================')
    time.sleep(5)
    do_connect()

# =========================================================


if __name__ == "__main__":
    do_connect()
    t = threading.Thread(target=change_url)
    t.start()

    webview.create_window("URL Change Example", "http://www.google.com")
    # create an application object.
    #app = wx.App()
    # Then a frame.
    #frm = wx.Frame(None, title="Vonage Network switch")
    # Show it.
    #frm.Show()
    #app.MainLoop()

