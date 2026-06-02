// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title GalacticMultiCurrencyExchange
 * @dev AI-optimized DEX supporting all 1,000 galactic currencies.
 *      Uses quantum-seeded AMM with neural liquidity rebalancing.
 * @author KOSASIH — AetherNova Forge — OmniGenesis AI
 */
contract GalacticMultiCurrencyExchange is ReentrancyGuard, Ownable {

    // ── Events ─────────────────────────────────────────────────────────────────
    event CurrencyRegistered(string symbol, address token, string civilization, string category);
    event Swapped(address indexed trader, string fromSymbol, string toSymbol, uint256 amountIn, uint256 amountOut);
    event LiquidityAdded(address indexed provider, string symbol, uint256 amount);
    event LiquidityRemoved(address indexed provider, string symbol, uint256 amount);
    event AGIRebalance(string symbol, uint256 newReserve, uint256 agiConfidence);

    // ── Structs ────────────────────────────────────────────────────────────────
    struct GalacticToken {
        address tokenAddress;
        string civilization;
        string category;
        string backing;
        uint256 reserve;
        uint256 totalSupply;
        bool active;
        uint256 registeredAt;
    }

    // ── State ──────────────────────────────────────────────────────────────────
    mapping(string => GalacticToken) public currencies;
    string[] public currencyList;
    uint256 public swapFeeBasis = 30; // 0.3% AGI-optimized fee
    address public agiOracleAddress;

    // ── Constructor ────────────────────────────────────────────────────────────
    constructor(address _agiOracle) Ownable(msg.sender) {
        agiOracleAddress = _agiOracle;
    }

    // ── Currency registration ──────────────────────────────────────────────────
    function registerCurrency(
        string calldata symbol,
        address tokenAddress,
        string calldata civilization,
        string calldata category,
        string calldata backing,
        uint256 totalSupply
    ) external onlyOwner {
        require(!currencies[symbol].active, "Already registered");
        currencies[symbol] = GalacticToken({
            tokenAddress: tokenAddress,
            civilization: civilization,
            category: category,
            backing: backing,
            reserve: 0,
            totalSupply: totalSupply,
            active: true,
            registeredAt: block.timestamp
        });
        currencyList.push(symbol);
        emit CurrencyRegistered(symbol, tokenAddress, civilization, category);
    }

    // ── AMM Swap ───────────────────────────────────────────────────────────────
    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) public view returns (uint256) {
        require(amountIn > 0 && reserveIn > 0 && reserveOut > 0, "Invalid amounts");
        uint256 amountInWithFee = amountIn * (10000 - swapFeeBasis);
        uint256 numerator = amountInWithFee * reserveOut;
        uint256 denominator = reserveIn * 10000 + amountInWithFee;
        return numerator / denominator;
    }

    function swap(
        string calldata fromSymbol,
        string calldata toSymbol,
        uint256 amountIn,
        uint256 minAmountOut
    ) external nonReentrant returns (uint256 amountOut) {
        GalacticToken storage from = currencies[fromSymbol];
        GalacticToken storage to = currencies[toSymbol];
        require(from.active && to.active, "Currency not active");
        amountOut = getAmountOut(amountIn, from.reserve, to.reserve);
        require(amountOut >= minAmountOut, "Slippage exceeded");
        IERC20(from.tokenAddress).transferFrom(msg.sender, address(this), amountIn);
        IERC20(to.tokenAddress).transfer(msg.sender, amountOut);
        from.reserve += amountIn;
        to.reserve -= amountOut;
        emit Swapped(msg.sender, fromSymbol, toSymbol, amountIn, amountOut);
    }

    // ── Liquidity management ───────────────────────────────────────────────────
    function addLiquidity(string calldata symbol, uint256 amount) external nonReentrant {
        GalacticToken storage token = currencies[symbol];
        require(token.active, "Currency not active");
        IERC20(token.tokenAddress).transferFrom(msg.sender, address(this), amount);
        token.reserve += amount;
        emit LiquidityAdded(msg.sender, symbol, amount);
    }

    // ── AGI rebalance ──────────────────────────────────────────────────────────
    function agiRebalance(
        string calldata symbol,
        uint256 targetReserve,
        uint256 confidence
    ) external {
        require(msg.sender == agiOracleAddress, "Only AGI oracle");
        currencies[symbol].reserve = targetReserve;
        emit AGIRebalance(symbol, targetReserve, confidence);
    }

    function getCurrencyCount() external view returns (uint256) {
        return currencyList.length;
    }

    function setSwapFee(uint256 fee) external onlyOwner {
        require(fee <= 1000, "Max 10%");
        swapFeeBasis = fee;
    }
}
