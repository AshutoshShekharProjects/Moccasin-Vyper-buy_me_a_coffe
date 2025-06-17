# pragma version 0.4.1
"""
@ license: MIT
@ auther: You!
@ title: buy me a coffee
@ notice: This contract is for creating simple funding contract
"""

#interface AggregatorV3Interface:
    #def decimal()->uint8: view 
    #def description()->String[1000]: view 
    #def version()->uint256: view 
    #def latestAnswer()->int256: view


from interfaces import AggregatorV3Interface
import get_price_module as gp

# Constants and immutables
MIN_USD: public(constant(uint256))=as_wei_value(5,"ether")
PRICE_FEED: public(immutable(AggregatorV3Interface)) #0x694AA1769357215DE4FAC081bf1f309aDC325306
# a variable declared as immutable needs to be initialised in the constructor otherwise contract wont compile,
# it is same as constant, except constans need to be initialized as they are defined not later 
OWNER: public(immutable(address))

# State/Storage variables
funders: public(DynArray[address,1000])
funder_to_amount_funded: public(HashMap[address, uint256])


@deploy
def __init__(price_feed_address: address):
    PRICE_FEED= AggregatorV3Interface(price_feed_address)
    # as owner is declared immutable it does not require it to be accessed using self
    OWNER=msg.sender

@external 
@payable
def fund():
    self._fund()

@internal 
@payable
def _fund():
    usd_value_of_eth: uint256= gp._get_eth_to_usd_rate(PRICE_FEED, msg.value)
    assert usd_value_of_eth >= MIN_USD , "You must send more ETH!" # as_wei_value(1,"ether") i.e. 1000000000000000000
    # mapping funders who funded
    self.funders.append(msg.sender)
    # mapping the amount of eth funded by each funder
    self.funder_to_amount_funded[msg.sender]+= msg.value

@external 
def withdraw():
    assert msg.sender == OWNER, "Only the contract owner can withdraw."
    #send(OWNER, self.balance)
    raw_call(OWNER, b"", value= self.balance) # better and safer way to send money
    # reset the funders list and map
    for funder: address in self.funders:
        self.funder_to_amount_funded[funder]=0
    self.funders= []


@external 
@view 
def get_eth_to_usd_rate(eth_amount: uint256)-> uint256:
    return gp._get_eth_to_usd_rate(PRICE_FEED, eth_amount)


@external 
@view
def get_price()-> int256:
    #price_feed: AggregatorV3Interface = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306)
    return staticcall PRICE_FEED.latestAnswer()

@external 
@payable 
def __default__():
    self._fund()