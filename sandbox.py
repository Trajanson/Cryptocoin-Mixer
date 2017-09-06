# import threading
#
# num = 7
#
#
# def printit(num):
#     threading.Timer(2.0, printit).start(num)
#     print(num)
#
#
# printit(num)

import time
from threading import Event, Thread


class RepeatedTimer(object):

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()


# start timer
timer = RepeatedTimer(2, print, 'Hello world')

# stop timer
time.sleep(10)
print("WOKE UP")
timer.stop()
