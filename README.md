# Cryptocoin Mixer
## By [Julian Theoderik Trajanson][trajanson]

A Cryptocoin Mixer is a tool used to obscure history and ownership of cryptocoin accounts. This function carries particular utility in the Bitcoin community, where all transactions are fully visible in a public ledger.

## Use Case

In its most extreme depiction, the lack of account privacy in some cryptocurrencies could be undermining to potential high-profile adopters who are otherwise deterred from using the currencies. Less conspicuous users similarly would like to maintain anonymity from antagonists and privacy in their personal transactions. These concerns are remedied by the use of a properly functioning Cryptocoin Mixer.

To use a Mixer, users submit their coins into the black-box process of the Mixer and have their coins arrive untraceably into a number of uncompromised accounts (preferably more than one) identified by the user. This Cryptocin Mixer is one such implementation of the black-box.

## Strategy

The theme of this Cryptocoin Mixer is **obfuscation and deception**.

#### Naive Approach: Linear Path Ping

###### Description:
In this approach, transactions can be mapped to a DAG (directed acyclic graph). Transactions flow in one direction from the input address, through layers of nodes in the Mixer and ultimately to the output address.

###### Deficiencies:
Antagonists can use the service to discover the input and output addresses and by following the DAG, discover the other addresses within the hidden layers. Any addresses that immediately receive coins from a compromised address are known to have used the service. Temporal analysis can also be indicative of where coins from the input node 'disappeared to'.

#### Intermediate Approach: The Tumbler

###### Description:
In this approach, transactions flow through the Mixer in stochastic patterns which contain cycles. To combat antagonists who would use the system to discover addresses within the system, compromised addresses are identified and phased out as new addresses are phased in. Coins taken into the system are not permitted to flow in a straight line to an output address. The addresses within the Mixer form an ecosystem that is intended to mirror the appearance of transaction in the external system. This is the approach taken by this Mixer.

An iterative improvement on this design may be to have multiple Tumbler eco-systems that rotate among input and output nodes. This would be roughly similar to the conduct of Casinos that rotate multiple decks of playing cards to diminish the threat of card counters.

###### Deficiencies:
Advanced analysis may be able to identify the behavioral characteristics that differentiate addresses within the Mixer eco-system from human addresses in the external system. Moreover, network analysis may indicate that compromised addresses within the eco-system have interacted more heavily with other addresses (within the eco-system). With knowledge of which nodes belong to the Mixer, temporal analysis can be used to narrow identification of deposits that match withdrawals from the input address.

A significant disadvantage of this approach is the cost of capital tied up in the Tumbler. Akin, to storing money under a mattress,


#### Advanced Approach: Cryptofutures Exchange


Antagonists can use the service to discover the input and output addresses and by following the DAG, discover the other addresses within the hidden layers. Temporal analysis can also be indicative of where coins from the input node 'disappeared to'.


heat map


demonstration of a number of technologies in the Python [Flask][flask] ecosystem deployed via use of [Virtualenv][virtualenv], [Gunicorn][gunicorn], [Heroku][heroku], [Travis CI][travis], [Docker][docker], and Flask's native [Werkzeug testing client][werkzeug].




Assumptions:
  - no big decimal class
  - only integers
# Cryptocoin-Mixer

To Run Tests:
`$ make test`


# docker build -t cyrptocoin_mixer .
# docker run -it cyrptocoin_mixer ./docker-entrypoint.sh


`$ source activate CryptocoinMixer`

https://speakerdeck.com/mitsuhiko/advanced-flask-patterns-1

https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html


## Key Features
- a
- b
- c


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








## Problems with implementation
- Database is out of sync with reality
  - if someone randomly adds value to a node it will still drop out of the system



[trajanson]: http://trajanson.com/
