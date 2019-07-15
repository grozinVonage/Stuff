#!/usr/bin/python
import os
import threading
import time

# =========================================================


class MyThread(threading.Thread):

    def __init__(self, event):
        threading.Thread.__init__(self)

        self.stop_event = event
        self.disconnect_interval = 0
        self.offline_time = 0
        self.stopped = False
        self.daemon = True

    # =========================================================
    def set(self, _disconnect_interval, _offline_time ):
        self.disconnect_interval = int(_disconnect_interval)
        self.offline_time = int(_offline_time)

    # =========================================================
    def stop(self):
        self.stopped = True
        self._stop()

    # =========================================================
    def run(self):
        while not self.stop_event.wait(self.disconnect_interval):
            print("my thread")
            self.do_disconnect()
            time.sleep(self.offline_time)
            self.do_connect()

    # =========================================================
    def do_connect(self):
        os.system("networksetup -setairportpower airport on")
        print("Connected : %s" % time.ctime())

    # =========================================================
    def do_disconnect(self):
        os.system("networksetup -setairportpower airport off")
        print("Disconnected : %s" % time.ctime())

