// an NFT contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    // how many breeds we can get
    enum Breed {
        PUG,
        SHIBA_INU,
        BERNARD
    } //1, 2, 3
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _VRFCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_VRFCoordinator, _linkToken)
        ERC721("Dogie", "DOG") // can be parameter
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = _fee;
    }

    // where we're going this token uri from and
    // create ourselve
    function createCollectible() public returns (bytes32) {
        // we want the user who called collectible to be sane user
        // who gets assignd the token id
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        // this is going to take the requestId as a key
        // then whoever sent it as the value and create this at the top

        emit requestedCollectible(requestId, msg.sender);
    }

    // override ---> only the vrf coordinator can call this
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        // we need to assign this breed to its token id ---> create a mapping
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId]; // who is sender the NFT
        _safeMint(owner, newTokenId); // msg here is always be the VRFCoordinator
        // the VRFCoordinator is actually the one calling this fullfillrandomness
        // who is the original callere of the createCollectible? ---> with another mapping
        // _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // need 3 tokenURI for those 3 dogs ---> pug, shiba inu, st bernard
        // that only the owner of the token id can actually be the one to update
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        // imported openZeppelin
        // _isA... cheks the owner of the ERC721 of that tokenId
        _setTokenURI(tokenId, _tokenURI);
    }
}
