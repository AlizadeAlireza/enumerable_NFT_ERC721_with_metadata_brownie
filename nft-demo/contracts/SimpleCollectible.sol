// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // take no input parameters
    // get name and symbol
    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    //this will create a new nft and assign it to whoever called this function
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI); // allow our nft have an img
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
