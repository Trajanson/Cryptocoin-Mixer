Assumptions:
  - no big decimal class
  - only integers
# Cryptocoin-Mixer

To Run Tests:
`$ make test`


`$ source activate CryptocoinMixer`

https://speakerdeck.com/mitsuhiko/advanced-flask-patterns-1

https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html



TODO:
- add watched inputs to redis



- Transaction Engine
- Formula for transactions
- Formula for determining charges
- Formula for adding nodes to ecosystem

- When client deposits money, create a new node that sucks all the money in at once, set as compromised


- Client input cannot be client output address



- increase likelihood of transaction based on charge





```
import threading


def printit():
    threading.Timer(5.0, printit).start()
    print("Hello, World!")


printit()
```


```
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
timer.stop()
```
