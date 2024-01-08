// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/metatx/ERC2771Context.sol";
import "@openzeppelin/contracts/metatx/MinimalForwarder.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TransferToken is ERC2771Context {
    constructor(
        MinimalForwarder forwarder // Initialize trusted forwarder
    ) ERC2771Context(address(forwarder)) {}

    function approve(address token, address to, uint256 amount) public virtual {
        ERC20 tokenContract = ERC20(token);
        // Approve the tokens
        require(
            tokenContract.approve(to, amount),
            "TransferToken: approve failed"
        );
    }

    function transfer(address token, address to, uint256 amount) external {
        ERC20 tokenContract = ERC20(token);
        // Transfer the tokens
        require(
            tokenContract.transferFrom(_msgSender(), to, amount),
            "TransferToken: transfer failed"
        );
    }
}

// require(
//     _msgSender() == address(this),
//     "TransferToken: only this contract can call this function"
// );
