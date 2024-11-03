// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/governance/utils/Snapshotting.sol";
import "@openzeppelin/contracts/utils/Address.sol";

contract AdvancedToken is ERC20, Ownable, Pausable {
    using SafeMath for uint256;
    using Address for address;

    // Fee percentage (in basis points, e.g., 100 = 1%)
    uint256 public transferFee = 100; // 1%
    address public feeRecipient;

    // Mapping for delegated voting
    mapping(address => address) public delegates;

    // Events
    event TransferFeeUpdated(uint256 newFee);
    event FeeRecipientUpdated(address newRecipient);
    event TokensLocked(address indexed account, uint256 amount, uint256 releaseTime);
    
    // Struct for locked tokens
    struct LockedToken {
        uint256 amount;
        uint256 releaseTime;
    }
    
    // Mapping for locked tokens
    mapping(address => LockedToken) public lockedTokens;

    constructor(uint256 initialSupply, address _feeRecipient) ERC20("AdvancedToken", "ATK") {
        _mint(msg.sender, initialSupply);
        feeRecipient = _feeRecipient;
    }

    // Override transfer functions to include fee
    function _transfer(address sender, address recipient, uint256 amount) internal override {
        require(!isLocked(sender), "Tokens are locked");
        
        uint256 fee = amount.mul(transferFee).div(10000);
        uint256 amountAfterFee = amount.sub(fee);
        
        super._transfer(sender, feeRecipient, fee); // Transfer fee to feeRecipient
        super._transfer(sender, recipient, amountAfterFee);
    }

    // Function to lock tokens
    function lockTokens(uint256 amount, uint256 duration) external {
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        require(lockedTokens[msg.sender].amount == 0, "Tokens already locked");

        lockedTokens[msg.sender] = LockedToken({
            amount: amount,
            releaseTime: block.timestamp + duration
        });

        _transfer(msg.sender, address(this), amount); // Transfer tokens to the contract
        emit TokensLocked(msg.sender, amount, lockedTokens[msg.sender].releaseTime);
    }

    // Function to unlock tokens
    function unlockTokens() external {
        require(isLocked(msg.sender), "No locked tokens");
        require(block.timestamp >= lockedTokens[msg.sender].releaseTime, "Tokens are still locked");

        uint256 amount = lockedTokens[msg.sender].amount;
        delete lockedTokens[msg.sender]; // Clear the locked tokens

        _transfer(address(this), msg.sender, amount); // Transfer tokens back to the user
    }

    // Check if tokens are locked
    function isLocked(address account) public view returns (bool) {
        return lockedTokens[account].amount > 0;
    }

    // Update transfer fee
    function updateTransferFee(uint256 newFee) external onlyOwner {
        require(newFee <= 1000, "Fee too high"); // Max 10%
        transferFee = newFee;
        emit TransferFeeUpdated(newFee);
    }

    // Update fee recipient
    function updateFeeRecipient(address newRecipient) external onlyOwner {
        feeRecipient = newRecipient;
        emit FeeRecipientUpdated(newRecipient);
    }

    // Delegate voting power
    function delegate(address to) external {
        require(to != msg.sender, "Cannot delegate to self");
        delegates[msg.sender] = to;
    }

    // Override snapshot functionality
    function snapshot() external onlyOwner {
        _snapshot();
    }
}
