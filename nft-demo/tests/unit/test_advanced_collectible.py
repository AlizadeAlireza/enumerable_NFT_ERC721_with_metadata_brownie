import pytest
from brownie import network, AdvancedCollectible, convert, chain, accounts
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # act
    # we can use it to get our events
    advanced_collectible, creation_transaction = deploy_and_create()

    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    # add the name of our event here
    # witch is requested collectible

    # we also should technically be able to get the breed and figure out
    # the breed of this first token of first collectible
    random_number = 777
    # we've coded our get_contract() in a way that if the mock has already
    # been deployed
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # assert
    # check to see that the token counter has been increased
    assert advanced_collectible.tokenCounter() == 1
    # correct token counter be at least 1

    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
