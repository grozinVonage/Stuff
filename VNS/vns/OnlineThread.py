#!/usr/bin/python
import os
import threading
import time
import vns.eventDispatcher


# =========================================================


class OnlineThread(threading.Thread):

    def __init__(self, event_dispatcher):
        threading.Thread.__init__(self)

        self.online_interval = 0
        self.daemon = False
        # Save a reference to the event dispatch
        self.event_dispatcher = event_dispatcher

    # =========================================================

    def run(self, _online_interval):
        print("Stared : %s" % time.ctime())
        self.online_interval = int(_online_interval)
        self.do_connect()
        time.sleep(self.online_interval)
        self.update_ui()

    # =========================================================
    def do_connect(self):
        os.system("networksetup -setairportpower airport on")
        print("Connected : %s" % time.ctime())

    # =========================================================
    def update_ui(self):
        self.event_dispatcher.dispatch_event(
            vns.eventDispatcher.MyEvent(vns.eventDispatcher.MyEvent.CONNECTED, self))