#!/usr/bin/python
import os
import time
import threading
import vns.eventDispatcher

global exitFlag
# =========================================================


class NetworkHandler(threading.Thread):

    def __init__(self, threadName, event_dispatcher):
        threading.Thread.__init__(self)
        self.name = threadName
        # Save a reference to the event dispatch
        self.event_dispatcher = event_dispatcher
        # self.stopEvent = 0
        self.connect_interval = 0
        self.disconnect_interval = 0
        self.state = threading.Condition()
        self.paused = True  # Start out paused.


    # =========================================================

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    # =========================================================
    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    # =========================================================
    #def setStopEvent(self, stopEvent):
    #    self.stopEvent = stopEvent

    # =========================================================

    def setIntervals(self, online_interval, offline_interval):
        self.connect_interval = online_interval
        self.disconnect_interval= offline_interval

    # =========================================================
    def run(self):
        # self.resume()
        #while not self.stopEvent.isSet():
        while True:
            with self.state:
                if self.paused:
                    self.do_connect(self.connect_interval)
                    self.state.wait()  # Block execution until notified.
            self.do_connect(self.connect_interval)
            self.do_disconnect(self.disconnect_interval)


    # =========================================================

    def do_connect(self, online_interval):

        print("Connect stared : %s" % time.ctime())
        os.system("networksetup -setairportpower airport on")
        print("Connected : %s" % time.ctime())

        self.update_ui(vns.eventDispatcher.MyEvent.CONNECTED)
        time.sleep(self.connect_interval)
        self.update_ui(vns.eventDispatcher.MyEvent.DONE_CONNECTED)

    # =========================================================

    def do_disconnect(self,offline_interval):
        print("disconnect Stared : %s" % time.ctime())
        os.system("networksetup -setairportpower airport off")
        print("Disconnected : %s" % time.ctime())

        self.update_ui(vns.eventDispatcher.MyEvent.DISCONNECTED)
        time.sleep(self.disconnect_interval)
        self.update_ui(vns.eventDispatcher.MyEvent.DONE_DISCONNECTED)

    # =========================================================
    def update_ui(self,event):
        self.event_dispatcher.dispatch_event(
            vns.eventDispatcher.MyEvent(event, self))

    # =========================================================