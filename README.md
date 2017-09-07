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
In this approach, transactions flow through the Mixer in stochastic "mean-reverting random-walk" patterns which contain cycles. To combat antagonists who would use the system to discover addresses within the system, compromised addresses are identified and phased out as new addresses are phased in. Coins taken into the system are not permitted to flow in a straight line to an output address. The addresses within the Mixer form an ecosystem that is intended to mirror the appearance of transaction in the external system. This is the approach taken by this Mixer.

An iterative improvement on this design may be to have multiple Tumbler eco-systems that rotate among input and output nodes. This would be roughly similar to the conduct of Casinos that rotate multiple decks of playing cards to diminish the threat of card counters.

###### Deficiencies:
Advanced analysis may be able to identify the behavioral characteristics that differentiate addresses within the Mixer eco-system from human addresses in the external system. Moreover, network analysis may indicate that compromised addresses within the eco-system have interacted more heavily with other addresses (within the eco-system). With knowledge of which nodes belong to the Mixer, temporal analysis can be used to narrow identification of deposits that match withdrawals from the input address.

A significant disadvantage of this approach is the cost of capital tied up in the Tumbler. Akin, to storing money under a mattress, storing currency in the Mixer incurs a steep opportunity cost. Moreover, many cryptocurrencies have historically high volatilities in their relation to the US Dollar. Therefore, investments in the Mixer would have to be considered more similarly in comparison to high-beta investments than to low-risk, low-yield financial instruments.


#### Advanced Approach: Cryptofutures Exchange

###### Description:
In this approach, many users maintain permanent accounts with the Mixer, thus negating the risk of temporal analysis of deposits and withdrawals.

Users who choose to maintain an account with the Mixer reserve a private account identity with the Mixer that is known only to the user and the Mixer. Through this private identity, the Mixer can regularly rotate new addresses to the user, who stores the majority of his or her wealth not in a private cryptocoin address but within the single address of the Mixer.

The Mixer, which now operates more in the manner of a bank, productively allocates the capital wealth stored within its address. Active participation in the Cryptocoin spot and futures markets hedges the Mixer against the volatility of US Dollar-Cryptocurrency exchange rates. [Read more about spot–future parity](https://en.wikipedia.org/wiki/Spot%E2%80%93future_parity).



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
1. `$ make test`




[trajanson]: http://trajanson.com/
