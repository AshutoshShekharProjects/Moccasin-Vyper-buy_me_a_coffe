from eth_utils import to_wei
import boa
from tests.conftest import SEND_AMOUNT


RANDOM_USER = boa.env.generate_address("non_owner")

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address
    
def test_starting_value(coffee, account):
    assert coffee.MIN_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must send more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_AMOUNT)
    # Act
    coffee.fund(value=SEND_AMOUNT)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_AMOUNT
    
def test_non_owner_cannot_withdraw(coffee_funded, account):
    with boa.env.prank(RANDOM_USER): # Use a random user to simulate non-owner
        with boa.reverts("Only the contract owner can withdraw."):
            coffee_funded.withdraw()  
            
def test_owner_can_withdraw(coffee_funded):
    with boa.env.prank(coffee_funded.OWNER()): # Simulate owner
        coffee_funded.withdraw()
    # Assert
    #assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(coffee_funded.OWNER()) == SEND_AMOUNT
    #assert coffee.address == coffee.OWNER()
    
def test_fund_with_different_accounts(coffee):
    # Arrange
    sm=0
    users = [boa.env.generate_address("non_owner") for i in range(10)]
    for i in range(10):
        boa.env.set_balance(users[i], SEND_AMOUNT)
        with boa.env.prank(users[i]):
            coffee.fund(value=SEND_AMOUNT)
            sm+= SEND_AMOUNT
    # Act
    #sm = sum(boa.env.get_balance(coffee.address))
    boa.env.set_balance(coffee.OWNER(), 0)
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()
    # Assert
    #assert boa.env.get_balance(coffee.OWNER()) == SEND_AMOUNT * 10
    assert boa.env.get_balance(coffee.OWNER()) == sm
    
def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_AMOUNT) > 0
    
        