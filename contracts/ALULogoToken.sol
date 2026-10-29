// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// ALUT tokens represent shares of the ALU logo.
contract ALULogoToken is ERC20, Ownable {
    /// The supply is fixed at 1,000,000 tokens.
    uint256 public constant TOTAL_SUPPLY = 1_000_000;

    /// Emitted when the owner sends shares to someone.
    event SharesDistributed(address indexed from, address indexed to, uint256 amount);

    /// The owner gets the full supply when the contract is deployed.
    constructor(address logoOwner)
        ERC20("ALU Logo Token", "ALUT")
        Ownable(logoOwner)
    {
        // Mint all tokens once. There is no function to create more later.
        _mint(logoOwner, TOTAL_SUPPLY);
    }

    // Use whole tokens so the share amounts are easier to read.
    function decimals() public pure override returns (uint8) {
        return 0;
    }

    /// The owner can send shares to another wallet.
    function distributeShares(address recipient, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");

        // This reverts if the address is invalid or the owner lacks tokens.
        _transfer(owner(), recipient, amount);

        emit SharesDistributed(owner(), recipient, amount);
    }

    /// Returns the wallet's percentage of the total supply, rounded down.
    function ownershipPercentage(address account) external view returns (uint256) {
        return (balanceOf(account) * 100) / totalSupply();
    }
}
