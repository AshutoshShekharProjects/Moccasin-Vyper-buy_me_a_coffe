from moccasin.config import get_active_network


def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named("buy_me_a_coffee") # it checks moccasin.toml contact name coffee and then checks if mentioned contract is deployed in db
    print(f"Working with contract {coffee.address}")
    print(f"On network {active_network.name}, withdrawing from {coffee.address}")
    coffee.withdraw()

def moccasin_main():
    return withdraw()