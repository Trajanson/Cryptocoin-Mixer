# [Cryptocoin Mixer][cryptocoinMixer]
[![Build Status](https://travis-ci.org/Trajanson/Cryptocoin-Mixer.svg?branch=master)](https://travis-ci.org/Trajanson/Cryptocoin-Mixer)
## By [Julian Theoderik Trajanson][trajanson]

A Cryptocoin Mixer is a tool used to obscure history and ownership of cryptocoin accounts. This function carries particular utility in the Bitcoin community, where all transactions are fully visible in a public ledger.

## Use Case

The lack of account privacy in some cryptocurrencies could be undermining to potential adopters who are resultantly deterred from using the currencies. Users similarly would like to maintain anonymity from antagonists and to secure privacy in their personal transactions. These concerns are remedied by the use of a properly functioning Cryptocoin Mixer.

To use a Mixer, users submit their coins into the black-box process of the Mixer and have their coins arrive untraceably into a number (preferably more than one) of uncompromised accounts identified by the user. This Cryptocin Mixer is one such implementation of the black-box mixing process.

## Strategy

The theme of this Cryptocoin Mixer is **obfuscation and deception**.

#### Naive Approach: Linear Path Ping

###### Description:
In this approach, transactions can be mapped to a DAG (directed acyclic graph). Transactions flow in one direction from the input address, through layers of nodes in the Mixer and ultimately to the output address.

###### Deficiencies:
Antagonists can use the service to discover the input and output addresses and, by following the DAG, discover the other addresses within the hidden layers. Any addresses that immediately receive coins from a compromised address are known to have used the service. Temporal analysis can also be indicative of where coins from the input node 'disappeared to'.

#### Intermediate Approach: The Tumbler
> ***This is the approach taken by this Mixer.***

###### Description:
In this approach, transactions flow through the Mixer in stochastic "mean-reverting random-walk" patterns which contain cycles. To combat antagonists who would use the system to discover addresses within the system, compromised addresses are identified and phased out as new addresses are phased in. Coins taken into the system are not permitted to flow in a straight line to an output address. The addresses within the Mixer form an ecosystem that is intended to mirror the appearance of transactions in the external system.

An iterative improvement on this design may be to have multiple Tumbler eco-systems that rotate among input and output nodes. This would be roughly similar to the conduct of Casinos that rotate multiple decks of playing cards to diminish the threat of card counters.

A further iterative improvement on this design would be to incorporate behavioral analysis of addresses outside the Mixer. The aim here would be to outsmart trained binary classifiers models which may be able to identify addresses within the Mixer vs. external addresses used by humans. At a level of low complexity, this might involve adjusting the frequency and size of transactions; at a level of high complexity in combatting gradient boosted decision trees or deep learning models this may involve manipulating the subtle interactions of various parameters.


###### Deficiencies:
Advanced analysis may be able to identify the behavioral characteristics that differentiate addresses within the Mixer eco-system from human addresses in the external system. Moreover, network analysis may indicate that compromised addresses within the eco-system have interacted more heavily with other addresses (within the eco-system). With knowledge of which nodes belong to the Mixer, temporal analysis can be used to narrow identification of deposits that match withdrawals from the input address.

A significant disadvantage of this approach is the cost of capital tied up in the Tumbler. Akin, to storing money under a mattress, storing currency in the Mixer incurs a steep opportunity cost. Moreover, many cryptocurrencies have historically high volatilities in their relation to the US Dollar. Therefore, investments in the Mixer would have to be considered more similarly in comparison to high-beta investments than to low-risk, low-yield financial instruments.


#### Advanced Approach: Cryptofutures Exchange

###### Description:
In this approach, many users maintain permanent accounts with the Mixer, thus negating the risk of temporal analysis of deposits and withdrawals.

Users who choose to maintain an account with the Mixer reserve a private account identity with the Mixer that is known only to the user and the Mixer. Through this private identity, the Mixer can regularly rotate new addresses to the user, who stores the majority of his or her wealth not in a private cryptocoin address but within the single address of the Mixer. In the extreme, the Mixer can create and deposit coins into new single-use cryptocoin addresses for every individual user transaction.

The Mixer, which now operates more in the manner of a bank, productively allocates the capital wealth stored within its address. The evolution in branding and context extirpates the need for users to hide that cryptocoins have passed through the Mixer.

Active participation in the Cryptocoin spot and futures markets hedges the Mixer against the volatility of US Dollar-Cryptocurrency exchange rates. [Read more about spot–future parity](https://en.wikipedia.org/wiki/Spot%E2%80%93future_parity).



###### Deficiencies:
This approach requires substantial liquidity to maintain low transactional costs. Furthermore, significant institutional trust is required to attain client confidence in the Mixer and in the Mixer's ability and desire to preserve the confidentiality of its user's data.



## Setup
###  Install Docker
- [For Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac?tab=description)
- [For Ubuntu](https://store.docker.com/editions/community/docker-ce-server-ubuntu)
- [For Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows?tab=description)

###  Run
1. `$ make build-docker`
2. `$ make run-docker`

###  Run Tests
*Monte Carlo Simulation parameters are configurable from within the `monte_carlo_simulation.py` script.*

1. `$ make test`
2. `$ make run-monte-carlo-simulations`




[trajanson]: http://trajanson.com/
[cryptocoinMixer]: http://ec2-34-229-88-203.compute-1.amazonaws.com/
