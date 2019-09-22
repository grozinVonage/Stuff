#!/usr/bin/python
import os
import time
import threading
import eventDispatcher

global exitFlag


# =========================================================


class NetworkHandler(threading.Thread):

    def __init__(self, threadName, event_dispatcher):
        threading.Thread.__init__(self)
        self.name = threadName
        # Save a reference to the event dispatch
        self.event_dispatcher = event_dispatcher
        self.connect_interval = 0
        self.disconnect_interval = 0
        self.state = threading.Condition()
        self.paused = True  # Start out paused.
        self.stop_thread = False

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
    def stop(self):
        with self.state:
            self.stop_thread = True
            self.state.notify()  # Unblock self if waiting.


    # =========================================================
    def set_intervals(self, online_interval, offline_interval):
        self.connect_interval = online_interval
        self.disconnect_interval = offline_interval

    # =========================================================
    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.connect()
                    self.update_ui(eventDispatcher.MyEvent.CONNECTED)
                    self.state.wait()  # Block execution until notified.
                if self.stop_thread:
                    self.connect()
                    exit(0)
            self.do_connect(self.connect_interval)
            self.do_disconnect(self.disconnect_interval)

    # =========================================================
    def connect(self):
        print("Connect stared : %s" % time.ctime())
        os.system("networksetup -setairportpower airport on")
        print("Connected : %s" % time.ctime())

    # =========================================================
    def disconnect(self):
        print("disconnect Stared : %s" % time.ctime())
        os.system("networksetup -setairportpower airport off")
        print("Disconnected : %s" % time.ctime())
    # =========================================================

    def do_connect(self, online_interval):
        self.connect()
        self.update_ui(eventDispatcher.MyEvent.CONNECTED)
        time.sleep(self.connect_interval)
        self.update_ui(eventDispatcher.MyEvent.DONE_CONNECTED)

    # =========================================================

    def do_disconnect(self, offline_interval):
        self.disconnect()
        self.update_ui(eventDispatcher.MyEvent.DISCONNECTED)
        time.sleep(self.disconnect_interval)
        self.update_ui(eventDispatcher.MyEvent.DONE_DISCONNECTED)

    # =========================================================
    def update_ui(self, event):
        self.event_dispatcher.dispatch_event(
            eventDispatcher.MyEvent(event, self))

    # =========================================================
