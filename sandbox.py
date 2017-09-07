import time
import threading

class Test(object):
    def __init__(self):
        self.num = 0

    def test(self):
        duration = 2

        if self.num < 5:
            self.num += 1
            print("NUM IS", self.num)
            threading.Timer(duration, self.test).start()
        else:
            print("OVER!!!!!!!")

Test().test()
#
# def test(self):
#     epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH
#
#     if self.is_waiting_at_barrier is True:
#         self.transaction_engine_is_halted = True
#     else:
#         threading.Timer(epoch_length,
#                         self.test).start()
#
#         self.mix_service.transaction_engine.execute_pending_transactions()




# # -*- coding: utf-8 -*-
#
# # import threading
# #
# # num = 7
# #
# #
# # def printit(num):
# #     threading.Timer(2.0, printit).start(num)
# #     print(num)
# #
# #
# # printit(num)
#
# import time
# from threading import Event, Thread
#
#
# class RepeatedTimer(object):
#
#     """Repeat `function` every `interval` seconds."""
#
#     def __init__(self, interval, function, *args, **kwargs):
#         self.interval = interval
#         self.function = function
#         self.args = args
#         self.kwargs = kwargs
#         self.start = time.time()
#         self.event = Event()
#         self.thread = Thread(target=self._target)
#         self.thread.start()
#
#     def _target(self):
#         while not self.event.wait(self._time):
#             self.function(*self.args, **self.kwargs)
#
#     @property
#     def _time(self):
#         return self.interval - ((time.time() - self.start) % self.interval)
#
#     def stop(self):
#         self.event.set()
#         self.thread.join()
#
#
# # start timer
# timer = RepeatedTimer(2, print, 'Hello world')
#
# # stop timer
# time.sleep(10)
# print("WOKE UP")
# timer.stop()
