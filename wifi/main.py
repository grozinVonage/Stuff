#!/usr/bin/python
import os
import time


# =========================================================


def do_connect():
    os.system("networksetup -setairportpower airport on")
    print("Connected : %s" % time.ctime())


# =========================================================


def do_disconnect():
    os.system("networksetup -setairportpower airport off")
    print("Disconnected : %s" % time.ctime())


# =========================================================


if __name__ == "__main__":
    do_connect()
    while (True):
        do_disconnect()
        print('=====================')
        time.sleep(5)
        do_connect()
        time.sleep(10)
